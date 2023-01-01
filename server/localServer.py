"""使用 Python-socketserver 搭建的微服务
使用 TCP 协议发送数据, 建议使用 socket 提供的接口
发送数据和接受数据的格式如下 (JSON 字符串), 使用 utf-8 编码:
Response:
{
    "user":"3051501876"
    "text":"I'm Luling"
}
Request-JSON:
{
    "user":"3051561876",
    "text":"Hello"
}
如果 response 的 text 为空, 则表示该请求失败.
"""
import os
import time
import socketserver
import logging

import constants as C

from logging import INFO, ERROR
from threading import Thread, Lock
from json import loads, dumps, load
from global_attributes import G
from logger import logger
from manager import AccessProcessor, MainProcessor
from translate import Translator




class Chat():
    text = ""
    user = "" # 需要 @ 的 User
    is_response = True
    def __init__(self, message, user:str, is_response=0):
        self.text = message
        self.user = user
        self.is_response = is_response

    def create(self):
        """返回 JSON 字符串, 表示聊天信息
        """
        return dumps({
            "user":self.user,
            "text":self.text
        })
    
    def __str__(self):
        return str(self.__dict__)
    
    
class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        conn = self.request         # request里封装了所有请求的数据
        data = conn.recv(65536).decode('utf-8')
        if not data:
            conn.close()
            return 
        logger.log(INFO, "origin:" + str(data))
        request_dict = loads(data)
        request_chat = Chat(request_dict['text'], request_dict['user'])
        logger.log(INFO, "request:" + str(request_chat))
        response = get_response(request_chat)
        response.text += "\n----译文仅供参考, 以原文为准----\n" + G.translator.translate(response.text)
        logger.log(INFO, "response:" + str(response))
        conn.sendall(dumps({"text":response.text, "user":response.user}).encode('utf-8'))
        conn.close()
            
            
def get_response(request:Chat) -> Chat:
    """通过 ChatRequest 获取 Response
    """
    try:
        statu, text = G.main_processor.process_cmd(text=request.text, user=request.user)
        if statu:
            return Chat(text, request.user, 1)
        G.lock.acquire()
        if (G.statu == 'waiting'):
            G.statu = 'processing'
            G.lock.release() 
            try:
                reply_text = G.main_processor.process(text=request.text, user=request.user)
            except (Exception, BaseException) as e:
                reply_text = "Message With Error" + str(e)
            G.lock.acquire()
            G.statu = 'waiting'
            G.lock.release()
            return Chat(reply_text, request.user, 1)
        else: 
            G.lock.release()
            return Chat("Your Message Is Ignored", request.user, 1)
    except (BaseException, Exception) as e:
        logger.log(ERROR, str(e))


def main():
    G.access_processor = AccessProcessor()
    G.main_processor = MainProcessor()
    G.translator = Translator()
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 1145), MyServer)
    logger.log(INFO, "Server Start")
    server.serve_forever()
    
    
main()