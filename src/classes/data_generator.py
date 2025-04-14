import json
from classes.preprocess_data import preprocess
import pandas as pd
from classes.embeddings_generator import EmbeddingGenerator


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

    @staticmethod
    def generate_for_classification(df : pd.DataFrame, embenddigs_generator : EmbeddingGenerator, embeddigs_column : str, save_file : str, additional_columns : dict = None):

        embeddigs = embenddigs_generator.generate(df[embeddigs_column].to_list())
        embeddigs_list = embenddigs_generator.embeddings_to_list(embeddigs)
        
        keys = ['embenddings']
        values = [embeddigs_list]

        if additional_columns != None:
            keys += list(additional_columns.keys())
            values += [df[column].to_list() for column in additional_columns.values()]

        dictionary = dict(zip(keys, values))

        with open(save_file, 'w', encoding='utf-8') as file:
            json.dump(dictionary, file, ensure_ascii=False)