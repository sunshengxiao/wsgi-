import webob
from webob import dec,Request,Response,exc
import wsgiref
from wsgiref.simple_server import make_server ,demo_app
from .route import Router
from .App import Application
import re
class Dictaob:
    def __init__(self,d:dict):
        if isinstance(d,(dict,)):
            self.__dict__['_dict']=d
        else:
            self.__dict__['_dict']={}

    def __getattr__(self, item):
        try:
            return self._dict[item]
        except KeyError:
            raise AttributeError('Attribute {} Not Found'.format(item))
    def __setattr__(self, key, value):
        raise NotImplemented



idex=Router('')
py=Router('/python')
Application.register(idex)
Application.register(py)
@py.get('/{name}')#################?????
def index(request:Request):
    res=Response()
    res.body="<h1>主页</h1>".encode()
    return res
@py.post('/python$')
def showpython(request:Request):
    res=Response()
    res.body='<h1>学习python</h1>'.encode()
    return res

if __name__ =='__main__':
    ip ="127.0.0.1"
    port=9999
    try:
        server=make_server(ip,port,Application())
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()



