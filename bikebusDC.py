# -*- coding: utf-8 -*-

# Bibliotecas
import os
import pandas as pd 

import biogeme.version as ver
print(ver.getText())
import biogeme.database as db 
from biogeme.expressions import (
    Variable, Beta, bioDraws, log, MonteCarlo,RandomVariable,Integrate)
import biogeme.distributions as dist
import biogeme.biogeme as bio 
from biogeme import models
from biogeme.nests import OneNestForNestedLogit, NestsForNestedLogit

# Config

os.chdir('D:/OneDrive/Análises/PD - BikeBus Fortaleza/Estimações/Nova Versão - 2024')
os.getcwd()




################## Modelo Global

# Importa bd
arquivo = '../../Dados/CSV/Parangaba_todos.csv'

nome_estimacao = os.path.splitext(os.path.basename(arquivo))[0]

df = pd.read_csv(arquivo, sep=';').drop(columns='ESCOLHA')
database = db.Database('Global', df)


# Prepara variáveis
GENERO = Variable('GENERO') 
MOTIVO = Variable('MOTIVO') 
RENDA_FAIXA1 = Variable('RENDA_FAIXA1') 
RENDA_FAIXA2 = Variable('RENDA_FAIXA2')
RENDA_FAIXA3 = Variable('RENDA_FAIXA3')
DIST_ATE1500 = Variable('DIST_ATE1500') 
DIST_1500_3500 = Variable('DIST_1500_3500')
DIST_MAIOR3500 = Variable('DIST_MAIOR3500') 
CAMINHADAESPERA_O = Variable('CAMINHADAESPERA_O') 
TEMPO_O = Variable('TEMPO_O') 
TEMPO_B = Variable('TEMPO_B') 
CICLO_B = Variable('CICLO_B') 
BICI_BP = Variable('BICI_BP') 
ESCOLHA = Variable('ESCOLHA') 
ESCOLHA_CODIFICADA = Variable('ESCOLHA_CODIFICADA') 


# Transformacoes
TEMPO_B_SCALED = TEMPO_B / 100.0
CAMINHADAESPERA_O_SCALED = CAMINHADAESPERA_O / 100.0
TEMPO_O_SCALED = TEMPO_O / 100.0

# Define Parâmetros (nome, default_value,lower_bound,upper_bound,flag -> if must be estimated = 0)
ASC_INTEGRADA = Beta('ASC_INTEGRADA',0,None,None,0)                       
ASC_BP = Beta( 'ASC_BP',0,None,None,0)                           
ASC_BUS = Beta( 'ASC_BUS' ,0,None,None,1)
B_GENERO = Beta('B_GENERO' ,0,None,None,0)
B_MOTIVO = Beta( 'B_MOTIVO' ,0,None,None,0)
B_RENDA_FAIXA1 = Beta('B_RENDA_FAIXA1'  ,0,None,None,0)
B_RENDA_FAIXA2 = Beta('B_RENDA_FAIXA2' ,0,None,None,0)
B_DIST_ATE1500 = Beta('B_DIST_ATE1500'   ,0,None,None,0)
B_DIST_1500_3500 = Beta('B_DIST_1500_350',0,None,None,0)
B_TEMPO_B = Beta('B_TEMPO_B'  ,0,None,None,0)
B_CICLO_B = Beta('B_CICLO_B'   ,0,None,None,0)
B_BICI_BP = Beta('B_BICI_BP' ,0,None,None,0)
B_CAMINHADAESPERA_O = Beta('B_CAMINHADAESPERA_O' ,0,None,None,0)
B_TEMPO_O = Beta('B_TEMPO_O' ,0,None,None,0)
MU = Beta('MU', 1, 1, 10, 0)


# Funções utilidade

V1 = (ASC_BP + B_TEMPO_B * TEMPO_B_SCALED + B_CICLO_B * CICLO_B + B_BICI_BP * BICI_BP) 
V2 = (ASC_INTEGRADA + B_TEMPO_B * TEMPO_B_SCALED + B_CICLO_B * CICLO_B )
V3 = (ASC_BUS + B_CAMINHADAESPERA_O * CAMINHADAESPERA_O_SCALED + B_TEMPO_O * TEMPO_O_SCALED + B_GENERO * GENERO + B_MOTIVO * MOTIVO + B_RENDA_FAIXA1 * RENDA_FAIXA1 + B_RENDA_FAIXA2 * RENDA_FAIXA2 + B_DIST_ATE1500 * DIST_ATE1500 + B_DIST_1500_3500 * DIST_1500_3500)

V = {1: V1, 2: V2, 3: V3}

# Availability of choice alternativs
av = {1: 1, 2: 1, 3: 1}

# Nests
existing = OneNestForNestedLogit(nest_param=MU, list_of_alternatives=[1, 2], name='BICICLETA')
nests = NestsForNestedLogit(choice_set=list(V), tuple_of_nests=(existing,))


# Roda modelos
logprob = models.loglogit(V, av, ESCOLHA_CODIFICADA)
logprob = models.lognested(V, av, nests, ESCOLHA_CODIFICADA) # nested


