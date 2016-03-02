import tornado.ioloop
import tornado.web
import json
from random import randint



class User():
    def __init__(self, uName):
        self.uName = uName
        self.set_perm_tuples = set() #user starts with no permissions


        ##this is for testing
        self.list_operations = ["viewSSN", "viewPage", "viewLocation"]
        self.list_specifics = ["user1", "user2", "user3"]
    def __repr__(self):
        return "test()"

    def __str__(self, *args):
        return str(*args)

    def add_permission(self, perm_tuple):
        """
        Takes in a permission tuple: (operation,specific)
        
        Appends the permission tuple to the set of tuples

        """
        self.set_perm_tuples.add(perm_tuple)



    def has_permission(self, operation, specific):
        """
        checks if (operation,specific) in set ( ('viewSSN', 'john'), ('viewPage', 'john') )
        """
        printStuff("self.user_permissions: " , self.user_permissions)
        perm_to_check = (operation, specific)

        return perm_to_check in self.set_perm_tuples

def test():
    john = User('john')
    alberto = User('alberto') 
    alberto.add_user_permission( ("view","john") )
    alberto.add_user_permission( ("view","leon") )


def createUser(name):
    user_instance = User(name)

    # len_list_ops = len(user_instance.list_operations) - 1
    # len_list_specifics = len(user_instance.list_specifics) - 1

    # rand_operation = user_instance.list_operations[ randint(0, len_list_ops) ]
    # rand_specific = user_instance.list_specifics[ randint(0,len_list_specifics) ]

    # print(rand_operation, rand_specific)

    # op_spec_tuple = (rand_specific, rand_operation)
    # user_instance.add_user_permission( op_spec_tuple)

    user_instance.add_user_permission( (user_instance.list_operations[0], user_instance.list_specifics[0]) )
    user_instance.add_user_permission( (user_instance.list_operations[0], user_instance.list_specifics[1]) )
    user_instance.add_user_permission( (user_instance.list_operations[1], user_instance.list_specifics[1]) )

    return user_instance

def printStuff(*args):
    print(*args)

class HomePage(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class NewUserLoginHandler(tornado.web.RequestHandler):
    """
    GET: handles logic for whether a /user is in the JSON data list
    POST: handles user adding a password
    """
    def get(self, id_):
        #get ID from /user[0-9]+
        self.application.user = "user" + id_

        with open('data/data.json') as json_data:
            d = json.load(json_data)
            json_data.close()
            """
                {"users": [ { "user111": 1} ], "admin": 0}
            """
            #stores {"users": [ { "user111": 1} ], "admin": 0}
            self.application.dict_of_users = d 
            #stores "users": [ { "user111": 1} ]
            self.application.list_of_dict_users = d['users']

        self.application.userInJSON = False


        #for each user in the list of the user dictionaries: {'user2': '1'}
        for usernameDict in self.application.list_of_dict_users:
            #if the users are the same
            if self.application.userInJSON:
                break
            #for a user in the user dictionary: 'user2'
            for userName in usernameDict:
                #are the users the same?
                self.application.userInJSON = userName == self.application.user
                #if they are the same
                if self.application.userInJSON:
                    #get the password
                    self.application.password = usernameDict[self.application.user]
                    #render user.html which will load HTML based off userInJSON
                    self.render(
                        'user.html',
                        memberVal = "user" + str(id_),
                        userInJSON = self.application.userInJSON,
                        )
                    break

    def post(self):
        #get password from POST
        password = self.get_argument("password")
        #new user that will be added to the users list in JSON
        new_user = {
            self.application.user: password
            }

        # append to the users list in JSON
        self.application.list_of_dict_users.append(new_user)

        jsonFile = open("data/data.json", "w+")
        jsonFile.write(json.dumps(self.application.dict_of_users))
        jsonFile.close()

        #make response
        response = {"success": True, "message": "User has been added", "userName": self.application.user}
        #send response
        self.write(json.dumps(response))

        self.application.created_user = createUser(self.application.user)
        



class AdminLoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("admin.html")

    def post(self):
        count_login_attempts = 0

        username = self.get_argument('user')
        password = self.get_argument('pass')
        credsPassed = username == 'Admin' and password == '0'

        if (credsPassed):
            response = {"success": True, "user": username, "password": password}
            self.write(json.dumps(response))     
        else:
            count_login_attempts +=1
            response = {"success": False, "user": username, "password": password}
            self.write(json.dumps(response))

class UserLoginHandler(tornado.web.RequestHandler):
    def post(self):
        submittedPassword = self.get_argument("password")
        userName = self.get_argument("userName")
        with open('data/data.json') as json_data:
            d = json.load(json_data)
            json_data.close()
            list_of_dict_users = d['users']
        for dictionaries in list_of_dict_users:
            for user in dictionaries:
                if userName in user:
                    user_password = dictionaries[user]

        if user_password == submittedPassword:
            response = {"success": True}
            self.write(json.dumps(response))
        else:
            response = {"success": False}
            self.write(json.dumps(response))

        # createUser(userName)
        self.application.created_user = createUser(userName)


class PanelPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('panel.html')

class HasPermissionHandler(tornado.web.RequestHandler):
    def get(self):
        specific = self.get_argument("specific")
        operation = self.get_argument("operation")


        # printStuff("list_specifics: " , self.application.created_user.list_specifics)
        # printStuff("list_operations: " , self.application.created_user.list_operations)


        spec_not_in_list = specific not in self.application.created_user.list_specifics
        op_not_in_list = operation not in self.application.created_user.list_operations

        if spec_not_in_list or op_not_in_list:
            response = {"has_permission": False, "message":"Specific or Operation does not exist!"}
            self.write(json.dumps(response))
        else:
            has_permission = self.application.created_user.has_permission(operation, specific)
            message = "Accepted" if has_permission else "Not Accepted"
            response = {"has_permission": has_permission, "message": message}
            self.write(json.dumps(response))
            
def make_app():
    handlers = [
            (r"/", HomePage),
            (r"/admin", AdminLoginHandler),
            (r"/adminCreds", AdminLoginHandler),
            (r"/user([0-9]+)", NewUserLoginHandler),
            (r"/registerPassword", NewUserLoginHandler),
            (r"/verifyPassword", UserLoginHandler),
            (r"/panel", PanelPageHandler),
            (r"/hasPerm", HasPermissionHandler)

        ]

    return tornado.web.Application(handlers,debug=True,template_path='./templates',
            static_path='./static',static_url_prefix='/static/')

def main():
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    """
    Purpose: If you use as a module code wont get executed
             If you use it as an executable it will get called 
    """
    main()































