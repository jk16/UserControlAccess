import tornado.ioloop
import tornado.web
import json

class homePage(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class AdminPage(tornado.web.RequestHandler):
    def get(self):
        self.render("admin.html")

    def post(self):
        username = self.get_argument('user')
        password = self.get_argument('pass')
        credsPassed = username == 'Admin' and password == '0'

        if (credsPassed):
            response = {"user": username, "password": password}
            self.write(json.dumps(response))                

def make_app():
    handlers = [
            (r"/", homePage),
            (r"/admin", AdminPage),
            (r"/adminCreds", AdminPage),
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
































