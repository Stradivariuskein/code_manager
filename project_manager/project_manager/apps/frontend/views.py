from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import os 
import requests
import json


def Dashboard(request):
    # Datos que quieres enviar en la solicitud POST
    # url = "https://192.168.2.115:9443/api/auth"
    # data = {
    #     'Username': 'mrkein',
    #     'Password': '38996049Alan@#$'
    # }

    # Cabeceras de la solicitud, si es necesario (por ejemplo, para indicar que los datos están en formato JSON)
    # headers = {
    #     'Content-Type': 'application/json'
    # }

    # Enviar la solicitud POST
    # response = requests.post(url, json=data, headers=headers, verify=False)
    portainertoken = "ptr_Mju7Q8S4eFxajVW2KQPTsvFJ5ycHD168P7PnfRNitKQ="
    url = "https://192.168.2.115:9443/api/endpoints/2/docker/containers/json"
    headers = {
        "X-API-Key":portainertoken,
        "all":"true"
    }
    
    response = requests.get(url, headers=headers, verify=False)
    data = response.content
    
    dic_data = json.loads(data)
    len_dic = len(dic_data)
    for container in dic_data:

        for key, content in container.items():
            print(f"########################################\n{key}\n{content}")
        print("#################################################################")

    return render(request,"dashboard.html", {"response": response})

