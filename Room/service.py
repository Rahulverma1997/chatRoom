from flask import url_for
from flask_mail import Message
from Room import mail
from Room.modal import users1
from Room.token import get_reset_token



def send_reset_email(user):
    token = get_reset_token(user)
    print("token================", token)
    msg = Message('Password Reset Request',
                  sender='chatroomservice.com',
                  recipients=[user.email])
    msg.body = f'''HI there

To reset your chatRoom password, visit the following link:
{url_for('auth_obj.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


def send_varification_email(user):
    token = get_reset_token(user, expires_sec=18000)
    print("token================", token)
    msg = Message('Varification Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To varify your email, visit the following link:
{url_for('auth_obj.varification_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)



