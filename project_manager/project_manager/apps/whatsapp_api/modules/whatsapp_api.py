import  requests

class WhatsappApi:
    apikey = "apikey_123"
    url = "http://172.22.0.9:3000/" # base url
    session_name = "mrkein"
    wp_id = "5491130748157@c.us"

    def send_mesege(self, message) -> bool:
        label = "BOT:"
        headers = {"x-api-key": self.apikey}
        data = {
                "chatId": self.wp_id,
                "contentType": "string",
                "content": f"{label}\n\t\t{message}"
            }
        target_url = f"{self.url}client/sendMessage/{self.session_name}"
        print(target_url)
        response = requests.post(target_url, data, headers=headers)
        if response.status_code == 200:
            return True
        
        print(response.content)

        return False