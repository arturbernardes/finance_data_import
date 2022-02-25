import requests
from bs4 import BeautifulSoup

from datetime import datetime
from ticker_carteira import *

#import Threading           #TODO fazer multithreading

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

def busca_dy_acoes(soup, ticker, mostrar_dado = None):
    try:
        dado = soup.find('div', class_='info w-50 w-md-50 w-lg-20')
        if dado:
            dy = dado.find('strong', class_='value').get_text()
            if mostrar_dado == 1:
                print(ticker, ' - DY: ', dy)
            return dy
    except Exception as error:
        print('Erro ao buscar dado!')
        print(error)

def salvar_dados(dados):
    try:
        with open('dados_financeiros_python.csv', 'w') as csvfile:
            csvfile.write('Data da busca:'+datetime.today().strftime('%d-%m-%y')+'\n' +
                          'Ticker' + ';' + 'DY' + '\n')
            for dado in dados:
                csvfile.write(dado)
    except Exception as error:
        print('Erro ao salvar arquivo')
        print(error)


if __name__ == '__main__':
    info = []
    for ticker in ticker_acao:
        busca_codigo = requisicao_e_parsing(URL_ACOES+ticker)
        busca_dy = busca_dy_acoes(busca_codigo, ticker, 1)

        info.append(ticker + ';' + busca_dy + '\n')

    salvar_dados(info)
    print('Fim da busca')


