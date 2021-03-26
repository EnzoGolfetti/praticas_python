# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 13:39:37 2020

@author: enzo
"""
import pandas as pd
import numpy as np
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
sal = pd.read_csv('Salaries.csv')
salhead = sal.head()
sal.info()
sal.describe()
jobs = sal['JobTitle']
total_benefits = sal['TotalPayBenefits']
total_benefits.describe() # 5 number summary
#transformando o 5 number summary em DataFrame para visualização
fns = pd.DataFrame(sal['TotalPayBenefits'].describe()) 
histogram = sns.distplot(total_benefits, kde=False, bins=300).set_title('Histograma de TotalBenefits')
# o histograma é uma boa forma de se analisar inicialmente dados
# o boxplot é uma forma gráfica de apresentar os 5 number summary
boxplot = sns.boxplot(sal['TotalPayBenefits'])
dispersao = sns.jointplot(x='TotalPay', y='TotalPayBenefits', data=sal)
corr = stats.pearsonr(sal['TotalPay'], sal['TotalPayBenefits'])
print(f'A correlação de Pearson entre os pagamentos é {corr}')
# Qual o maior salário pago em 2014?
sal[sal['Year']== 2014]['TotalPayBenefits'].max()
# Quantas pessoas receberam mais de 100.000 em 2013?
sal[(sal['Year'] == 2013) & (sal['TotalPay']>100000)].count()
# Qual a média de pagamentos em SF? E a Mediana?
total_benefits.mean()
total_benefits.median()
