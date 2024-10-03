from .models import User
from django.http import JsonResponse

class ChatIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        chat_id = request.GET.get("chat_id") or request.POST.get("chat_id")
        
        if chat_id:
            try:
                request.user = User.objects.get(chat_id=chat_id)
            except User.DoesNotExist:
                # return self.process_exception(request, User.DoesNotExist)
                return JsonResponse({"message": "User not found"}, status=404)
                
                
        return self.get_response(request)
        
    