from .models import User

def save_profile(request, backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        profile = User.objects.filter(name=response.get('email'))
        if not profile:
            profile = User(id=user.id, email=user.email, name=response.get('name'))
        profile.save()
        request.session['id'] = user.id
        if profile:
            request.session['id'] = user.id
   