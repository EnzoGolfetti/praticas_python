#Importar bibliotecas
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import requests
import re
import os
import time
import datetime
import random
import pandas as pd
import numpy as np

#Printa a hora que começou a rodar o código
print(datetime.datetime.now())

def esperar(segundos=None):
    """Caso nenhum valor seja atribuido, 
    será atribuido um tempo randomico entre 2 e 8
    (Feito desta forma para simular a ação de um usuário)"""
    if not segundos:
        segundos = random.randrange(2,8)
    time.sleep(segundos)

#Definindo credenciais
site_login = os.environ.get('USERNAME_PROJETO_JULIA')
site_pwd = os.environ.get('PASSWORD_PROJETO_JULIA')

#Criar um objeto do Selenium
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

driver.maximize_window()

#Acessar página inicial do Site
driver.get("https://otus-ora.otus-solutions.com.br/#/login")
esperar(10)

#Inserir USERNAME
driver.find_element(By.NAME, 'userEmail').send_keys(site_login)
esperar(4)

#Inserir PASSWORD
driver.find_element(By.NAME, 'userPassword').send_keys(site_pwd)
esperar(4)

#Apertar botão de login
driver.find_element(By.XPATH, '//*[@id="user-login-page"]/div[1]/md-card/form/div/div[2]/button[1]').click()
esperar(7)

#Apertar botão "Exibir todos"
driver.find_element(By.XPATH, '/html/body/div[1]/div/div/otus-dashboard/div/otus-dashboard-home-display/md-content/div/div/div[1]/div/otus-participant-search/md-autocomplete/md-autocomplete-wrap/button').click()
esperar(10)

#Aumentar o limite de linhas para 500
limitador_linhas = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/otus-participants-manager-dashboard/div/div/otus-participants-list/md-content/md-content/div/dynamic-data-table/md-whiteframe/div[3]/div[3]/div[2]/div[2]')
esperar(3)
limitador_linhas.click()
esperar(3)
#Não esquecer de documentar porque usei uma forma ineficiente aqui
limitador_linhas.find_element(By.XPATH, '/html/body/div[5]/md-select-menu/md-content/md-option[6]').click()
esperar(30)

#Encontrar filtro de buscas
barrra_de_pesquisa = driver.find_element(By.XPATH, '//*[starts-with(@id, "input_")]')
esperar(10)

#Lista de itens que serão pesquisados na barra de pesquisa
lista_itens = ['refresco', 'pó para bebida', 'nuggets', 'presunto cozido', 'apresuntado', 'mortadela', 'linguiça',
                'Biscoito integral', 'Biscoito de polvilho', 'Biscoito água e sal', 'salsicha', 'salame', 'paio', 'steaks', 
                'hambúrguer', 'hamburguer', 'barbecue', 'molho de alho', 'molho de pimenta', 'molho inglês', 'ketchup', 'molho para salada', 
                'maionese', 'mostarda', 'shoyu', 'tempero para', 'tempero pronto', 'preparado para'
            ]

#Dicionário auxiliar
dict_forms_products = dict()

#Nome do produto - está na parte de cima do forms
#descrição do produto - se não tiver não pode apagar (só essa, todas as outras se não tiver pode apagar)
lista_perguntas = ['Qual o endereço do ponto de venda?', 'Qual a razão social do ponto de venda?', 'Qual a consistência do alimento?', 'Escolha o grupo ao qual o alimento pertence:',
                    'Subgrupo X:', 'Qual a denominação de venda do produto?', 'Qual a marca fantasia do produto?', 'Peso líquido do produto?',
                    'Qual a porção?', 'Qual a quantidade de carboidratos na porção?', 'Há declaração de açúcar?', 'Qual a quantidade de açúcares totais na porção?',
                    'Qual a quantidade de gorduras saturadas na porção?', 'Qual a quantidade de sódio na porção?', 
                    'Digite a lista de ingredientes do alimento, conforme é apresentado no rótulo (somente ingredientes).'
                    ]

#Definição de perguntas que queremos a resposta
lista_perguntas_codigos = [1, 2, 4, 5, """Aqui vou colocar a lógica de buscar o número do grupo marcado + 6""", 16, 18, 23, 32, 36, 38, 39, 44, 49, 51]

#Dicionários auxiliares
dict_respostas = dict()
dict_forms_products_2 = dict()
counter_product = 0

