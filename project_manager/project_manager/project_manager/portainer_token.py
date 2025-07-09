
def get_p_token():
    from apps.account.models import PortainerToken # esto es asi para evitar el error encapsulamos el import
    try:        
        return PortainerToken.objects.all().first().token
    except:
        return None
        
PORTAINER_TOKEN = get_p_token()