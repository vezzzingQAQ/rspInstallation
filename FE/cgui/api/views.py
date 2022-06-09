from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from client import client as vclient
from client import ipport


def sendCommand(request, state):
    CLIENT = vclient.VezClient()
    CLIENT.start(ipport.cmObj.send_to_ip, ipport.cmObj.send_to_port)
    CLIENT.send_message({"command": state})
    print(state)
    return JsonResponse({"state": "success"})
