from functools import wraps
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'message': 'Authentication required!'}, status=401)
        if request.user.role != 'manager':
            return JsonResponse({'message': 'Admin access required!'}, status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def user_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'message': 'Authentication required!'}, status=401)
        if request.user.role != 'employee':
            return JsonResponse({'message': 'User access required!'}, status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped_view
