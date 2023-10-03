import os
import requests
import config


api_host = 'https://api.stability.ai'
api_key = -


def getModelList():
    url = f"{api_host}/v1/engines/list"
    response = requests.get(url, headers={"Authorization": f"Bearer {api_key}"})

    if response.status_code == 200:
        payload = response.json()
        print("Success")
        print(payload)
    else:
        print(response.status_code)
        print(response.text)

getModelList()

