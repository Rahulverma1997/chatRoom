from itsdangerous import TimedJSONWebSignatureSerializer as Serializer  
from Room.modal import users1
from Room.db import get_user
from flask import current_app
    
    
def get_reset_token(user, expires_sec=1800):
    s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
    return s.dumps({'email': user.email}).decode('utf-8')


def verify_reset_token(token):
    s = Serializer(current_app.config['SECRET_KEY']) 
    try:
        email = s.loads(token)['email']
    except:
        return None
    return get_user(email)