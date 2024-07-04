# %%
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm  # Para ver quanto tempo demora

# %%
url_teste = "https://www.google.com"

resp_teste = requests.get(url_teste)
# %%
resp_teste.status_code

# %%
resp_teste.text

# %%
url = "https://www.residentevildatabase.com/personagens/ada-wong/"

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "referer": "https://www.residentevildatabase.com/personagens/",
    "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
}

resp = requests.get(url, headers=headers)

# %%
resp.status_code  # 200 de status code é igual sucesso

# %%
resp.text  # Irá te mostrar o código que roda o site (geralmente html)

# %%
soup = BeautifulSoup(resp.text)
soup

# %%
div_page = soup.find(
    "div", class_="td-page-content"
)  # buscar a parte que eu quero dentro do cod html
div_page

# %%
div_page.find_all("p")

# %%
paragrafo = div_page.find_all("p")[1]
paragrafo

# %%
ems = paragrafo.find_all("em")
ems
# %%
ems[0]

# %%
ems[0].text

# %%
data = dict()

for i in ems:
    chave, valor = i.text.split(":")
    chave = chave.strip()
    data[chave] = valor.strip()

data
# %%
data["Peso"]

# %%
data["Tipo sanguíneo"]


# %%
# Otimizando e automatizando o processo criando funções
def get_content(url):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "max-age=0",
        "priority": "u=0, i",
        "referer": "https://www.residentevildatabase.com/personagens/",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    }

    resp = requests.get(url, headers=headers)
    return resp


def get_basic_infos(soup):

    div_page = soup.find("div", class_="td-page-content")
    paragrafo = div_page.find_all("p")[1]
    ems = paragrafo.find_all("em")

    data = dict()
    for i in ems:
        chave, valor = i.text.split(":")
        chave = chave.strip()
        data[chave] = valor.strip()

    return data


# %%
# Aplicando funções

url = "https://www.residentevildatabase.com/personagens/alex-wesker/"

resp = get_content(url)

if resp.status_code != 200:
    print("Não foi possível obter os dados")
else:
    soup = BeautifulSoup(resp.text)
    get_basic_infos(soup)

# %%
# Encontrando o h4 com as aparições dos personagens
soup.find("div", class_="td-page-content").find("h4")

# %%
soup.find("div", class_="td-page-content").find("h4").find_next()
# Passa o proximo tipo de objeto que existe, que nesse caso é uma lista não numerada

# %%
lis = soup.find("div", class_="td-page-content").find("h4").find_next().find_all("li")
lis

# %%
lis[0]

# %%
lis[0].text

# %%
aparicoes = [i.text for i in lis]
aparicoes


# %%
def get_aparicoes(soup):

    lis = (
        soup.find("div", class_="td-page-content").find("h4").find_next().find_all("li")
    )
    aparicoes = [i.text for i in lis]

    return aparicoes


# %%
url = "https://www.residentevildatabase.com/personagens/alex-wesker/"

resp = get_content(url)

if resp.status_code != 200:
    print("Não foi possível obter os dados")
else:
    soup = BeautifulSoup(resp.text)
    data = get_basic_infos(soup)
    data["Aparições"] = get_aparicoes(soup)
    data
# %%
data


# %%
def get_personagem(url):

    resp = get_content(url)
    if resp.status_code != 200:
        print("Não foi possível obter os dados")
        return {}
    else:
        soup = BeautifulSoup(resp.text)
        data = get_basic_infos(soup)
        data["Aparições"] = get_aparicoes(soup)
        return data


# %%
url = "https://www.residentevildatabase.com/personagens/ada-wong/"
get_personagem(url)


# %%
# Agora utilizando para pegar todos os personagens
def get_content(url):
    # Tirando o header para tronar o header uma variavel global
    # para não rodar toda vez que a função for chamada, assim otimizando o codigo
    resp = requests.get(url, headers=headers)
    return resp


# %%
url = "https://www.residentevildatabase.com/personagens/"

resp = requests.get(url, headers=headers)
soup_personagem = BeautifulSoup(resp.text)
ancoras = soup_personagem.find("div", class_="td-page-content").find_all("a")
ancoras
# %%
for i in ancoras:
    print(i["href"])

# %%
links = [i["href"] for i in ancoras]
links


# %%
def get_links():

    url = "https://www.residentevildatabase.com/personagens/"
    resp = requests.get(url, headers=headers)
    soup_personagem = BeautifulSoup(resp.text)
    ancoras = soup_personagem.find("div", class_="td-page-content").find_all("a")

    links = [i["href"] for i in ancoras]
    return links
