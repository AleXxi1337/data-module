from pydantic import BaseModel

# Модель для запроса обработки текста
class TextRequest(BaseModel):
    text: str

class CSVGetCell(BaseModel):
    dataset: str
    col: int
    row: int

class CSVGetColumn(BaseModel):
    dataset: str
    col: int