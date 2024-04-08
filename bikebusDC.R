library(dplyr)
library(tidyr)
library(openxlsx)
library(stringr)
library(data.table)
library(mlogit)
library(Formula)

rm(list=ls())
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))


# Referencias -------------------------------------------------------------

# https://cran.r-project.org/web/packages/mlogit/vignettes/c2.formula.data.html

data("Train", package = "mlogit")


# Preparação Dados ---------------------------------------------------------


bd <- fread("../../Dados/CSV/Parangaba_todos.csv")

bd <- bd %>% 
  select(!c(ESCOLHA_CODIFICADA,TELA)) %>%
  rename(ID_INDIVIDUO = ID_FORMULARIO) %>% 
  group_by(ID_INDIVIDUO) %>% 
  mutate(ID = paste0(ID_INDIVIDUO,"_",row_number()),
         ID_RESPOSTA = row_number(),.after=ID_INDIVIDUO) %>% 
  ungroup()

bd <- bd %>% 
  mutate(ESCOLHA = toupper(ESCOLHA))

bd_preparado <- dfidx(bd, 
                      shape = "wide",
                      choice="ESCOLHA",
                      idx = "ID",
                      idnames = c("ID","alternativa"))

bd_preparado <- bd_preparado %>% 
  mutate(TEMPO_O = ifelse(idx$alternativa == "ÔNIBUS",TEMPO_O,0),
         CAMINHADAESPERA_O = ifelse(idx$alternativa == "ÔNIBUS",CAMINHADAESPERA_O,0),
         TEMPO_B = ifelse(idx$alternativa != "ÔNIBUS",TEMPO_B,0),
         BICI_BP = ifelse(idx$alternativa == "BICICLETA PRÓPRIA",BICI_BP,0),
         CICLO_B = ifelse(idx$alternativa != "ÔNIBUS",CICLO_B,0),
         TEMPO_B_SCALED = TEMPO_B / 100,
         CAMINHADAESPERA_O_SCALED = CAMINHADAESPERA_O / 100,
         TEMPO_O_SCALED = TEMPO_O / 100)

bd_preparado <- bd_preparado %>% 
  mutate(MOTIVO = ifelse(idx$alternativa == "ÔNIBUS",MOTIVO,0),
         GENERO = ifelse(idx$alternativa == "ÔNIBUS",GENERO,0),
         RENDA_FAIXA1 = ifelse(idx$alternativa == "ÔNIBUS",RENDA_FAIXA1,0),
         RENDA_FAIXA2 = ifelse(idx$alternativa == "ÔNIBUS",RENDA_FAIXA2,0),
         DIST_1500_3500 = ifelse(idx$alternativa == "ÔNIBUS",DIST_1500_3500,0),
         DIST_ATE1500 = ifelse(idx$alternativa == "ÔNIBUS",DIST_ATE1500,0))



# Roda modelos ------------------------------------------------------------

# Multinomial logit

multinomial <- mlogit(data=bd_preparado,
                      formula = ESCOLHA ~ CICLO_B + BICI_BP + TEMPO_O_SCALED + TEMPO_B_SCALED + CAMINHADAESPERA_O + GENERO + MOTIVO + RENDA_FAIXA1 + RENDA_FAIXA2 + DIST_ATE1500 + DIST_1500_3500,
                      reflevel = "ÔNIBUS")

coef <- as.data.frame(multinomial$coefficients)
summary(multinomial)  

# Nested logit

nested <- mlogit(data=bd_preparado,
                 formula = ESCOLHA ~ CICLO_B + BICI_BP + TEMPO_O_SCALED + TEMPO_B_SCALED + CAMINHADAESPERA_O_SCALED + GENERO + MOTIVO + RENDA_FAIXA1 + RENDA_FAIXA2 + DIST_ATE1500 + DIST_1500_3500,
                 reflevel = "ÔNIBUS",
                 nests =list(BUS = "ÔNIBUS",BIKE = c("BICICLETA INTEGRADA","BICICLETA PRÓPRIA")),
                 un.nest.el = T)
coef <- as.data.frame(nested$coefficients)
summary(nested)

# Mixed

mixed <- mlogit(data=bd_preparado,
                formula = ESCOLHA ~ CICLO_B + BICI_BP + TEMPO_O_SCALED + TEMPO_B_SCALED + CAMINHADAESPERA_O_SCALED + GENERO + MOTIVO + RENDA_FAIXA1 + RENDA_FAIXA2 + DIST_ATE1500 + DIST_1500_3500,
                reflevel = "ÔNIBUS",
                rpar = c(TEMPO_B_SCALED = "ln",
                         CICLO_B = "ln"),
                R = 5000,
                halton = NA)
coef <- as.data.frame(mixed$coefficients)
summary(mixed)  


