import tornado.web
from tornado.websocket import WebSocketHandler
from tornado.web import RequestHandler
import os
import datetime


# 视图类
class IndexHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render("index.html")


class AllromHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render("allrom.html")


class StaticFileHandler(tornado.web.StaticFileHandler):
    def __init__(self, *args, **kwargs):
        super(StaticFileHandler, self).__init__(*args, **kwargs)
        # ???
        self.xsrf_token


class HomeHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render("home.html")


# 在新的websocket连接之后执行open函数
class ChatHandler(WebSocketHandler):
    users = set()  # 用于存储在线用户id
    cache = []  # 聊天记录

    #  这个方法向客户端发送message消息，message可以使字符串或者字典(自动转为json字符串)如果binary参数为false,则message会以utf-8的编码发送,如果为true,可以发送二进制模式字节码
    def open(self):
        self.write_message(u"Welcome to the rom!")
        for user in self.users:
            user.write_message(u"[%s]登录了" % (self.request.remote_ip))
        self.users.add(self)

    #  更新cache
    #  @classmethod
    #  def update_cache(cls, chat):
        #  cls.cache.append(chat)
#
    #  对在线的人进行推送
    #  @classmethod
    #  def send_updates(cls, chat):
        #  for users in cls.users:
            #  try:
                #  users.write_message(chat)
            #  except Exception:
                #  return

    # 当websocket连接关闭后调用，客户端主动的关闭
    def on_close(self):
        self.users.remove(self)
        for user in self.users:
            user.write_message(u"[%s]退出了" % (self.request.remote_ip))

    #  当客户端发送消息过来时调用
    def on_message(self, message):
        for user in self.users:
            user.write_message(u"[%s]说:%s" % (self.request.remote_ip, message))

    # 服务器关闭websocket
    def on_close(self):
        self.users.remove(self)
        for u in self.users:
            u.write_message(
                u"[%s]-[%s]-离开聊天室" %
                (self.request.remote_ip,
                 datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    # 判断请求源 对于符合条件的请求源允许连接
    def check_origin(self, origin):
        return True

    #  def open(self):
    #  self.users.append(self)  # 建立连接后添加用户到容器中
    #  for u in self.users:  # 向已在线用户发送消息
    #  u.write_message(u"[%s]-[%s]-进入聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    #  def on_message(self, message):
    #  for u in self.users:  # 向在线用户广播消息
    #  u.write_message(u"[%s]-[%s]-说：%s" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message))
