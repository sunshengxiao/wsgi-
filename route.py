import re
class Router():
    PATERN = re.compile('/({[^{}:]+:?[^{}:]*})')

    TYPEPATTERN = {
        'str': r'[^/]+',
        'word': r'\w+',
        'int': r'[-+]?\d+',
        'float': r'[-+]?\w+.\w+',
        'any': r'.+'
    }
    TYPECAST = {
        'str': str,
        'word': str,
        'int': int,
        'float': float,
        'any': str
    }

    def transform(self,kv: str):
        name, _, type = kv.strip('/{}').partition(':')
        return '/（?P<{}>{}'.format(name, self.TYPEPATTERN.get(type, '\w+')), name, self.TYPECAST.get(type, str)

    def parse(self,src: str):
        start = 0
        res = ''
        translator = {}
        while True:
            matcher = self.PATERN.search(src, start)
            if matcher:
                res += matcher.string[start:matcher.start()]
                temp = self.transform(matcher.string[matcher.start():matcher.end()])
                print(temp)
                res += temp[0]
                translator[temp[1]] = temp[2]
                start = matcher.end()
            else:
                break
        if res:
            return res, translator
        else:
            return src, translator

    def __init__(self,prefix:str):
        self.__router=[]
        self.__prefix=prefix
    @property
    def prefix(self):
        return self.__prefix
    def route(self, parttern, *method):
        def wrapper(handle):
            # cls.Routtable[path]=handle
            realparttern,translator=self.parse(parttern)
            self.__router.append((method, re.compile(realparttern),translator, handle))
            return handle
        return wrapper
    def get(self,parttern):
        return self.route(parttern,'GET')

    def post(self, parttern):
        return self.route(parttern, 'POST','GET')

    def match(self,request):
        if request.path.startswith(self.prefix):
            for meth,par,tran,han in self.__router:
                if not meth or request.method.upper() in meth:
                    match=par.match(request.path.replace(self.prefix,"",1))
                    if match:
                        # request.args=matcher.group()
                        # newdict={}
                        # request.kwargs=Dictaob(match.groupdict())
                        # for k,v in match.groupdict().item():
                        #     newdict[k]=tran[k](v)
                        # request.vars=Dictaob[newdict]
                        # print(newdict)
                        return han(request)