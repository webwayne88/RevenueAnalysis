from fastapi import FastAPI, File, UploadFile, HTTPException
import zipfile
from llm_model.ask_llm import get_llm_answer
from process_zip import process_zip_file
from pydantic import BaseModel
import zipfile
from io import BytesIO


class AnalysisRequest(BaseModel):
    data: dict 

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Сервис анализа выручки работает!"}


@app.post("/process_zip", summary="Обработка ZIP-архива")
async def process_zip(file: UploadFile = File(...)):
    try:
        result = process_zip_file(BytesIO(await file.read()))
        return dict(sorted(result.items(), key=lambda x: x[0]))
    except zipfile.BadZipFile:
        raise HTTPException(
            status_code=400,
            detail="Некорректный ZIP-архив"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка обработки файла: {str(e)}"
        )


@app.post("/get-analysis", summary="Получение отчета")
async def get_analysis(request: AnalysisRequest):
    try:
        return get_llm_answer(request)  
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Произошла ошибка при анализе данных: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", reload=True)
        