#Looping para cada item na lista de pesquisas
for item in lista_itens:
    #Pesquisa item na barra
    barrra_de_pesquisa.clear()
    barrra_de_pesquisa.send_keys(item)
    #Aguarda
    esperar(5)
    #Encontrar a tabela já filtrada apresentada
    table_from_item = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/otus-participants-manager-dashboard/div/div/otus-participants-list/md-content/md-content/div/dynamic-data-table/md-whiteframe/div[3]')
    #Script internalizado do Selenium para encontrar o HTML
    html_source_code = driver.execute_script("return document.body.innerHTML;")
    #Passar o HTML da página com BeautifulSoup
    html_soup = BeautifulSoup(html_source_code, 'html.parser')
    #Encontrar a lista de ID's que tenham "bodyRow" em qualquer ponto do texto para ter as linhas que foram filtradas na tabela
    ids = [tag['id'] for tag in html_soup.find_all(id=re.compile('bodyRow'))]
    esperar(5)
    #Agora deve-se iterar sobre a lista de ID's encontrada e fazer todas as demais interações dentro desse for
    for id in ids:
        
        #Linhas auxiliares para buscar o nome do produto do ID correspondente
        linha_do_id_table = html_soup.find(id = id)
        textos = linha_do_id_table.find_all('span', attrs={'class': 'md-body-1 ng-binding ng-scope'})
        nome_produto = [texto.text.strip() for texto in textos][1]

        #Clicka no primeiro participante
        driver.find_element(By.XPATH, f'//*[@id="{id}"]/div[8]/button').click()
        esperar(20)
        #Após acessar o dashboard - clicka em 'Atividades'
        driver.find_element(By.XPATH, '//*[@id="surveyforms-menu"]/div/button').click()
        esperar(20)
        #Buscar HTML completo da página para avaliação
        html_source_code_page_product = driver.execute_script("return document.body.innerHTML;")
        esperar(5)
        #Pass to BeautifulSoup
        html_soup_product = BeautifulSoup(html_source_code_page_product, 'html.parser')
        esperar(5)
        #Pass to an object
        lista_header2 = html_soup_product.find_all(string='Participante não possui atividades') #Participante não possui atividades
        print(lista_header2)
        esperar(10)
        
        #Testa se houve preenchimento da lista com o header 
        if len(lista_header2) > 0:
            text_sem_atividade2 = lista_header2[0]
        else:
            text_sem_atividade2 = ''

        #Verifica se no Header tem o texto de erro
        if 'Participante não possui atividades' in text_sem_atividade2:
            """Se não tem atividades tem que retornar no looping"""
            esperar(5)
            #Aperta em HOME
            driver.find_element(By.XPATH, '//*[@id="home-menu"]/div/button').click()
            esperar(15)
            #Apertar em exibir todos
            driver.find_element(By.XPATH, '/html/body/div[1]/div/div/otus-dashboard/div/otus-dashboard-home-display/md-content/div/div/div[1]/div/otus-participant-search/md-autocomplete/md-autocomplete-wrap/button').click()
            esperar(10)

            #Aumentar o limite de linhas para 500
            limitador_linhas = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/otus-participants-manager-dashboard/div/div/otus-participants-list/md-content/md-content/div/dynamic-data-table/md-whiteframe/div[3]/div[3]/div[2]/div[2]')
            esperar(3)
            limitador_linhas.click()
            esperar(3)
            #Não esquecer de documentar porque usei uma forma ineficiente aqui
            limitador_linhas.find_element(By.XPATH, '/html/body/div[5]/md-select-menu/md-content/md-option[6]').click()
            esperar(15)
            #Buscar caixa de pesquisa novamente
            barrra_de_pesquisa = driver.find_element(By.XPATH, '//*[starts-with(@id, "input_")]')
            esperar(10)
            #Pesquisa item na barra novamente
            barrra_de_pesquisa.send_keys(item)
            #Aguarda
            esperar(5)

        #Se não tem o texto de erro vai para o forms do banco de dados
        else:
            driver.refresh()
            esperar(10)
            try:
                #Clickar no banco de dados
                driver.find_element(By.XPATH, '//*[@id="activity0"]/figure/md-grid-tile-header/figcaption/div').click()
                esperar(8)
                #Clickar no botão de visualizar atividade
                driver.find_element(By.XPATH, '/html/body/div[1]/div/div/otus-participant-dashboard/div/div/otus-dashboard-display/div/otus-activity-manager/otus-activity-manager-bottom-sheet/md-bottom-sheet/div/button[2]').click()
                esperar(10)
                #Tentar puxar o formulário e correr o processo normal de extração e obtenção do itens relevantes
                try:
                    #Pegar o forms em HTML com o BeautifulSoup
                    html_source_code_forms_product = driver.execute_script("return document.body.innerHTML;")
                    html_soup_forms_product = BeautifulSoup(html_source_code_forms_product, 'html.parser')
                    dict_forms_products[nome_produto] = html_soup_forms_product

                    #Lista de itens para verificar se pode excluir o produto já do dicionário
                    lista_perguntas_codigos_verificacao = [1, 2, 4, 16, 18, 23, 32, 36, 38, 39, 44, 49, 51]
                    lista_auxiliar_respostas = []
                    #Verificação de pergunta estar respondida
                    for codigo_pergunta in lista_perguntas_codigos_verificacao:
                        #Passa a pergunta como objeto
                        pergunta_aux = html_soup_forms_product.find_all('survey-item-view')[codigo_pergunta]
                        reposta_aux = pergunta_aux.find('span', attrs={'class' : 'md-caption ng-binding ng-hide'}).text.strip().lower()
                        lista_auxiliar_respostas.append(reposta_aux)
                    
                    esperar(5)
                    #Avalia se tem alguma pergunta só visitada na lista auxiliar
                    if 'visitada' in lista_auxiliar_respostas:
                        dict_forms_products.pop(nome_produto)
                        print(dict_forms_products.keys())

                    #########################################################################################################################
                    else:
                        """Etapa de utilização da biblioteca BeautifulSoup para tratamento das perguntas coletadas
                        """
                        print(dict_forms_products.keys())
                        #Dict auxiliar é criado a cada produto que é inserido no dicionário
                        dict_de_para_codigos = {1 : lista_perguntas[0],
                                                2 : lista_perguntas[1],
                                                4 : lista_perguntas[2],
                                                5 : lista_perguntas[3],
                                                6 : lista_perguntas[4],
                                                16 : lista_perguntas[5],
                                                18 : lista_perguntas[6],
                                                23 : lista_perguntas[7],
                                                32 : lista_perguntas[8],
                                                36 : lista_perguntas[9],
                                                38 : lista_perguntas[10],
                                                39 : lista_perguntas[11],
                                                44 : lista_perguntas[12],
                                                49 : lista_perguntas[13],
                                                51 : lista_perguntas[14]
                                                }
                        
                        dict_respostas = dict()

                        #Resgatando a page HTML
                        forms = dict_forms_products[nome_produto]

                        #Definindo posição do subgrupo
                        pergunta_grupo = forms.find_all('survey-item-view')[5]

                        #Garantindo que o código não quebre se 5 estiver sem resposta
                        if 'visitada' in pergunta_grupo.find('span', attrs={'class' : 'md-caption ng-binding ng-hide'}).text.strip().lower():
                            #Definição de perguntas sem grupo e subgrupo
                            lista_perguntas_codigos = [1, 2, 4, 16, 18, 23, 32, 36, 38, 39, 44, 49, 51]
                            dict_de_para_codigos.pop(5)
                            dict_de_para_codigos.pop(6)

                        else:
                            for i in pergunta_grupo.find_all('div', attrs={'class' : 'ng-scope layout-align-start-center'}):
                                if 'false' in str(i.find('md-icon', attrs={'aria-label' : 'radio_button_checked'})):
                                    pergunta_substituir = int(re.findall(r'\d+',i.find(string=re.compile('Grupo')).strip())[0]) + 5 
                                    # Tem que somar esse número mais 1 mais o número dessa pergunta que é 5 para chegar na prox.
                                    lista_perguntas[4] = "Subgrupo " + re.findall(r'\d+',i.find(string=re.compile('Grupo')).strip())[0] + ":"
                                    dict_de_para_codigos[pergunta_substituir] = dict_de_para_codigos.pop(6)
                                    dict_de_para_codigos[pergunta_substituir] = lista_perguntas[4] 
                            
                            #Definição de perguntas com grupo e subgrupo
                            lista_perguntas_codigos = [1, 2, 4, 5, pergunta_substituir, 16, 18, 23, 32, 36, 38, 39, 44, 49, 51]
                        
                        #Garantindo que o código não quebre se na 38 a resposta for NÃO
                        #Definindo posição do açúcar (38)
                        pergunta_acucar_ext = forms.find_all('survey-item-view')[38]
                        if 'Sim' in str(pergunta_acucar_ext.find('div', attrs={'class' : 'ng-scope layout-align-start-center'})):
                            checked_button_style = pergunta_acucar_ext.find('md-icon', attrs={'aria-label' : 'radio_button_checked'})

                            #Se marcar que não tem açúcar
                            if 'true' in str(checked_button_style):
                                #Exclui a 39 da lista de perguntas
                                lista_perguntas_codigos.remove(39)
                                dict_de_para_codigos.pop(39)


                        #Loop de coletar respostas das perguntas
                        for cod_pergunta in lista_perguntas_codigos:
                            #IF para quando não são as perguntas com RADIO BUTTONS
                            if ( (cod_pergunta != 4) and (cod_pergunta != 38) and (cod_pergunta != 5) and 
                                (cod_pergunta != 7) and (cod_pergunta != 8) and (cod_pergunta != 9) and
                                (cod_pergunta != 10) and (cod_pergunta != 11) and (cod_pergunta != 12) and 
                                (cod_pergunta != 13) and (cod_pergunta != 14) and (cod_pergunta != 15) 
                                ):
                                #Passar objeto da resposta
                                pergunta_comum = forms.find_all('survey-item-view')[cod_pergunta]

                                resposta_comum = [texto.text.strip() for texto in pergunta_comum.find_all('p')][1]

                                dict_respostas[dict_de_para_codigos[cod_pergunta]] = resposta_comum
                            
                            #Se for a pergunta 4 com radio button
                            elif cod_pergunta == 4:
                                pergunta_comum = forms.find_all('survey-item-view')[cod_pergunta]

                                #Código para pergunta sobre consistência do alimento
                                if 'Sólido' in str(pergunta_comum.find('div', attrs={'class' : 'ng-scope layout-align-start-center'})):
                                    checked_button_style = pergunta_comum.find('md-icon', attrs={'aria-label' : 'radio_button_checked'})

                                    if 'true' in str(checked_button_style):
                                        resposta_comum = 'Líquido'
                                    else:
                                        #Se o radio_button_checked (checked_button_style) for False é porque foi aquele opção que foi selecionada no forms.
                                        resposta_comum = 'Sólido'
                                
                                dict_respostas[dict_de_para_codigos[cod_pergunta]] = resposta_comum
                            
                            #Se for a pergunta 5 com radio button
                            elif cod_pergunta == 5:
                                pergunta_comum = forms.find_all('survey-item-view')[cod_pergunta]

                                #Avaliando qual foi o grupo marcado para o alimento
                                for i in pergunta_comum.find_all('div', attrs={'class' : 'ng-scope layout-align-start-center'}):
                                    if 'false' in str(i.find('md-icon', attrs={'aria-label' : 'radio_button_checked'})):

                                        #Se foi o grupo 8 tem que ser tratado diferente pois tem uma tag 'span' entre o grupo e o texto
                                        if int(re.findall(r'\d+',i.find(string=re.compile('Grupo')).strip())[0]) == 8:

                                            for j in pergunta_comum.find_all('div', attrs={'class' : 'ng-scope layout-align-start-center'}):
                                                if 'false' in str(j.find('md-icon', attrs={'aria-label' : 'radio_button_checked'})):
                                                    resposta_comum = [texto.text.strip() for texto in list(j.find('span'))[1]][0]
                                        
                                        else:
                                            lista_com_resposta_aux = [texto.text.strip() for texto in list(pergunta_comum.find('div', attrs={'class' : 'ng-scope layout-align-start-center'})\
                                                                                                                        .find('span', attrs={'class' : 'ng-binding'}))]
                                            resposta_comum = lista_com_resposta_aux[0].split('\xa0')[1]
                                
                                dict_respostas[dict_de_para_codigos[cod_pergunta]] = resposta_comum

                            #Se for a pergunta variável entre 7 e 15 com radio button
                            elif cod_pergunta == pergunta_substituir:
                                pergunta_comum = forms.find_all('survey-item-view')[cod_pergunta]

                                for i in pergunta_comum.find_all('div', attrs={'class' : 'ng-scope layout-align-start-center'}):

                                    if 'false' in str(i.find('md-icon', attrs={'aria-label' : 'radio_button_checked'})):
                                        resposta_comum = [texto.text.strip() for texto in list(i.find('span'))][0]
                                
                                dict_respostas[dict_de_para_codigos[cod_pergunta]] = resposta_comum
                            
                            #Se for a pergunta 38 do açúcar com radio button
                            elif cod_pergunta == 38:
                                pergunta_comum = forms.find_all('survey-item-view')[cod_pergunta]

                                if 'Sim' in str(pergunta_comum.find('div', attrs={'class' : 'ng-scope layout-align-start-center'})):
                                    checked_button_style = pergunta_comum.find('md-icon', attrs={'aria-label' : 'radio_button_checked'})

                                    #Se o radio_button_checked (checked_button_style) for False é porque foi aquele opção que foi selecionada no forms.
                                    if 'false' in str(checked_button_style):
                                        resposta_comum = 'Sim'
                                    else:
                                        resposta_comum = 'Não'
                                
                                #Adiciona as respostas das perguntas ao dicionário
                                dict_respostas[dict_de_para_codigos[cod_pergunta]] = resposta_comum

                        dict_forms_products_2[nome_produto] = dict_respostas

                        #A cada 20 produtos já passar para um dataframe e salvar como CSV
                        counter_product += 1
                        if (counter_product % 20) == 0:
                            df_temp = pd.DataFrame.from_dict(dict_forms_products_2, orient='index')
                            df_temp = df_temp.rename(columns={dict_de_para_codigos[pergunta_substituir] : 'Subgrupo do alimento'})
                            #Exporta o DataFrame
                            df_temp.to_csv(f"banco_dados_tcc_julia_produtos_numero_{counter_product - 20}_a_{counter_product}_{str(datetime.datetime.today().date()).replace('-', '')}_v11.csv",
                                        sep=';', encoding='ISO-8859-1', index=True
                                        )
                    
                    #Aperta em sair do forms
                    driver.find_element(By.XPATH, '//*[@id="header-viewer"]/div/button[3]').click()
                    esperar(8)
                    #Aperta em HOME
                    driver.find_element(By.XPATH, '//*[@id="home-menu"]/div/button').click()
                    esperar(15)
                    #Apertar em exibir todos
                    driver.find_element(By.XPATH, '/html/body/div[1]/div/div/otus-dashboard/div/otus-dashboard-home-display/md-content/div/div/div[1]/div/otus-participant-search/md-autocomplete/md-autocomplete-wrap/button').click()
                    esperar(10)

                    #Aumentar o limite de linhas para 500
                    limitador_linhas = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/otus-participants-manager-dashboard/div/div/otus-participants-list/md-content/md-content/div/dynamic-data-table/md-whiteframe/div[3]/div[3]/div[2]/div[2]')
                    esperar(3)
                    limitador_linhas.click()
                    esperar(3)
                    #Não esquecer de documentar porque usei uma forma ineficiente aqui
                    limitador_linhas.find_element(By.XPATH, '/html/body/div[5]/md-select-menu/md-content/md-option[6]').click()
                    esperar(15)

                    #Buscar caixa de pesquisa novamente
                    barrra_de_pesquisa = driver.find_element(By.XPATH, '//*[starts-with(@id, "input_")]')
                    esperar(10)
                    #Pesquisa item na barra novamente
                    barrra_de_pesquisa.send_keys(item)
                    #Aguarda
                    esperar(5)

