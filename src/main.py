from fastapi import FastAPI, HTTPException
from classes.data_loader import DataLoader
from classes.data_generator import DataGenerator
import pandas as pd
from src.models import *
from classes.preprocess_data import preprocess
from classes.embeddings_generator import EmbeddingGenerator
from classes.embeddings_filter import embeddings_filter


eg = EmbeddingGenerator()


# Инициализация загрузчика с примером URL
urls = {
    "data": "/data/data.csv"
}

dl = DataLoader(urls)

DataGenerator.generate_for_valudation(df=dl.holder['data'], column='Название', save_file='/data/programs.json')
dl.append('programs', '/data/programs.json')

DataGenerator.generate_for_valudation(df=dl.holder['data'], save_file='/data/columns.json')
dl.append('columns', '/data/columns.json')

DataGenerator.generate_for_classification(df=dl.holder['data'], embenddigs_generator=eg, embeddigs_column='Основная информация', additional_columns={'degree' : 'Степень'}, save_file='/data/embeddings.json')
dl.append('embeddings', '/data/embeddings.json')

app = FastAPI()

@app.get("/data/{dataset_name}")
async def get_dataset(dataset_name: str):
    """Получить данные по имени набора"""
    data = dl.holder.get(dataset_name)
    
    if data is None:
        raise HTTPException(
            status_code=404,
            detail=f"Dataset '{dataset_name}' not found"
        )
    
    # Конвертируем DataFrame в словарь для JSON-ответа
    if isinstance(data, pd.DataFrame):
        return data.to_dict(orient="records")
    
    return data

@app.get("/datasets")
async def list_datasets():
    """Получить список доступных наборов данных"""
    return {
        "available_datasets": list(dl.holder.keys())
    }

@app.post("/preprocess-text/")
async def process_text(request: TextRequest):
    """Эндпоинт для предобработки текста"""
    processed_text = preprocess(request.text)
    return {
        "result": processed_text
    }

@app.post("/get-cell/")
async def get_cell(request: CSVGetCell):
    """Эндпоинт для значения ячейки"""
    return {
        "cell": dl.holder[request.dataset].iloc[request.row, request.col]
    }

@app.post("/get-column/")
async def get_cell(request: CSVGetColumn):
    """Эндпоинт для имени колонки"""
    return {
        "column": list(dl.holder[request.dataset].columns)[request.col]
    }

@app.post("/get-sliced-embeddigs/")
async def get_sliced_embeddings(request: EmbeddigsGet):
    return embeddings_filter(dl.holder['embeddings'], request.filters)