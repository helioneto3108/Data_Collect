# %%
import requests
import pandas as pd
import datetime
import json

# %%
url = "https://www.tabnews.com.br/api/v1/contents"

resp = requests.get(url)
resp.status_code
# %%
resp.text
# Não é muito bom utilizar em caso de API, pois o conteudo vem menos estruturado
# %%
resp.json()
# Para puxar a API com dados mais estruturados
# %%
data = resp.json()
data
# %%
type(data)
# %%
data[0]
# %%
len(data)
# Dara o quanto esse resultado da API está me trazendo de valores
# Nesse caso estamos pegando de 30 e 30
# %%
url = "https://www.tabnews.com.br/api/v1/contents/?page=2"
# Agroa com essa url ele me trará os proximos 30 conteudos
# OBS: Casa url irá depender de como a API foi desenvolvida
# Ou seja, tem que olhar na documentação da API para aprender a fazer essas chamadas


# %%
# Fazendo um função para puxar a listas de conteudos
def get_response(**kwargs):
    url = "https://www.tabnews.com.br/api/v1/contents"
    resp = requests.get(url, params=kwargs)
    return resp


# **kwargs voce está passando uma quantidade infinita de parametros que não necessariamente são obrigatórios
# Os argumento parms da função get são os mesmo parametros que vc coloca na url como por exemplo ?page=2&per_page=100
# %%
resp = get_response(page=1, per_page=100, strategy="new")
resp.json()

# %%
resp = get_response(page=2, per_page=100, strategy="new")
resp.json()


# %%
# Criando função para salvar os dados
def save_data(data, option="json"):

    now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")

    if option == "json":
        with open(f"data/contents/json/{now}.json", "w") as open_file:
            json.dump(data, open_file, indent=4)
            # json.dump é para pegar o dado (data nesse caso) e jogar no arquivo json
            # ident é a indentação
            # with é utilizado para abrir e fechar o arquivo (BOAS PRÁTICAS)

    elif option == "parquet":
        df = pd.DataFrame(data)
        df.to_parquet(f"data/contents/parquet/{now}.parquet", index=False)


# %%
resp = get_response(page=1, per_page=100, strategy="new")
if resp.status_code == 200:
    print("SUCESSO!")

# %%
data = resp.json()
data

# %%
save_data(data)
# %%
save_data(data, option="parquet")
# %%
