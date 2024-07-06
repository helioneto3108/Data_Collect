# %%
import requests
import pandas as pd
import datetime
import time
import json


# %%
def get_response(**kwargs):
    url = "https://www.tabnews.com.br/api/v1/contents"
    resp = requests.get(url, params=kwargs)
    return resp


def save_data(data, option="json"):

    now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")

    if option == "json":
        with open(f"data/contents/json/{now}.json", "w") as open_file:
            json.dump(data, open_file, indent=4)

    elif option == "parquet":
        df = pd.DataFrame(data)
        df.to_parquet(f"data/contents/parquet/{now}.parquet", index=False)


# %%
# Automatizando o processo de coleta
page = 1
while True:
    print(page)  # Para saber onde estamos
    resp = get_response(page=page, per_page=100, strategy="new")

    if resp.status_code == 200:
        data = resp.json()
        save_data(data)
        time.sleep(
            2
        )  # Para não ficar requisitando muito dado, senão o servidor trava e da status code == 429
        page += 1

        if len(data) < 100:
            break

    else:
        print(resp.status_code)  # Para ver o numero do erro que está dando
        print(resp.json())  # Para ver o erro que está dando em detalhe
        time.sleep(60 * 5)  # Para dar tempo de relizar outro request

# Uma boa prática aqui seria colocar um contador de falhas
# no else e colocar um condição or no break para parar depois de certo ponto
# %%
# Tratamento de data para possivel filtro
date = "2024-06-10T12:55:09.099Z"
pd.to_datetime(date)
# %%
date = pd.to_datetime(date).date()
date

# %%
# Fazendo agora com um criterio de parada
# Agora pegara os arquivos que foram atualizado depois de 2024
page = 1
data_stop = pd.to_datetime("2024-01-01").date()
while True:
    print(page)  # Para saber onde estamos
    resp = get_response(page=page, per_page=100, strategy="new")

    if resp.status_code == 200:
        data = resp.json()
        save_data(data)
        time.sleep(2)
        page += 1

        date = pd.to_datetime(data[-1]["updated_at"]).date()
        if len(data) < 100 or date < data_stop:
            break

    else:
        print(resp.status_code)  # Para ver o numero do erro que está dando
        print(resp.json())  # Para ver o erro que está dando em detalhe
        time.sleep(60 * 5)  # Para dar tempo de relizar outro request

# %%
