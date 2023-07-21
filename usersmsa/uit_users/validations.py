from django.contrib.auth import get_user_model


UserModel = get_user_model()


def validation_error(data):
    if data.get('email') is None or data.get('username') is None or data.get('password') is None:
        return 'Fields email, username and passwors is required'

    email = data['email'].strip()
    username = data['username'].strip()
    password = data['password'].strip()

    if not email or UserModel.objects.filter(email=email).exists():
        return 'Choose another email'

    if not password or len(password) < 8:
        return 'Choose another password, min 8 characters'

    if not username:
        return 'Choose another username'
    return None
