from django.core.cache import cache
TIME_TO_DELETE = 3600
def get_p_token():
    token = cache.get("portainer_token")
    if token is None:
        from apps.account.models import PortainerToken
        try:
            token_obj = PortainerToken.objects.first()
            token = token_obj.token if token_obj else None
            cache.set("portainer_token", token, timeout=TIME_TO_DELETE)  
        except Exception:
            return None
    return token