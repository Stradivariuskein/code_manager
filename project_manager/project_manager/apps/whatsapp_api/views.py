from django.shortcuts import render , HttpResponse

import requests
import project_manager.settings as settings
import random
import string

from .models import WhatsappSession, WhatsappApi

# manda el token como sengundo factor de autenticacion
def send_token(request):
    def generate_token(length=6):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choices(characters, k=length))
    # label = "BOT:"
    # headers = {"x-api-key": settings.WHASTAPP_API_KEY}
    # token = generate_token()
    # data = {
    #         "chatId": settings.CHAT_ID,
    #         "contentType": "string",
    #         "content": f"{label}\nyour_token: {token}"
    #     }
    # response = requests.post(f"{settings.WHASTAPP_API_URL}/client/sendMessage/mrkein", data, headers=headers)
    # print(response.status_code)
    return HttpResponse("pass")
    wp_session = WhatsappSession(name="mrkein",wp_id=settings.WP_ID)
    
    print(f"wp_session: {wp_session.name}")
    

    wp_api = WhatsappApi(wp_session=wp_session)
    token = generate_token()
    wp_api.send_mesege(token)

    return HttpResponse(f"{wp_session.name}<br>{wp_session.wp_id}<br>{token}")


def send_port(request):
    return HttpResponse("pass")
    port = request.GET.get('port')
    print(port)
    wp_session = WhatsappSession(name="mrkein",wp_id=settings.WP_ID)
    wp_api = WhatsappApi(wp_session=wp_session)
    response = wp_api.send_mesege(port)
    return HttpResponse(f"{response}")