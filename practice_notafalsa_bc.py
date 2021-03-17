# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 17:20:27 2021

@author: Enzo Golfetti
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
nf = pd.read_csv('Falsificacao_DadosAbertos.csv')
nf.rename({'1995;PARANÁ;Cédulas - 1a. família;50.00;237' : 'cedulas'}, axis=1, inplace=True)
nf.set_axis(['cedulas'], axis=1, inplace=True)
nf.drop('00', axis=1, inplace=True) #jeito mais fácil seria só aplicar o 'del'
#separando conteúdo dentro da coluna
# com strings usar o split indicando o separador que está na coluna
nf['ano'], nf['estado'], nf['classe'], nf['valor'], nf['quant'] = nf.cedulas.str.split(';').str
nf.drop('cedulas', axis=1, inplace=True)
total_50 = nf[nf['valor'] == '50.00'].count()
total_100 = nf[nf['valor'] == '100.00'].count()
total_5 = nf[nf['valor'] == '5.00'].count()
total_10 = nf[nf['valor'] == '10.00'].count()
total_20 = nf[nf['valor'] == '20.00'].count()
#esse monte de código acima é equivalente à usar .value_counts()
nf['valor'].value_counts()
#função que simplifica essas entradas acima é .value_counts()
# convertendo classes de objetos para outras nas colunas
# usar astype() e copy=False se quiser mudar no Dataframe
nf2 = nf.convert_dtypes()
nf2.dtypes
nf3 = nf2.astype({'valor' : 'float64'}, copy=False) #convertendo a coluna valor
#temos que jogar para dentro de outro Dataframe, por isso de nf3
nf3.dtypes
# tentando converter todos os valores direto
nf4 = nf2.astype({'ano' : 'string', 'valor' : 'string', 'quant' : 'float64'}, copy=False)
nf4.dtypes
#usando o groupy() para simplificar as observações
valor = nf4.groupby(nf4['valor'])
valor.sum()
#fazendo gráficos destes dados
fig, ax = plt.subplots(figsize=(10,10)) #observação da quant de cédulas
ax.barh(nf4['valor'], nf4['quant'], color='black', lw=1)
 
fig, ax = plt.subplots(figsize=(20,10))
plt.style.available #ver os estilos disponiveis
plt.style.use('dark_background')
ax.bar(nf4['ano'], nf4['quant'], color='red')
ax.set_xlabel('ANO', color='red')
ax.set_ylabel('Quant.')
ax.set_title('Quantidade apreendida por ano')
plt.tight_layout()
nf4[nf4['ano']=='2020']['quant'].sum()

