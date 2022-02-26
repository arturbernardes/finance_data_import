from ticker_pessoal import *

from datetime import datetime
from bs4 import BeautifulSoup

import threading
import requests


INFO_ACOES = []
INFO_FIIS = []
THREADS_LIST = []


def requisicao_e_parsing(URL):
    try:
        requisicao_dominio = requests.get(URL)
        try:
            soup_dominio = BeautifulSoup(requisicao_dominio.text, 'html.parser')
            return soup_dominio
        except Exception as error1:
            print('Erro de Parsing')
            print(error1)
    except Exception as error:
        print('Erro de Requisição')
        print(error)


def busca_dy_acoes():
    while True:
        try:
            ticker = ticker_acao.pop(0)
        except Exception as error:
            break

        try:
            soup = requisicao_e_parsing(URL_ACOES + ticker)
            dado = soup.find('div', class_='info w-50 w-md-50 w-lg-20')
            if dado:
                dy = dado.find('strong', class_='value').get_text()
                INFO_ACOES.append(ticker + ';' + dy + '\n')
        except Exception as error:
            print('Erro ao buscar dado!')
            print(error)


def busca_dy_FIIS():
    while True:
        try:
            ticker = ticker_fii.pop(0)
        except Exception as error:
            return

        try:
            soup = requisicao_e_parsing(URL_FIIS + ticker)
            dado = soup.find('div', class_='info w-50 w-lg-20')
            if dado:
                dy = dado.find('strong', class_='value').get_text()
                INFO_FIIS.append(ticker + ';' + dy + '\n')
        except Exception as error:
            print('Erro ao buscar dado!')
            print(error)


def salvar_dados(dados, tipo_dado):
    try:
        with open('dados_'+tipo_dado+'.csv', 'w') as csvfile:
            csvfile.write('Ticker' + ';' + 'DY' + '\n')
            for dado in dados:
                csvfile.write(dado)
    except Exception as error:
        print('Erro ao salvar arquivo')
        print(error)


if __name__ == '__main__':
    quantidade_thread = 10
    print('Buscando DY')
    for i in range(quantidade_thread):
        t = threading.Thread(target=busca_dy_acoes)
        j = threading.Thread(target=busca_dy_FIIS)
        THREADS_LIST.append(t)
        THREADS_LIST.append(j)

    for t in THREADS_LIST:
        t.start()

    for t in THREADS_LIST:
        t.join()

    print('Salvando dados')
    salvar_dados(INFO_ACOES, 'acoes')
    salvar_dados(INFO_FIIS, 'FIIs')

