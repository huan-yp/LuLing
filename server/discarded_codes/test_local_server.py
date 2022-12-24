import socketserver
import socket

class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        conn = self.request         # request里封装了所有请求的数据 
        assert(isinstance(conn, socket.socket))
        print(conn)
        # data = conn.recv(65536).decode('utf-8')
        # if not data:
            # conn.close()
            # return 
        import time
        conn.send("HTTP/1.1 200 OK\nServer:Apache Tomcat/5.0.12\nDate:Mon,6Oct2003 13:23:42 GMT\n\n<html>\n<head>\n<title>HTTP响应示例<title>\n</head>\n<body>\nHello HTTP!\n</body>\n</html>\n".encode("utf-8"))
        tex = b"dfhashfiohdoighaio" * 300
        conn.close()
        conn.sendall(tex)
        # time.sleep(10)
        conn.send(b"jskdjfklsadadfjja")
        # conn.send(b"234")
        # conn.send(b"345")
        # conn.close()

def main():
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 1145), MyServer)
    # logger.log(INFO, "Server Start")
    server.serve_forever()
    
    
main()