###############Se o formulário não carregar tenta atualizar a página dele
                except:
                    try:
                        driver.refresh()
                        #Pegar o forms em HTML com o BeautifulSoup
                        html_source_code_forms_product = driver.execute_script("return document.body.innerHTML;")
                        html_soup_forms_product = BeautifulSoup(html_source_code_forms_product, 'html.parser')
                        dict_forms_products[nome_produto] = html_soup_forms_product

                        #Lista de itens para verificar se pode excluir o produto já do dicionário
                        lista_perguntas_codigos_verificacao = [1, 2, 4, 16, 18, 23, 32, 36, 38, 39, 44, 49, 51]
                        lista_auxiliar_respostas = []
                        #Verificação de pergunta estar respondida
                        for codigo_pergunta in lista_perguntas_codigos_verificacao:
                            #Passa a pergunta como objeto
                            pergunta_aux = html_soup_forms_product.find_all('survey-item-view')[codigo_pergunta]
                            reposta_aux = pergunta_aux.find('span', attrs={'class' : 'md-caption ng-binding ng-hide'}).text.strip().lower()
                            lista_auxiliar_respostas.append(reposta_aux)
                        
                        esperar(5)
                        #Avalia se tem alguma pergunta só visitada na lista auxiliar
                        if 'visitada' in lista_auxiliar_respostas:
                            dict_forms_products.pop(nome_produto)
                            print(dict_forms_products.keys())

                        #########################################################################################################################
                        else:
                            """Etapa de utilização da biblioteca BeautifulSoup para tratamento das perguntas coletadas
                            """
                            print(dict_forms_products.keys())
                            #Dict auxiliar é criado a cada produto que é inserido no dicionário
                            dict_de_para_codigos = {1 : lista_perguntas[0],
                                                    2 : lista_perguntas[1],
                                                    4 : lista_perguntas[2],
                                                    5 : lista_perguntas[3],
                                                    6 : lista_perguntas[4],
                                                    16 : lista_perguntas[5],
                                                    18 : lista_perguntas[6],
                                                    23 : lista_perguntas[7],
                                                    32 : lista_perguntas[8],
                                                    36 : lista_perguntas[9],
                                                    38 : lista_perguntas[10],
                                                    39 : lista_perguntas[11],
                                                    44 : lista_perguntas[12],
                                                    49 : lista_perguntas[13],
                                                    51 : lista_perguntas[14]
                                                    }
                            
                            dict_respostas = dict()

                            #Resgatando a page HTML
                            forms = dict_forms_products[nome_produto]

                            #Definindo posição do subgrupo
                            pergunta_grupo = forms.find_all('survey-item-view')[5]

                            #Garantindo que o código não quebre se 5 estiver sem resposta
                            if 'visitada' in pergunta_grupo.find('span', attrs={'class' : 'md-caption ng-binding ng-hide'}).text.strip().lower():
                                #Definição de perguntas sem grupo e subgrupo
                                lista_perguntas_codigos = [1, 2, 4, 16, 18, 23, 32, 36, 38, 39, 44, 49, 51]
                                dict_de_para_codigos.pop(5)
                                dict_de_para_codigos.pop(6)

                            else:
                                for i in pergunta_grupo.find_all('div', attrs={'class' : 'ng-scope layout-align-start-center'}):
                                    if 'false' in str(i.find('md-icon', attrs={'aria-label' : 'radio_button_checked'})):
                                        pergunta_substituir = int(re.findall(r'\d+',i.find(string=re.compile('Grupo')).strip())[0]) + 5 
                                        # Tem que somar esse número mais 1 mais o número dessa pergunta que é 5 para chegar na prox.
                                        lista_perguntas[4] = "Subgrupo " + re.findall(r'\d+',i.find(string=re.compile('Grupo')).strip())[0] + ":"
                                        dict_de_para_codigos[pergunta_substituir] = dict_de_para_codigos.pop(6)
                                        dict_de_para_codigos[pergunta_substituir] = lista_perguntas[4] 
                                
                                #Definição de perguntas com grupo e subgrupo
                                lista_perguntas_codigos = [1, 2, 4, 5, pergunta_substituir, 16, 18, 23, 32, 36, 38, 39, 44, 49, 51]
                            
                            #Garantindo que o código não quebre se na 38 a resposta for NÃO
                            #Definindo posição do açúcar (38)
                            pergunta_acucar_ext = forms.find_all('survey-item-view')[38]
                            if 'Sim' in str(pergunta_acucar_ext.find('div', attrs={'class' : 'ng-scope layout-align-start-center'})):
                                checked_button_style = pergunta_acucar_ext.find('md-icon', attrs={'aria-label' : 'radio_button_checked'})

                                #Se marcar que não tem açúcar
                                if 'true' in str(checked_button_style):
                                    #Exclui a 39 da lista de perguntas
                                    lista_perguntas_codigos.remove(39)
                                    dict_de_para_codigos.pop(39)


                            #Loop de coletar respostas das perguntas
                            for cod_pergunta in lista_perguntas_codigos:
                                #IF para quando não são as perguntas com RADIO BUTTONS
                                if ( (cod_pergunta != 4) and (cod_pergunta != 38) and (cod_pergunta != 5) and 
                                    (cod_pergunta != 7) and (cod_pergunta != 8) and (cod_pergunta != 9) and
                                    (cod_pergunta != 10) and (cod_pergunta != 11) and (cod_pergunta != 12) and 
                                    (cod_pergunta != 13) and (cod_pergunta != 14) and (cod_pergunta != 15) 
                                    ):
                                    #Passar objeto da resposta
                                    pergunta_comum = forms.find_all('survey-item-view')[cod_pergunta]

                                    resposta_comum = [texto.text.strip() for texto in pergunta_comum.find_all('p')][1]

                                    dict_respostas[dict_de_para_codigos[cod_pergunta]] = resposta_comum
                                
                                #Se for a pergunta 4 com radio button
                                elif cod_pergunta == 4:
                                    pergunta_comum = forms.find_all('survey-item-view')[cod_pergunta]

                                    #Código para pergunta sobre consistência do alimento
                                    if 'Sólido' in str(pergunta_comum.find('div', attrs={'class' : 'ng-scope layout-align-start-center'})):
                                        checked_button_style = pergunta_comum.find('md-icon', attrs={'aria-label' : 'radio_button_checked'})

                                        if 'true' in str(checked_button_style):
                                            resposta_comum = 'Líquido'
                                        else:
                                            #Se o radio_button_checked (checked_button_style) for False é porque foi aquele opção que foi selecionada no forms.
                                            resposta_comum = 'Sólido'
                                    
                                    dict_respostas[dict_de_para_codigos[cod_pergunta]] = resposta_comum
                                
                                #Se for a pergunta 5 com radio button
                                elif cod_pergunta == 5:
                                    pergunta_comum = forms.find_all('survey-item-view')[cod_pergunta]

                                    #Avaliando qual foi o grupo marcado para o alimento
                                    for i in pergunta_comum.find_all('div', attrs={'class' : 'ng-scope layout-align-start-center'}):
                                        if 'false' in str(i.find('md-icon', attrs={'aria-label' : 'radio_button_checked'})):

                                            #Se foi o grupo 8 tem que ser tratado diferente pois tem uma tag 'span' entre o grupo e o texto
                                            if int(re.findall(r'\d+',i.find(string=re.compile('Grupo')).strip())[0]) == 8:

                                                for j in pergunta_comum.find_all('div', attrs={'class' : 'ng-scope layout-align-start-center'}):
                                                    if 'false' in str(j.find('md-icon', attrs={'aria-label' : 'radio_button_checked'})):
                                                        resposta_comum = [texto.text.strip() for texto in list(j.find('span'))[1]][0]
                                            
                                            else:
                                                lista_com_resposta_aux = [texto.text.strip() for texto in list(pergunta_comum.find('div', attrs={'class' : 'ng-scope layout-align-start-center'})\
                                                                                                                            .find('span', attrs={'class' : 'ng-binding'}))]
                                                resposta_comum = lista_com_resposta_aux[0].split('\xa0')[1]
                                    
                                    dict_respostas[dict_de_para_codigos[cod_pergunta]] = resposta_comum

                                #Se for a pergunta variável entre 7 e 15 com radio button
                                elif cod_pergunta == pergunta_substituir:
                                    pergunta_comum = forms.find_all('survey-item-view')[cod_pergunta]

                                    for i in pergunta_comum.find_all('div', attrs={'class' : 'ng-scope layout-align-start-center'}):

                                        if 'false' in str(i.find('md-icon', attrs={'aria-label' : 'radio_button_checked'})):
                                            resposta_comum = [texto.text.strip() for texto in list(i.find('span'))][0]
                                    
                                    dict_respostas[dict_de_para_codigos[cod_pergunta]] = resposta_comum
                                
                                #Se for a pergunta 38 do açúcar com radio button
                                elif cod_pergunta == 38:
                                    pergunta_comum = forms.find_all('survey-item-view')[cod_pergunta]

                                    if 'Sim' in str(pergunta_comum.find('div', attrs={'class' : 'ng-scope layout-align-start-center'})):
                                        checked_button_style = pergunta_comum.find('md-icon', attrs={'aria-label' : 'radio_button_checked'})

                                        #Se o radio_button_checked (checked_button_style) for False é porque foi aquele opção que foi selecionada no forms.
                                        if 'false' in str(checked_button_style):
                                            resposta_comum = 'Sim'
                                        else:
                                            resposta_comum = 'Não'
                                    
                                    #Adiciona as respostas das perguntas ao dicionário
                                    dict_respostas[dict_de_para_codigos[cod_pergunta]] = resposta_comum

                            
                            #Tem um problema no dicionário que ele está colocando os dados do último produto processo em todos os outros produtos anteriores
                            #Tem um problema na ordem do dict de-para que está colocando nomes errados nas informações
                            #Fora do segundo Loop atualiza o dicionário dos produtos 2 com um sub-dicionário com as respostas por pergunta
                            dict_forms_products_2[nome_produto] = dict_respostas

                            #A cada 20 produtos já passar para um dataframe e salvar como CSV
                            counter_product += 1
                            if (counter_product % 20) == 0:
                                df_temp = pd.DataFrame.from_dict(dict_forms_products_2, orient='index')
                                df_temp = df_temp.rename(columns={dict_de_para_codigos[pergunta_substituir] : 'Subgrupo do alimento'})
                                #Exporta o DataFrame
                                df_temp.to_csv(f"banco_dados_tcc_julia_produtos_numero_{counter_product - 20}_a_{counter_product}_{str(datetime.datetime.today().date()).replace('-', '')}_v11.csv",
                                            sep=';', encoding='ISO-8859-1', index=True
                                            )
                        
                        #Aperta em sair do forms
                        driver.find_element(By.XPATH, '//*[@id="header-viewer"]/div/button[3]').click()
                        esperar(8)
                        #Aperta em HOME
                        driver.find_element(By.XPATH, '//*[@id="home-menu"]/div/button').click()
                        esperar(15)
                        #Apertar em exibir todos
                        driver.find_element(By.XPATH, '/html/body/div[1]/div/div/otus-dashboard/div/otus-dashboard-home-display/md-content/div/div/div[1]/div/otus-participant-search/md-autocomplete/md-autocomplete-wrap/button').click()
                        esperar(10)

                        #Aumentar o limite de linhas para 500
                        limitador_linhas = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/otus-participants-manager-dashboard/div/div/otus-participants-list/md-content/md-content/div/dynamic-data-table/md-whiteframe/div[3]/div[3]/div[2]/div[2]')
                        esperar(3)
                        limitador_linhas.click()
                        esperar(3)
                        #Não esquecer de documentar porque usei uma forma ineficiente aqui
                        limitador_linhas.find_element(By.XPATH, '/html/body/div[5]/md-select-menu/md-content/md-option[6]').click()
                        esperar(15)
                        #Buscar caixa de pesquisa novamente
                        barrra_de_pesquisa = driver.find_element(By.XPATH, '//*[starts-with(@id, "input_")]')
                        esperar(10)
                        #Pesquisa item na barra novamente
                        barrra_de_pesquisa.send_keys(item)
                        #Aguarda
                        esperar(5)

