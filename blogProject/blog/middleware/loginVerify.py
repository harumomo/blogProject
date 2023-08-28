from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class Verify(MiddlewareMixin):
    """验证用户是否登录"""
    def process_request(self, request):
        # 只有写博客需要验证登录
        if request.path_info == "/create/":
            info = request.session.get("info")
            if info:
                return
            return redirect("/login")
        return

    def process_response(self, request, response):
        return response
