import json
from classes.preprocess_data import preprocess
import pandas as pd


class DataGenerator:

    @staticmethod
    def generate_for_valudation(df : pd.DataFrame, save_file : str, column : str = None):
        
        if column != None:
            values = list(df[column])
        else:
            values = list(df.columns)

        dictionary = dict(zip([i for i in df.index], [preprocess(v) for v in values]))

        with open(save_file, 'w', encoding='utf-8') as file:
            json.dump(dictionary, file, ensure_ascii=False)