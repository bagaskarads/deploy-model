import uvicorn
from enum import Enum
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Path, Query
import tensorflow as tf
import numpy as np
import os
from google.oauth2 import service_account
from google.cloud import storage
from config import get_config

with open("service_account.json", "w") as file:
    file.write(json_svc_account)

credentials = service_account.Credentials.from_service_account_file(
    "./service_account.json"
)

gcs = storage.Client(credentials=credentials)

# URL of the image to be downloaded is defined as image_url
app = FastAPI()  # create a new FastAPI app instance

# Define a Pydantic model for an item


class Item(BaseModel):
    sl: float
    sw: float
    pl: float
    pw: float


model_url = "https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"
model = tf.keras.models.load_model('./model/somethingidk.h5')


def predict(sl, sw, pl, pw):
    # sl = 5.8
    # sw = 2.6
    # pl = 4.0
    # pw = 1.2
    # should output 'Iris-versicolor'

    resmessage = "undefined"
    temp = np.array([[sl, sw, pl, pw]])
    result = model.predict(temp)
    clas = np.argmax(result)

    if (clas == 0):
        resmessage = "Iris-setosa"
    elif (clas == 1):
        resmessage = "Iris-versicolor"
    elif (clas == 2):
        resmessage = "Iris-virginica"
    else:
        resmessage = "undefined"

    return resmessage


@app.get("/")
def hello_world():
    return ("hello world")


@app.post("/")
def add_item(item: Item):
    result = predict(item.sl, item.sw, item.pl, item.pw)
    return {result}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=port, timeout_keep_alive=1200)
