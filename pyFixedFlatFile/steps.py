"""Module to build a dict with the information of the attibutes defined in specification"""
from pyFixedFlatFile.exceptions import ParamsException


class Step:
    """create __steps dict with the data defined in specification"""

    def __init__(self, *args, **kwargs):
        self.current_id = None # identifier of the line
        self.__steps = {}
    
    @property
    def steps(self):
        return self.__steps 
    
    def eq(self, id):
        self.current_id = str(id)

    def builder(self, size, **kwargs): 
        """Gera os dicionário que contém como chave o identificador da linha e os
        seus valores são uma lista de dicionário com as informações dos atributos:"""

        """Builds the dict with the attributes of the specification. 
        This dict will be used for generate method from PyFixedFlatFile generate linha of the flat file.
        """

        if kwargs['ident'] != 'constant' and not isinstance(size, int):
            raise ParamsException("Size must be a int! Error in {} attribute.".format(kwargs['ident']))
        
        if 'tp' in kwargs and kwargs['tp'] != 'numeric':
            raise ParamsException("tp value must be only 'numeric'! Error in {} attribute.".format(kwargs['ident']))

        if 'fmt' in kwargs and not callable(kwargs['fmt']):
            raise ParamsException("fmt value must be only a callable! Error in {} attribute.".format(kwargs['ident']))    

        specs = {k: v for k, v in kwargs.items()}
        try:
            specs['size'] = int(size) # preciso colocar isso dentro de um trycexcept
        except Exception as e:
            raise Exception("size attribute must be int but its value has type {}".format(type(size)))
        
        if not self.current_id:
            raise Exception("Id of line not especified: You must use 'eq' method of PyFixedFlatFile!") 

        if self.current_id not in self.steps:
            self.steps[self.current_id] = []
        self.steps[self.current_id].append(specs)
        
        return 