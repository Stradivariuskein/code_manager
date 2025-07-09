from django.db import models
import project_manager.settings as settings
import requests


class WhatsappSession(models.Model):
    name = models.CharField(max_length=50)
    wp_id = models.CharField(max_length=18)


class WhatsappApi(models.Model):
    apikey = settings.WHASTAPP_API_KEY
    url = settings.WHASTAPP_API_URL # base url
    wp_session = models.ForeignKey(WhatsappSession, on_delete=models.PROTECT)

    def send_mesege(self, token) -> bool:
        label = "BOT:"
        headers = {"x-api-key": self.apikey}
        data = {
                "chatId": self.wp_session.wp_id,
                "contentType": "string",
                "content": f"{label}\n\t\tyour_token: {token}"
            }
        target_url = f"{self.url}client/sendMessage/{self.wp_session.name}"
        print(target_url)
        response = requests.post(target_url, data, headers=headers)
        if response.status_code == 200:
            return True
        
        print(response.content)

        return False
        
    