####################Se de novo o forms não carregar volta a página e tenta acessar novamente ele
                    except:
                        driver.back()
                        esperar(10)
                        #Clickar no banco de dados
                        driver.find_element(By.XPATH, '//*[@id="activity0"]/figure/md-grid-tile-header/figcaption/div').click()
                        esperar(8)
                        try:
                            #Clickar no botão de visualizar atividade
                            driver.find_element(By.XPATH, '/html/body/div[1]/div/div/otus-participant-dashboard/div/div/otus-dashboard-display/div/otus-activity-manager/otus-activity-manager-bottom-sheet/md-bottom-sheet/div/button[2]').click()
                            esperar(10)
                            #Tentar puxar o formulário e correr o processo normal de extração e obtenção do itens relevantes
                            try:
                                #Pegar o forms em HTML com o BeautifulSoup
                                html_source_code_forms_product = driver.execute_script("return document.body.innerHTML;")
                                html_soup_forms_product = BeautifulSoup(html_source_code_forms_product, 'html.parser')
                                dict_forms_products[nome_produto] = html_soup_forms_product

                                #Lista de itens para verificar se pode excluir o produto já do dicionário
                                lista_perguntas_codigos_verificacao = [1, 2, 4, 16, 18, 23, 32, 36, 38, 39, 44, 49, 51]
                                lista_auxiliar_respostas = []
                                #Verificação de pergunta estar respondida
                                for codigo_pergunta in lista_perguntas_codigos_verificacao:
                                    #Passa a pergunta como objeto
                                    pergunta_aux = html_soup_forms_product.find_all('survey-item-view')[codigo_pergunta]
                                    reposta_aux = pergunta_aux.find('span', attrs={'class' : 'md-caption ng-binding ng-hide'}).text.strip().lower()
                                    lista_auxiliar_respostas.append(reposta_aux)
                                
                                esperar(5)
                                #Avalia se tem alguma pergunta só visitada na lista auxiliar
                                if 'visitada' in lista_auxiliar_respostas:
                                    dict_forms_products.pop(nome_produto)
                                    print(dict_forms_products.keys())

                                #########################################################################################################################
                                else:
                                    """Etapa de utilização da biblioteca BeautifulSoup para tratamento das perguntas coletadas
                                    """
                                    print(dict_forms_products.keys())
                                    #Dict auxiliar é criado a cada produto que é inserido no dicionário
                                    dict_de_para_codigos = {1 : lista_perguntas[0],
                                                            2 : lista_perguntas[1],
                                                            4 : lista_perguntas[2],
                                                            5 : lista_perguntas[3],
                                                            6 : lista_perguntas[4],
                                                            16 : lista_perguntas[5],
                                                            18 : lista_perguntas[6],
                                                            23 : lista_perguntas[7],
                                                            32 : lista_perguntas[8],
                                                            36 : lista_perguntas[9],
                                                            38 : lista_perguntas[10],
                                                            39 : lista_perguntas[11],
                                                            44 : lista_perguntas[12],
                                                            49 : lista_perguntas[13],
                                                            51 : lista_perguntas[14]
                                                            }
                                    
                                    dict_respostas = dict()

                                    #Resgatando a page HTML
                                    forms = dict_forms_products[nome_produto]

                                    #Definindo posição do subgrupo
                                    pergunta_grupo = forms.find_all('survey-item-view')[5]

                                    #Garantindo que o código não quebre se 5 estiver sem resposta
                                    if 'visitada' in pergunta_grupo.find('span', attrs={'class' : 'md-caption ng-binding ng-hide'}).text.strip().lower():
                                        #Definição de perguntas sem grupo e subgrupo
                                        lista_perguntas_codigos = [1, 2, 4, 16, 18, 23, 32, 36, 38, 39, 44, 49, 51]
                                        dict_de_para_codigos.pop(5)
                                        dict_de_para_codigos.pop(6)

                                    else:
                                        for i in pergunta_grupo.find_all('div', attrs={'class' : 'ng-scope layout-align-start-center'}):
                                            if 'false' in str(i.find('md-icon', attrs={'aria-label' : 'radio_button_checked'})):
                                                pergunta_substituir = int(re.findall(r'\d+',i.find(string=re.compile('Grupo')).strip())[0]) + 5 
                                                # Tem que somar esse número mais 1 mais o número dessa pergunta que é 5 para chegar na prox.
                                                lista_perguntas[4] = "Subgrupo " + re.findall(r'\d+',i.find(string=re.compile('Grupo')).strip())[0] + ":"
                                                dict_de_para_codigos[pergunta_substituir] = dict_de_para_codigos.pop(6)
                                                dict_de_para_codigos[pergunta_substituir] = lista_perguntas[4] 
                                        
                                        #Definição de perguntas com grupo e subgrupo
                                        lista_perguntas_codigos = [1, 2, 4, 5, pergunta_substituir, 16, 18, 23, 32, 36, 38, 39, 44, 49, 51]
                                    
                                    #Garantindo que o código não quebre se na 38 a resposta for NÃO
                                    #Definindo posição do açúcar (38)
                                    pergunta_acucar_ext = forms.find_all('survey-item-view')[38]
                                    if 'Sim' in str(pergunta_acucar_ext.find('div', attrs={'class' : 'ng-scope layout-align-start-center'})):
                                        checked_button_style = pergunta_acucar_ext.find('md-icon', attrs={'aria-label' : 'radio_button_checked'})

                                        #Se marcar que não tem açúcar
                                        if 'true' in str(checked_button_style):
                                            #Exclui a 39 da lista de perguntas
                                            lista_perguntas_codigos.remove(39)
                                            dict_de_para_codigos.pop(39)


                                    #Loop de coletar respostas das perguntas
                                    for cod_pergunta in lista_perguntas_codigos:
                                        #IF para quando não são as perguntas com RADIO BUTTONS
                                        if ( (cod_pergunta != 4) and (cod_pergunta != 38) and (cod_pergunta != 5) and 
                                            (cod_pergunta != 7) and (cod_pergunta != 8) and (cod_pergunta != 9) and
                                            (cod_pergunta != 10) and (cod_pergunta != 11) and (cod_pergunta != 12) and 
                                            (cod_pergunta != 13) and (cod_pergunta != 14) and (cod_pergunta != 15) 
                                            ):
                                            #Passar objeto da resposta
                                            pergunta_comum = forms.find_all('survey-item-view')[cod_pergunta]

                                            resposta_comum = [texto.text.strip() for texto in pergunta_comum.find_all('p')][1]

                                            dict_respostas[dict_de_para_codigos[cod_pergunta]] = resposta_comum
                                        
                                        #Se for a pergunta 4 com radio button
                                        elif cod_pergunta == 4:
                                            pergunta_comum = forms.find_all('survey-item-view')[cod_pergunta]

                                            #Código para pergunta sobre consistência do alimento
                                            if 'Sólido' in str(pergunta_comum.find('div', attrs={'class' : 'ng-scope layout-align-start-center'})):
                                                checked_button_style = pergunta_comum.find('md-icon', attrs={'aria-label' : 'radio_button_checked'})

                                                if 'true' in str(checked_button_style):
                                                    resposta_comum = 'Líquido'
                                                else:
                                                    #Se o radio_button_checked (checked_button_style) for False é porque foi aquele opção que foi selecionada no forms.
                                                    resposta_comum = 'Sólido'
                                            
                                            dict_respostas[dict_de_para_codigos[cod_pergunta]] = resposta_comum
                                        
                                        #Se for a pergunta 5 com radio button
                                        elif cod_pergunta == 5:
                                            pergunta_comum = forms.find_all('survey-item-view')[cod_pergunta]

                                            #Avaliando qual foi o grupo marcado para o alimento
                                            for i in pergunta_comum.find_all('div', attrs={'class' : 'ng-scope layout-align-start-center'}):
                                                if 'false' in str(i.find('md-icon', attrs={'aria-label' : 'radio_button_checked'})):

                                                    #Se foi o grupo 8 tem que ser tratado diferente pois tem uma tag 'span' entre o grupo e o texto
                                                    if int(re.findall(r'\d+',i.find(string=re.compile('Grupo')).strip())[0]) == 8:

                                                        for j in pergunta_comum.find_all('div', attrs={'class' : 'ng-scope layout-align-start-center'}):
                                                            if 'false' in str(j.find('md-icon', attrs={'aria-label' : 'radio_button_checked'})):
                                                                resposta_comum = [texto.text.strip() for texto in list(j.find('span'))[1]][0]
                                                    
                                                    else:
                                                        lista_com_resposta_aux = [texto.text.strip() for texto in list(pergunta_comum.find('div', attrs={'class' : 'ng-scope layout-align-start-center'})\
                                                                                                                                    .find('span', attrs={'class' : 'ng-binding'}))]
                                                        resposta_comum = lista_com_resposta_aux[0].split('\xa0')[1]
                                            
                                            dict_respostas[dict_de_para_codigos[cod_pergunta]] = resposta_comum

                                        #Se for a pergunta variável entre 7 e 15 com radio button
                                        elif cod_pergunta == pergunta_substituir:
                                            pergunta_comum = forms.find_all('survey-item-view')[cod_pergunta]

                                            for i in pergunta_comum.find_all('div', attrs={'class' : 'ng-scope layout-align-start-center'}):

                                                if 'false' in str(i.find('md-icon', attrs={'aria-label' : 'radio_button_checked'})):
                                                    resposta_comum = [texto.text.strip() for texto in list(i.find('span'))][0]
                                            
                                            dict_respostas[dict_de_para_codigos[cod_pergunta]] = resposta_comum
                                        
                                        #Se for a pergunta 38 do açúcar com radio button
                                        elif cod_pergunta == 38:
                                            pergunta_comum = forms.find_all('survey-item-view')[cod_pergunta]

                                            if 'Sim' in str(pergunta_comum.find('div', attrs={'class' : 'ng-scope layout-align-start-center'})):
                                                checked_button_style = pergunta_comum.find('md-icon', attrs={'aria-label' : 'radio_button_checked'})

                                                #Se o radio_button_checked (checked_button_style) for False é porque foi aquele opção que foi selecionada no forms.
                                                if 'false' in str(checked_button_style):
                                                    resposta_comum = 'Sim'
                                                else:
                                                    resposta_comum = 'Não'
                                            
                                            #Adiciona as respostas das perguntas ao dicionário
                                            dict_respostas[dict_de_para_codigos[cod_pergunta]] = resposta_comum

                                    
                                    #Tem um problema no dicionário que ele está colocando os dados do último produto processo em todos os outros produtos anteriores
                                    #Tem um problema na ordem do dict de-para que está colocando nomes errados nas informações
                                    #Fora do segundo Loop atualiza o dicionário dos produtos 2 com um sub-dicionário com as respostas por pergunta
                                    dict_forms_products_2[nome_produto] = dict_respostas

                                    #A cada 20 produtos já passar para um dataframe e salvar como CSV
                                    counter_product += 1
                                    if (counter_product % 20) == 0:
                                        df_temp = pd.DataFrame.from_dict(dict_forms_products_2, orient='index')
                                        df_temp = df_temp.rename(columns={dict_de_para_codigos[pergunta_substituir] : 'Subgrupo do alimento'})
                                        #Exporta o DataFrame
                                        df_temp.to_csv(f"banco_dados_tcc_julia_produtos_numero_{counter_product - 20}_a_{counter_product}_{str(datetime.datetime.today().date()).replace('-', '')}_v11.csv",
                                                    sep=';', encoding='ISO-8859-1', index=True
                                                    )
                                
                                #Aperta em sair do forms
                                driver.find_element(By.XPATH, '//*[@id="header-viewer"]/div/button[3]').click()
                                esperar(8)
                                #Aperta em HOME
                                driver.find_element(By.XPATH, '//*[@id="home-menu"]/div/button').click()
                                esperar(15)
                                #Apertar em exibir todos
                                driver.find_element(By.XPATH, '/html/body/div[1]/div/div/otus-dashboard/div/otus-dashboard-home-display/md-content/div/div/div[1]/div/otus-participant-search/md-autocomplete/md-autocomplete-wrap/button').click()
                                esperar(10)

                                #Aumentar o limite de linhas para 500
                                limitador_linhas = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/otus-participants-manager-dashboard/div/div/otus-participants-list/md-content/md-content/div/dynamic-data-table/md-whiteframe/div[3]/div[3]/div[2]/div[2]')
                                esperar(3)
                                limitador_linhas.click()
                                esperar(3)
                                #Não esquecer de documentar porque usei uma forma ineficiente aqui
                                limitador_linhas.find_element(By.XPATH, '/html/body/div[5]/md-select-menu/md-content/md-option[6]').click()
                                esperar(15)
                                #Buscar caixa de pesquisa novamente
                                barrra_de_pesquisa = driver.find_element(By.XPATH, '//*[starts-with(@id, "input_")]')
                                esperar(10)
                                #Pesquisa item na barra novamente
                                barrra_de_pesquisa.send_keys(item)
                                #Aguarda
                                esperar(5)
                            
                            #Se ainda assim não conseguir pula e vai pro próximo item
                            except:
                                driver.back()
                                esperar(10)
                                #Aperta em HOME
                                driver.find_element(By.XPATH, '//*[@id="home-menu"]/div/button').click()
                                esperar(15)
                                #Apertar em exibir todos
                                driver.find_element(By.XPATH, '/html/body/div[1]/div/div/otus-dashboard/div/otus-dashboard-home-display/md-content/div/div/div[1]/div/otus-participant-search/md-autocomplete/md-autocomplete-wrap/button').click()
                                esperar(10)

                                #Aumentar o limite de linhas para 500
                                limitador_linhas = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/otus-participants-manager-dashboard/div/div/otus-participants-list/md-content/md-content/div/dynamic-data-table/md-whiteframe/div[3]/div[3]/div[2]/div[2]')
                                esperar(3)
                                limitador_linhas.click()
                                esperar(3)
                                #Não esquecer de documentar porque usei uma forma ineficiente aqui
                                limitador_linhas.find_element(By.XPATH, '/html/body/div[5]/md-select-menu/md-content/md-option[6]').click()
                                esperar(15)
                                #Buscar caixa de pesquisa novamente
                                barrra_de_pesquisa = driver.find_element(By.XPATH, '//*[starts-with(@id, "input_")]')
                                esperar(10)
                                #Pesquisa item na barra novamente
                                barrra_de_pesquisa.send_keys(item)
                                #Aguarda
                                esperar(5)

