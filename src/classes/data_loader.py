import pandas as pd
import json

def singleton(cls):
    instances = {}
    
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper


@singleton
class DataLoader:

    def __init__(self, urls : dict):
        self._data_holder = dict(zip(list(urls.keys()), [self._auto_loader(url) for url in urls.values()]))

    def _auto_loader(self, url : str):
        if '.csv' in url:
            return pd.read_csv(url)
        if '.json' in url:
            file = open(url, "r", encoding="utf-8")
            return json.load(file)

    @property
    def holder(self):
        return self._data_holder
    
    def append(self, name : str, url : str):
        self._data_holder[name] = self._auto_loader(url)