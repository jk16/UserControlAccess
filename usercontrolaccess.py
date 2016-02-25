import tornado.ioloop
import tornado.web
import json


def printStuff(*args):
    print(*args)

class HomePage(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class UserPage(tornado.web.RequestHandler):
    """
    GET: handles logic for whether a /user is in the JSON data list
    POST: handles user adding a password
    **Dont handle logic verification here
    """
    def get(self, id_):
        #get ID from /user[0-9]+
        self.application.user = "user" + id_
        with open('data/data.json') as json_data:
            d = json.load(json_data)
            json_data.close()
            self.application.list_users = d

        #validate user existence in JSON
        userInJSON = any( u['user'] == self.application.user for u in self.application.list_users['users'] )

        #render user.html which will load HTML based off userInJSON
        self.render(
            'user.html',
            memberVal = "user" + str(id_),
            userInJSON = userInJSON,
            )

    def post(self):
        #get password from POST
        password = self.get_argument("password")
        #new user that will be added to the users list in JSON
        new_user = {
            "user": self.application.user, 
            "pass":password
            }

        # append to the users list in JSON
        self.application.list_users['users'].append(new_user)

        jsonFile = open("data/data.json", "w+")
        jsonFile.write(json.dumps(self.application.list_users))
        jsonFile.close()

        #make response
        response = {"success": True, "message": "User has been added"}
        #send response
        self.write(json.dumps(response))


class AdminPage(tornado.web.RequestHandler):
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

def make_app():
    handlers = [
            (r"/", HomePage),
            (r"/admin", AdminPage),
            (r"/adminCreds", AdminPage),
            (r"/user([0-9]+)", UserPage),
            (r"/registerPassword", UserPage)
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