the_biogeme = bio.BIOGEME(database, logprob)
the_biogeme.modelName = nome_estimacao
the_biogeme.calculateNullLoglikelihood(av)
results = the_biogeme.estimate()





##################### Modelos segmentados

# Importa bd
arquivo = '../../Dados/CSV/Parangaba_homem.csv'
#arquivo = '../../Dados/CSV/Parangaba_mulher.csv'
#arquivo = '../../Dados/CSV/Parangaba_trabalho.csv'
#arquivo = '../../Dados/CSV/Parangaba_estudo.csv'
#arquivo = '../../Dados/CSV/Parangaba_rendaAte1500.csv'
#arquivo = '../../Dados/CSV/Parangaba_rendaMaior1500.csv'


nome_estimacao = os.path.splitext(os.path.basename(arquivo))[0]

df = pd.read_csv(arquivo, sep=';').drop(columns='ESCOLHA')
database = db.Database(nome_estimacao, df)


# Prepara variáveis
GENERO = Variable('GENERO') 
MOTIVO = Variable('MOTIVO') 
RENDA_FAIXA1 = Variable('RENDA_FAIXA1') 
RENDA_FAIXA2 = Variable('RENDA_FAIXA2')
RENDA_FAIXA3 = Variable('RENDA_FAIXA3')
DIST_ATE1500 = Variable('DIST_ATE1500') 
DIST_1500_3500 = Variable('DIST_1500_3500')
DIST_MAIOR3500 = Variable('DIST_MAIOR3500') 
CAMINHADAESPERA_O = Variable('CAMINHADAESPERA_O') 
TEMPO_O = Variable('TEMPO_O') 
TEMPO_B = Variable('TEMPO_B') 
CICLO_B = Variable('CICLO_B') 
BICI_BP = Variable('BICI_BP') 
ESCOLHA = Variable('ESCOLHA') 
ESCOLHA_CODIFICADA = Variable('ESCOLHA_CODIFICADA') 


# Transformacoes
TEMPO_B_SCALED = TEMPO_B / 100.0
CAMINHADAESPERA_O_SCALED = CAMINHADAESPERA_O / 100.0
TEMPO_O_SCALED = TEMPO_O / 100.0

# Define Parâmetros (nome, default_value,lower_bound,upper_bound,flag -> if must be estimated = 0)
ASC_INTEGRADA = Beta('ASC_INTEGRADA',0,None,None,0)                       
ASC_BP = Beta( 'ASC_BP',0,None,None,0)                           
ASC_BUS = Beta( 'ASC_BUS' ,0,None,None,1)
B_GENERO = Beta('B_GENERO' ,0,None,None,0)
B_MOTIVO = Beta( 'B_MOTIVO' ,0,None,None,0)
B_RENDA_FAIXA1 = Beta('B_RENDA_FAIXA1'  ,0,None,None,0)
B_RENDA_FAIXA2 = Beta('B_RENDA_FAIXA2' ,0,None,None,0)
B_DIST_ATE1500 = Beta('B_DIST_ATE1500'   ,0,None,None,0)
B_DIST_1500_3500 = Beta('B_DIST_1500_350',0,None,None,0)
B_TEMPO_B = Beta('B_TEMPO_B'  ,0,None,None,0)
B_CICLO_B = Beta('B_CICLO_B'   ,0,None,None,0)
B_BICI_BP = Beta('B_BICI_BP' ,0,None,None,0)
B_CAMINHADAESPERA_O = Beta('B_CAMINHADAESPERA_O' ,0,None,None,0)
B_TEMPO_O = Beta('B_TEMPO_O' ,0,None,None,0)
MU = Beta('MU', 1, 1, 10, 0)


# Funções utilidade

V1 = (ASC_BP + B_TEMPO_B * TEMPO_B_SCALED + B_CICLO_B * CICLO_B + B_BICI_BP * BICI_BP) 
V2 = (ASC_INTEGRADA + B_TEMPO_B * TEMPO_B_SCALED + B_CICLO_B * CICLO_B )
V3 = (ASC_BUS + B_CAMINHADAESPERA_O * CAMINHADAESPERA_O_SCALED + B_TEMPO_O * TEMPO_O_SCALED )#+ B_DIST_ATE1500 * DIST_ATE1500 + B_DIST_1500_3500 * DIST_1500_3500)

V = {1: V1, 2: V2, 3: V3}

# Availability of choice alternativs
av = {1: 1, 2: 1, 3: 1}

# Nests
existing = OneNestForNestedLogit(nest_param=MU, list_of_alternatives=[1, 2], name='BICICLETA')
nests = NestsForNestedLogit(choice_set=list(V), tuple_of_nests=(existing,))


# Roda modelos
logprob = models.loglogit(V, av, ESCOLHA_CODIFICADA)
logprob = models.lognested(V, av, nests, ESCOLHA_CODIFICADA) # nested


the_biogeme = bio.BIOGEME(database, logprob)
the_biogeme.modelName = nome_estimacao
the_biogeme.calculateNullLoglikelihood(av)
results = the_biogeme.estimate()


