# Variável global para guardar as informações coletadas #
data = {
    "Resolucao" : [],
    "Empresa" : [],
    "Autorizacao" : [],
    "Marca" : [],
    "Processo" : [],
    "Registro" : [],
    "Venda e Emprego" : [],
    "Vencimento" : [],
    "Apresentacao" : [],
    "Validade Produto" : [],
    "Categoria" : [],
    "Assunto Peticao" : [],
    "Expediente Peticao" : [],
    "Versao" : []
}

def get_links(url_pesquisa):
    """
    Retorna uma lista com os links das páginas das publicações resultante de uma url de pesquisa.
    Utiliza as bibliotecas Selenium e BeautifulSoup.
    Para a biblioteca Selenium foi utilizado o navegador Chrome.
    """
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.chrome.options import Options  
    from bs4 import BeautifulSoup
    import time

    # Definindo driver do Selenium utilizando o Chrome #
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)
    wait = WebDriverWait(driver, 30)

    # Realizando acesso à url de pesquisa #
    driver.get(url_pesquisa)
    time.sleep(.5)

    # Acessando html relacionado aos links das publicações resultantes do link de pesquisa #
    container = driver.find_element_by_id("_br_com_seatecnologia_in_buscadou_BuscaDouPortlet_hierarchy_content").get_attribute('innerHTML')
    soup = BeautifulSoup(container, 'html.parser')

    # Identificando cada link de publicaçao #
    links = []
    for link in soup.find_all('a', href=True):
        links.append(link['href'])

    return links

def app_new_null_data(resolucao):
    """
    Adiciona um registo em data para um saneante inicialmente sem dados
    """
    global data

    data["Resolucao"].append(resolucao)
    data["Empresa"].append('')
    data["Autorizacao"].append('')
    data["Marca"].append('')
    data["Processo"].append('')
    data["Registro"].append('')
    data["Venda e Emprego"].append('')
    data["Vencimento"].append('')
    data["Apresentacao"].append('')
    data["Validade Produto"].append('')
    data["Categoria"].append('')
    data["Assunto Peticao"].append('')
    data["Expediente Peticao"].append('')
    data["Versao"].append('')

def collect_data(publicacoes):
    """
    Coleta os dados das páginas de publicações passadas como parâmetro.
    Registra os dados coletados na variável global.
    Utiliza as bibliotecas Requests e BeautifulSoup
    """
    from requests import get
    from bs4 import BeautifulSoup

    global data

    for publicacao in publicacoes:

        url = 'https://www.in.gov.br'

        print("Coletanto dados de " + url + str(publicacao))

        # Acessando publicação #
        response = get(url+str(publicacao))
        soup = BeautifulSoup(response.text, 'html.parser')
        anexo = soup.find('div', class_ = 'texto-dou')

        # Coletando a resoluçao referente à publicação #
        resolucao = anexo.find('p', class_ = 'identifica').text

        # Separando o texto para coleta dos dados #
        texto = anexo.find_all('p', class_ = 'dou-paragraph')

        # Coletando os dados #
        app_new_null_data(resolucao)
        for line in texto:

            line_splitted = line.text.split(':')

            if line_splitted[0] == 'NOME DA EMPRESA':
                data["Empresa"].pop()
                data["Empresa"].append(line_splitted[1])
            elif line_splitted[0] == 'AUTORIZAÇÃO':
                data["Autorizacao"].pop()
                data["Autorizacao"].append(line_splitted[1])
            elif line_splitted[0] == 'NOME DO PRODUTO E MARCA':
                data["Marca"].pop()
                data["Marca"].append(line_splitted[1])
            elif line_splitted[0] == 'NUMERO DE PROCESSO':
                data["Processo"].pop()
                data["Processo"].append(line_splitted[1])
            elif line_splitted[0] == 'NUMERO DE REGISTRO':
                data["Registro"].pop()
                data["Registro"].append(line_splitted[1])
            elif line_splitted[0] == 'VENDA E EMPREGO':
                data["Venda e Emprego"].pop()
                data["Venda e Emprego"].append(line_splitted[1])
            elif line_splitted[0] == 'VENCIMENTO':
                data["Vencimento"].pop()
                data["Vencimento"].append(line_splitted[1])
            elif line_splitted[0] == 'APRESENTAÇÃO':
                data["Apresentacao"].pop()
                data["Apresentacao"].append(line_splitted[1])
            elif line_splitted[0] == 'VALIDADE DO PRODUTO':
                data["Validade Produto"].pop()
                data["Validade Produto"].append(line_splitted[1])
            elif line_splitted[0] == 'CATEGORIA':
                data["Categoria"].pop()
                data["Categoria"].append(line_splitted[1])
            elif line_splitted[0] == 'ASSUNTO DA PETIÇÃO':
                data["Assunto Peticao"].pop()
                data["Assunto Peticao"].append(line_splitted[1])
            elif line_splitted[0] == 'EXPEDIENTE DA PETIÇÃO':
                data["Expediente Peticao"].pop()
                data["Expediente Peticao"].append(line_splitted[1])
            elif line_splitted[0] == 'VERSÃO':
                data["Versao"].pop()
                data["Versao"].append(line_splitted[1])
            elif line_splitted[0][0] == '_': app_new_null_data(resolucao)

def to_excel(arqivo='resultado'):
    """
    Grava os dados coletados em um arquivo excel (.xlsx).
    Parâmetros
    ---------
    arqivo: str
        caminho e/ou nome do arquivo de escrita dos dados (sem extensão).
        default: 'resultado'
    """
    import pandas as pd
    global data

    df = pd.DataFrame(data) # Transfomando os dados em dataframe #
    df.to_excel(arqivo+'.xlsx') # Gravando os dados em arquivo excel #

def main():

    # Definindo url de busca de publicações #
    url_inicial = 'https://www.in.gov.br/consulta/-/buscar/dou?q="deferir+os+registros+e+as+petições+dos+produtos+saneantes"&s=todos&exactDate=personalizado&sortType=0&publishFrom=01-05-2021&publishTo=30-06-2021'
    
    # Obtendo os links das publicações resultantes da busca #
    links_publicacoes = get_links(url_inicial)

    # Coletando os dados das publicações #
    collect_data(links_publicacoes)

    # Gravando dados em planilha excel #
    to_excel()

if __name__ == "__main__":
    main()