########################Se não conseguir acessar nem o forms volta para a home
                        except:
                            #Aperta em HOME
                            driver.find_element(By.XPATH, '//*[@id="home-menu"]/div/button').click()
                            esperar(15)
                            #Apertar em exibir todos
                            driver.find_element(By.XPATH, '/html/body/div[1]/div/div/otus-dashboard/div/otus-dashboard-home-display/md-content/div/div/div[1]/div/otus-participant-search/md-autocomplete/md-autocomplete-wrap/button').click()
                            esperar(10)

                            #Aumentar o limite de linhas para 500
                            limitador_linhas = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/otus-participants-manager-dashboard/div/div/otus-participants-list/md-content/md-content/div/dynamic-data-table/md-whiteframe/div[3]/div[3]/div[2]/div[2]')
                            esperar(3)
                            limitador_linhas.click()
                            esperar(3)
                            #Não esquecer de documentar porque usei uma forma ineficiente aqui
                            limitador_linhas.find_element(By.XPATH, '/html/body/div[5]/md-select-menu/md-content/md-option[6]').click()
                            esperar(15)
                            #Buscar caixa de pesquisa novamente
                            barrra_de_pesquisa = driver.find_element(By.XPATH, '//*[starts-with(@id, "input_")]')
                            esperar(10)
                            #Pesquisa item na barra novamente
                            barrra_de_pesquisa.send_keys(item)
                            #Aguarda
                            esperar(5)


            except:
                #Aperta em HOME
                driver.find_element(By.XPATH, '//*[@id="home-menu"]/div/button').click()
                esperar(15)
                #Apertar em exibir todos
                driver.find_element(By.XPATH, '/html/body/div[1]/div/div/otus-dashboard/div/otus-dashboard-home-display/md-content/div/div/div[1]/div/otus-participant-search/md-autocomplete/md-autocomplete-wrap/button').click()
                esperar(10)

                #Aumentar o limite de linhas para 500
                limitador_linhas = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/otus-participants-manager-dashboard/div/div/otus-participants-list/md-content/md-content/div/dynamic-data-table/md-whiteframe/div[3]/div[3]/div[2]/div[2]')
                esperar(3)
                limitador_linhas.click()
                esperar(3)
                #Não esquecer de documentar porque usei uma forma ineficiente aqui
                limitador_linhas.find_element(By.XPATH, '/html/body/div[5]/md-select-menu/md-content/md-option[6]').click()
                esperar(15)
                #Buscar caixa de pesquisa novamente
                barrra_de_pesquisa = driver.find_element(By.XPATH, '//*[starts-with(@id, "input_")]')
                esperar(10)
                #Pesquisa item na barra novamente
                barrra_de_pesquisa.send_keys(item)
                #Aguarda
                esperar(5)

#Fechar automaticamente após o teste
driver.close()

#Printa a hora que terminou de rodar o código
print(datetime.datetime.now())



