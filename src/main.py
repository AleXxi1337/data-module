from fastapi import FastAPI, HTTPException
from classes.data_loader import DataLoader
from classes.data_generator import DataGenerator
import pandas as pd

app = FastAPI()

# Инициализация загрузчика с примером URL
urls = {
    "data": "/data/data.csv"
}

dl = DataLoader(urls)

DataGenerator.generate_for_valudation(df=dl.holder['data'], column='Название', save_file='/data/programs.json')
dl.append('programs', '/data/programs.json')

DataGenerator.generate_for_valudation(df=dl.holder['data'], save_file='/data/columns.json')
dl.append('columns', '/data/columns.json')

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