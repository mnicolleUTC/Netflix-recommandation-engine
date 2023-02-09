import mlflow 
import uvicorn
import pandas as pd 
from pydantic import BaseModel
from typing import Literal, List, Union
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import RedirectResponse

description = """
This Netflix API allows you to make recommandations of movies for a given user.

## Get_Reco

Where you can: 
* `/load` the best matches for given user
"""

tags_metadata = [
    {
        "name": "Predictions",
        "description": "Use this endpoint for getting predictions"
    }
]

app = FastAPI(
    title="👨‍💼 API_Netflix_Reco",
    description=description,
    version="0.1",
    openapi_tags=tags_metadata
)

@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')


@app.get("/load", tags=["Load"])
async def load_reco(rows: int=10):
    """
    Get a sample of your whole dataset. 
    You can specify how many movies you want by specifying a value for `rows`, default is `10`
    """
    df = pd.read_csv("https://netflix-recommandation.s3.eu-west-3.amazonaws.com/sample.csv")
    sample = df.sample(rows)
    return sample.to_json()


if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000) # Here you define your web server to run the `app` variable (which contains FastAPI instance), with a specific host IP (0.0.0.0) and port (4000)