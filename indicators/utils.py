# you have already created UserSerializer
from indicators.serializers import UserSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    user = UserSerializer(user, context={'request': request}).data
    return {
        'token': token,
        'userid': user['id'],
        'email': user['email'],
        'firstname': user['first_name'],
        'lastname': user['last_name'],
        'phone': user['phone'],
        'user_type': user['user_type'],
        'privilege': user['privilege']
    }
