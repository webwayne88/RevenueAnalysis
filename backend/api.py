from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from io import BytesIO
import zipfile

from llm.pipeline import get_llm_answer
from utils import process_zip_file


class Analysis(BaseModel):
    revenue_data: dict
    llm_response: dict

app = FastAPI() 

@app.post("/analyze", response_model=Analysis)
async def analyze(file: UploadFile = File(...)):
    try: 
        file_processing_result = process_zip_file(BytesIO(await file.read()))
        file_processing_result = dict(sorted(file_processing_result.items(), key=lambda x: x[0]))
        llm_answer = get_llm_answer(file_processing_result)   
        return {
            "revenue_data": file_processing_result,
            "llm_response": llm_answer
        }  
        
    except zipfile.BadZipFile as e:
        raise HTTPException(
            status_code=400,
            detail="Некорректный ZIP-архив"  + str(e)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка обработки запроса: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", reload=True)
        

