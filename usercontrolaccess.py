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



    def has_permission(self, perm_tuple):
        """
        checks if (operation,specific) in set ( ('viewSSN', 'john'), ('viewPage', 'john') )
        """
        perm_to_check = perm_tuple

        return perm_to_check in self.set_perm_tuples


def createUser(name):
    user_instance = User(name)

    # len_list_ops = len(user_instance.list_operations) - 1
    # len_list_specifics = len(user_instance.list_specifics) - 1

    # rand_operation = user_instance.list_operations[ randint(0, len_list_ops) ]
    # rand_specific = user_instance.list_specifics[ randint(0,len_list_specifics) ]

    # print(rand_operation, rand_specific)

    # op_spec_tuple = (rand_specific, rand_operation)
    # user_instance.add_user_permission( op_spec_tuple)

    user_instance.add_permission( (user_instance.list_operations[0], user_instance.list_specifics[0]) )
    user_instance.add_permission( (user_instance.list_operations[0], user_instance.list_specifics[1]) )
    user_instance.add_permission( (user_instance.list_operations[1], user_instance.list_specifics[1]) )
    printStuff("user permissions: " , (user_instance.set_perm_tuples))

    return user_instance

def printStuff(*args):
    print(*args)

class HomePage(tornado.web.RequestHandler):
    def get(self):
        self.render(
            'index.html',
            admin_failed = self.application.admin_failed
            )

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

        def build_set_users(list_of_users):
            set_key_to_return = set([])
            for user_pass_dict in list_of_users:
                for user in user_pass_dict:
                    set_key_to_return.add(user)
            return set_key_to_return

        list_of_dict_users = self.application.list_of_dict_users
        set_of_user_names = build_set_users(list_of_dict_users)
        self.application.userInJSON = any(self.application.user == user for user in set_of_user_names)

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

class AdminLoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("admin.html")

    def post(self):

        admin_password = self.get_argument('password')
        creds_passed = admin_password == '0'
        ##set admin/pass cookies
        has_admin_cookie = self.get_cookie("admin")
        if not has_admin_cookie and creds_passed:
            self.set_cookie("admin","0")

        if creds_passed:
            response = {"success": True}
            self.write(json.dumps(response))
        else:
            response = {"success": False}
            self.write(json.dumps(response))

class AdminPanelPageHandler(tornado.web.RequestHandler):
    def get(self):
        password_correct = self.get_cookie("admin") == "0"
        if password_correct:
            self.application.admin_failed = False
            self.render('crudpanel.html')
        else:
            self.application.admin_failed = True
            self.redirect('/')


class HasPermissionHandler(tornado.web.RequestHandler):
    def get(self):
        specific = self.get_argument("specific")
        operation = self.get_argument("operation")
        created_user = self.application.created_user

        perm_to_check = (operation, specific)
        user_has_perm = created_user.has_permission(perm_to_check)

        if user_has_perm:
            response = {"has_permission": True, "message":"User has permission"}
            self.write(json.dumps(response))
        else:
            response = {"has_permission": False, "message":"User doesnt have permission"}
            self.write(json.dumps(response))

class AddPermissionHandler(tornado.web.RequestHandler):
    def get(self):
        specific = self.get_argument("specific")
        operation = self.get_argument("operation")
        created_user = self.application.created_user
        response = {"success": "User Added!"}
        self.write(json.dumps(response))

class PermissionPanelHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('permpanel.html')

def make_app():
    handlers = [
            (r"/", HomePage),
            (r"/admin", AdminLoginHandler),
            (r"/adminCreds", AdminLoginHandler),
            (r"/user([0-9]+)", NewUserLoginHandler),
            (r"/registerPassword", NewUserLoginHandler),
            (r"/verifyPassword", UserLoginHandler),
            (r"/crudpanel", AdminPanelPageHandler),
            (r"/hasPerm", HasPermissionHandler),
            (r"/addPerm", AddPermissionHandler),
            (r"/permpanel", PermissionPanelHandler),

        ]

    app = tornado.web.Application(handlers,debug=True,template_path='./templates',
            static_path='./static',static_url_prefix='/static/')

    app.admin_failed = False

    return app

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































