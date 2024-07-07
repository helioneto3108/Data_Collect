# %%
import requests
import datetime
import json
import time
import pandas as pd


# %%
class collector:

    def __init__(self, url, instance_name) -> None:
        self.url = url
        self.instance_name = instance_name

    def get_content(self, **kwargs):

        resp = requests.get(self.url, params=kwargs)
        return resp

    def save_parquet(self, data):

        now = datetime.datetime.now().strftime("%Y%m%d_%H:%M%S.%f")

        df = pd.DataFrame(data)
        df.to_parquet(f"data/{self.instance_name}/parquet/{now}.json", index=False)

    def save_json(self, data):

        now = datetime.datetime.now().strftime("%Y%m%d_%H:%M%S.%f")

        with open(f"data/{self.instance_name}/json/{now}.json", "w") as open_file:
            json.dump(data, open_file)

    def save_data(self, data, format="json"):

        if format == "json":
            self.save_json(data)

        elif format == "parquet":
            self.save_parquet(data)

    def get_and_save(self, save_format="json", **kwargs):

        resp = self.get_content(**kwargs)

        if resp.status_code == 200:
            self.save_data(resp.json(), save_format)

        else:
            print(f"Request sem sucesso: {resp.status_code}", resp.json())


# %%

url = "https://api.jovemnerd.com.br/wp-json/jovemnerd/v1/nerdcasts/"

collect = collector(url, "episodios")
# %%
collect.get_content()
# %%
collect.get_content().json()
# %%
collect.get_and_save()

# %%
