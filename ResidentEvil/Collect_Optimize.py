# %%
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm  # Para ver quanto tempo demora
import pandas as pd

# %%
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


def get_content(url):
    # Tirando o header para tronar o header uma variavel global
    # para não rodar toda vez que a função for chamada, assim otimizando o codigo
    resp = requests.get(url, headers=headers)
    return resp


def get_basic_infos(soup):

    div_page = soup.find("div", class_="td-page-content")
    paragrafo = div_page.find_all("p")[1]
    ems = paragrafo.find_all("em")

    data = dict()
    for i in ems:
        chave, valor, *_ = i.text.split(":")
        # *_ -> Serve para ignorar todo o resto (desempacotamento de listas)
        chave = chave.strip()
        data[chave] = valor.strip()

    return data


def get_aparicoes(soup):

    lis = (
        soup.find("div", class_="td-page-content").find("h4").find_next().find_all("li")
    )
    aparicoes = [i.text for i in lis]

    return aparicoes


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


def get_links():

    url = "https://www.residentevildatabase.com/personagens/"
    resp = requests.get(url, headers=headers)
    soup_personagem = BeautifulSoup(resp.text)
    ancoras = soup_personagem.find("div", class_="td-page-content").find_all("a")

    links = [i["href"] for i in ancoras]
    return links


# %%
links = get_links()

data = []
for i in tqdm(links):
    d = get_personagem(i)
    d["Links"] = i
    nome = i.strip("/").split("/")[-1].replace("-", " ").title()
    d["Nome"] = nome
    data.append(d)

# %%
df = pd.DataFrame(data)
df

# %%
df[~df["de nascimento"].isna()]

# %%
# Salvando o DataFrame
df.to_parquet("dados_re.parquet", index=False)
# Parquet é melhor pois ele armazena metadados
# Por ser um arquivo Binário, ou seja, preserva melhor a estrutura de dados complexos como listas
# %%
df.to_csv("dados_re.csv", index=False, sep=";")
# Arquivo de texto, não muito bom para armazenar estruturas complexas de dados
# %%
df.to_pickle("dados_re.pkl")
# Também é binário, porem ficar maior que o parquet
# Serialização de objetos
# Bom para preservar o tipo de dados (df continuara df)
# Pegar um objeto em python e salva em disco
# Bom para salvar modelo de ML
# Preserva bem a estrutura de dados
# %%
