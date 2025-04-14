from classes.embeddings_generator import EmbeddingGenerator
from classes.data_generator import DataGenerator
import pandas as pd


df = pd.DataFrame(
    [{'А' : 'абобус', 'Б' : 'билибоба'},
    {'А' : 'иди нахуй', 'Б' : 'лох'},
    {'А' : 'в пизду', 'Б' : 'ебаный'},
    {'А' : 'соси', 'Б' : 'негр'}]
)

eg = EmbeddingGenerator()
DataGenerator.generate_for_classification(df, eg, 'А', 'data/pososi.json', {'b' : 'Б'})