from .models import User


class ChatIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        chat_id = request.GET.get("chat_id") or request.POST.get("chat_id")
        
        if chat_id:
            try:
                request.user = User.objects.get(chat_id=chat_id)
            except User.DoesNotExist:
                request.user = None

        return self.get_response(request)

