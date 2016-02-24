import tornado.ioloop
import tornado.web
import json


class homePage(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class AdminPage(tornado.web.RequestHandler):
    def get(self):
        self.render("admin.html")

def make_app():
    handlers = [
            (r"/", homePage),
            (r"/", AdminPage),
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
































