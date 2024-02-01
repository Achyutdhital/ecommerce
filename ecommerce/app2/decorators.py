from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def superadmin_required(view_func):
    """
    Decorator for views that only allows superadmins to access.
    """
    actual_decorator = user_passes_test(
        lambda user: user.is_superuser,
        login_url='app2:app2login'  # Change 'app' to your app name and 'home' to the desired URL name
    )
    
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator