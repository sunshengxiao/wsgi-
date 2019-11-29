from webob import dec,Request,Response,exc
class Application:
    #Routtable={}
    Routtable = []
    @classmethod
    def register(self,router):
        self.Routtable.append(router)
    @dec.wsgify
    def __call__(self,request: Request) -> Response:
        for rout in self.Routtable:
            respon=rout.match(request)
            if respon:
                return respon
        raise exc.HTTPNotFound('页面被劫持')
    def notfound(request:Request):
        res=Response()
        res.status_code = 404
        res.body = "<h1>not fond</h1>".encode()
        return res