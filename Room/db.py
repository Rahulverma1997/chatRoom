from Room import mongo1
from Room.modal import users1

db_operations = mongo1.db.users

def save_user(user):
    db_operations.insert_one(user) 



def update_user(user, password):
    db_operations.update_one(
        { '_id' : user.email },
        {
             "$set": { 'password' : password } ,
        }
    ) 


def get_user(email):
    user = db_operations.find_one({'_id' : email })
    return users1(user['firstname'],user['lastname'], user['_id'], user['password']) if user else None

    