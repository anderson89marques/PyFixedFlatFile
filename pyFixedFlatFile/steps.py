_author_ = "Anderson Marques Morais"
from pyFixedFlatFile.exceptions import ParamsException

class Step:
    def __init__(self, *args, **kwargs):
        self.current_id = None
        self.__steps = {}
    
    @property
    def steps(self):
        return self.__steps 
    
    def eq(self, id):
        self.current_id = str(id)

    def builder(self, size, **kwargs): 
        """É utilizada na contrução da especificação dos atributos"""

        if kwargs['ident'] != 'constant' and not isinstance(size, int):
            raise ParamsException("Size must be a int! Error in {} attribute.".format(kwargs['ident']))
        
        if 'tp' in kwargs and kwargs['tp'] != 'numeric':
            raise ParamsException("tp value must be only 'numeric'! Error in {} attribute.".format(kwargs['ident']))

        if 'fmt' in kwargs and not callable(kwargs['fmt']):
            raise ParamsException("fmt value must be only a callable! Error in {} attribute.".format(kwargs['ident']))    

        specs = {k: v for k, v in kwargs.items()}
        specs['size'] = int(size) # preciso colocar isso dentro de um trycexcept
        
        if not self.current_id:
            raise Exception("Id of line not especified: You must use 'eq' method of PyFixedFlatFile!") 

        if self.current_id not in self.steps:
            self.steps[self.current_id] = []
        self.steps[self.current_id].append(specs)
        
        return "ok"
        
    def __getattr__(self, nome_classe):
        """É utilizada na contrução da especificação dos atributos"""

        def build(size, **kwargs): 
            """"""
            specs = {k: v for k, v in kwargs.items()}
            specs['ident'] = nome_classe
            specs['size'] = int(size) # preciso colocar isso dentro de um trycexcept
            
            if self.current_id not in self.steps:
                self.steps[self.current_id] = []
            self.steps[self.current_id].append(specs)

            return "ok"
        return build

