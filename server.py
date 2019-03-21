import tornado.ioloop
import tornado.web
import os
#import logging
import tornado.auth
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
#import uuid
import json
import pprint
from game_engine import InitGame, LoadGame, SetUp, SolvePuzzle, LoadGameLogicWithLines

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        #self.write("Hello, world")
        self.render('index.html')

#application = tornado.web.Application([
#    (r"/", MainHandler),
#])

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        example_response = {}
        example_response['name'] = 'example'
        example_response['width'] = 1020
        self.write(json.dumps(example_response))

    def post(self):
        jsonobj = json.loads(self.request.body)
        print 'Post data received'
        for key in jsonobj.keys():
            print 'key: %s , value: %s' % (key, jsonobj[key])
            if key == 'LOAD':
                difficulty = int(jsonobj[key])
                InitGame()
                rowList = LoadGame(difficulty)
                response_to_send = {}
                rows = {"ROWS": rowList}
                self.write(json.dumps(rows))
            if key == 'SOLVE':
                SetUp()
                rowList = SolvePuzzle()
                rows = {"ROWS": rowList}
                self.write(json.dumps(rows))
            if key == 'CUSTOM':
                lines = jsonobj[key]
                print 'lines = ' + str(lines)
                LoadGameLogicWithLines(lines)
                SetUp()
                rowList = SolvePuzzle()
                rows = {"ROWS": rowList}
                self.write(json.dumps(rows))



settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    "login_url": "/login",
    "xsrf_cookies": False,
}

application = tornado.web.Application([
    (r'/test', TestHandler),
    (r"/", MainHandler),
    (r"/(apple-touch-icon\.png)", tornado.web.StaticFileHandler,

     dict(path=settings['static_path'], )),
], **settings)

if __name__ == "__main__":
    application.listen(8888)
    print 'server running on port 8888'
    tornado.ioloop.IOLoop.instance().start()