
class users1:
    def __init__(self, firstname, lastname ,email,password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        

    @staticmethod
    def is_authenticated(self):
        return True

    @staticmethod
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email

    def create(self):
        new_user = {
            'firstname' : self.firstname, 
            'lastname' : self.lastname,
            '_id' : self.email,
            'password' : self.password,
            'varification': False
            
            }
        print('Created successfully')

        return new_user
        


