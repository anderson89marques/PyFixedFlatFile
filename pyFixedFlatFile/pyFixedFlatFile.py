"""module to build fixed flat files"""
from pyFixedFlatFile.specs import Spec


class PyFixedFlatFile:
    """implements the logics to build the flat files"""

    def __init__(self, *args, **kwargs):
        self.__spec = Spec()

    @property
    def spec(self):
        return self.__spec

    @property
    def data(self):
        """return steps from specs definition"""
        return self.spec.data

    def fmt(self, spec, registro):
        result = ""
        ident = spec['ident']
        size = spec['size']

        if ident == 'constant':
            result = str(size) # o valor que está em size é o valor da constante     
        else:
            if 'fmt' in spec:
                resp = spec['fmt'](registro[ident])
            elif ident == 'id':
                resp = registro[ident]
                if len(resp) != size:
                    raise Exception("The value of id parameter is not equal size! Id value: {}, size value {}. the size must be {}".format(resp, size, len(resp)))
            elif ident == 'filler':
                resp = ' ' # o campo será preenchido com espaços em branco
            else:
                if ident in registro:
                    resp = registro[ident]
                else:
                    if 'default' in spec:
                        resp = spec['default']
                    else:
                        raise Exception("attribute {} not specified".format(ident))
                            
            if 'tp' in spec and spec['tp'] == 'numeric':
                # Coloca zero(a) a esquerda
                result = '{:0>{size}}'.format(int(resp), size=size)
            else:
                # alinha os dados a esquerda e preenche com espaços em branco a direita
                result = '{:<{size}}'.format(resp, size=size)
            
            if len(result) != size:
                    raise Exception("The length of value returned by function is not equal the size! Value return ed: {}, size value {}. the size must be {}".format(resp, size, len(resp)))
        return result

    def eq(self, id):
        """Setando o identicador da linha"""
        self.spec.eq(id)

    def generate(self, registro):
        s = ""
        if 'id' in registro and registro['id'] in self.data:
            reg_spec = self.data[registro['id']]
            for spec in reg_spec:
                s += self.fmt(spec, registro)
        else:
            raise Exception("Id is not in attributes specification!") # melhorar essas mensagens em inglês
        
        return s

    def __getattr__(self, class_name):
        """implementation of builder pattern that turn possible write code like this:
        builder = PyFixedFlatFile()
        builder.eq("10") 
        builder.id(2).\
        cnpj(14, fmt=lambda v: "{:>14}".format(v)).\
        inscricaoEstadual(14, default='').\
        """
        def builder(size, **kwargs):
            keys = {'ident': class_name, **kwargs}
            self.spec.builder(size, **keys)
            
            return self 
        return builder