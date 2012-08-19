import os
import tornado.ioloop
import tornado.web

import attendence

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("query_print.html", classes=attendence.classes)

class PrintHandler(tornado.web.RequestHandler):
  def post(self):
		min_empty = int(self.get_argument("min_empty"))
		self.render("print_classes.html", groups=attendence.class_print_info(min_empty))
		
handlers = [
    (r"/query_print", MainHandler),
    (r"/print", PrintHandler),
]

settings = dict(
		template_path=os.path.join(os.path.dirname(__file__), "templates"),
		static_path=os.path.join(os.path.dirname(__file__), "static"),
		debug=True,
)               

application = tornado.web.Application(handlers, **settings)

if __name__ == "__main__":
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()

