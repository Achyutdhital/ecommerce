

def user_info(request):
    user = request.user
    return {'user_info': user}