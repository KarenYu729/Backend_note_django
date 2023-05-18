from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class AuthfromMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path_info in ['/login/', '/image/code/']:
            return
        # if have login
        info_dict = request.session.get("info")
        if info_dict:
            return
        # haven't login
        return redirect('/login/')



