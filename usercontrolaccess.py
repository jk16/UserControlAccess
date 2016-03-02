import tornado.ioloop
import tornado.web
import json
from random import randint



class User():
    def __init__(self, uName):
        self.uName = uName
        self.user_permissions = {} #{operation: specific}

    def __repr__(self):
        return "test()"

    def __str__(self, *args):
        return str(*args)

    def add_user_permission(self, perm_tuple):
        """
        Takes in a permission tuple: (operation,specific)
        """

        specific = perm_tuple[1]
        operation = perm_tuple[0]

        operation_in_list = True if operation in self.user_permissions else False

        if operation_in_list:
            # add to the existing "operation": set([])
            self.user_permissions[operation].add(specific)
        else :
            self.user_permissions[operation] = set([])
            self.user_permissions[operation].add(specific)



    def has_permission(self, operation, specific):
        """action on a user"""

        """
        { "views": set([]), "click":set([])  }
        
        """
        print(specific in self.user_permissions[operation])
        return True if specific in self.user_permissions[operation] else False

def test():
    self.application.john = User('john')
    self.application.alberto = User('alberto') 
    self.application.alberto.add_user_permission( ("view","john") )
    self.application.alberto.add_user_permission( ("view","leon") )


def createUser(name):
    list_operations = ["user1", "user2", "user3"]
    list_specifics = ["viewSSN", "viewPage", "viewLocation"]
    user = User(name)
    len_list_ops = len(list_operations) - 1
    len_list_specifics = len(list_specifics) - 1

    rand_operation = list_operations[ randint(0, len_list_ops) ]
    rand_specific = list_specifics[ randint(0,len_list_specifics) ]

    print(rand_operation, rand_specific)
    op_spec_tuple = (rand_specific, rand_operation)
    user.add_user_permission( op_spec_tuple)

    return user

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


        for usernameDict in self.application.list_of_dict_users:
            self.application.userInJSON = any( userName == self.application.user for userName in usernameDict )
            if self.application.userInJSON:
                self.application.password = usernameDict[self.application.user]


        #render user.html which will load HTML based off userInJSON
        self.render(
            'user.html',
            memberVal = "user" + str(id_),
            userInJSON = self.application.userInJSON,
            )

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

        has_permission = self.application.created_user.has_permission(operation, specific)
        response = {"has_permission": has_permission}
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































