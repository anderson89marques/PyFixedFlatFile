"""Module to build a dict with the information of the attibutes defined in specification"""
from pyFixedFlatFile.exceptions import ParamsException


class Spec:
    """create __steps dict with the data defined in specification"""

    def __init__(self, *args, **kwargs):
        self.current_id = None  # identifier of the line
        self._spec_data = {}

    @property
    def data(self):
        return self._spec_data

    def eq(self, id):
        self.current_id = str(id)

    def builder(self, size, **kwargs):
        """Builds the dict with the attributes of the specification. 
        This dict will be used for generate method from PyFixedFlatFile generate linha of the flat file.
        """

        if kwargs['ident'] != 'constant' and not isinstance(size, int):
            raise ParamsException(
                "Size must be a int! Error in {} attribute.".format(kwargs['ident']))

        if 'tp' in kwargs and kwargs['tp'] not in ('numeric', 'float'):
            raise ParamsException(
                "tp value must be only 'numeric'! Error in {} attribute.".format(kwargs['ident']))

        if 'fmt' in kwargs and not callable(kwargs['fmt']):
            raise ParamsException(
                "fmt value must be only a callable! Error in {} attribute.".format(kwargs['ident']))

        specs = {k: v for k, v in kwargs.items()}
        try:
            # preciso colocar isso dentro de um trycexcept
            specs['size'] = int(
                size) if kwargs['ident'] != 'constant' else size
        except Exception as e:
            raise Exception(
                "size attribute must be int but its value has type {}".format(type(size)))

        if not self.current_id:
            raise Exception(
                "Id of line not especified: You must use 'eq' method of PyFixedFlatFile!")

        if self.current_id not in self.data:
            self.data[self.current_id] = []
        self.data[self.current_id].append(specs)

        return
