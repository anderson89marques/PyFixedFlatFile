"""module to build fixed flat files"""
import inspect
from collections import defaultdict

from pyFixedFlatFile.exceptions import LineIdentifierException, ParamsException


class PyFixedFlatFile:
    """Implements the logic to build a flat file"""

    def __init__(self, *args, **kwargs):
        # contains the steps from builder definition
        self.data = defaultdict(list)
        self.nl = '\r\n' if kwargs.get('NL') == 'dos' else '\n'

        # File specification don't initialize a line indexed by zero
        self.position = slice(kwargs.get('start')-1, kwargs.get('stop') -
                              1) if kwargs.get('start') and kwargs.get('start') else slice(0, 1)

        self.__current_id = None  # identifier of the line
        self.__start_column = 0

    def eq(self, id):
        """Set line ident"""
        self.__current_id = str(id)
        self.__start_column = 0

    def read(self, file_path):
        result = []
        with open(file_path, 'r') as file_:
            for line in file_:
                result.append(self.process_line(line))
        return result

    def process_line(self, line):
        line_id = line[self.position]
        if line_id not in list(self.data.keys()):
            raise LineIdentifierException(
                f"Line identifier not in specification: {self.data.keys()}")

        reg_spec = self.data[line_id]
        line_dict = {}
        for spec in reg_spec:
            resp = self.process_column(spec, line, line_dict)
            line_dict.update(resp)

        return line_dict

    def process_column(self, spec, line, line_dict):
        ident = spec['ident']
        size = spec['size']
        if ident == 'constant':
            size = len(size)

        param = line[spec['slice']].strip()
        if 'fmt' in spec:
            if len(inspect.signature(spec['fmt']).parameters) == 1:
                param = spec['fmt'](param)
            else:
                param = spec['fmt'](param, line_dict)

        if 'tp' in spec and spec['tp'] == 'numeric':
            param = int(param)

        if 'tp' in spec and spec['tp'] == 'float':
            param = float(param)

        result = {ident: param}
        return result

    def fmt(self, spec, registro):
        result = ""
        ident = spec['ident']
        size = spec['size']

        if ident == 'constant':
            # the size will be used as constant value
            result = str(size)
        else:
            if 'fmt' in spec:
                resp = spec['fmt'](registro[ident])
            elif ident == 'id':
                resp = registro[ident]
                if len(resp) != size:
                    raise Exception("The value of id parameter is not equal size! Id value: {}, size value {}. the size must be {}".format(
                        resp, size, len(resp)))
            elif ident == 'filler':
                resp = ' '
            else:
                if ident in registro:
                    resp = registro[ident]
                else:
                    if 'default' in spec:
                        resp = spec['default']
                    else:
                        raise Exception(
                            "attribute {} not specified".format(ident))

            if 'tp' in spec and spec['tp'] == 'numeric':
                # Put zeros in string's left
                result = '{:0>{size}}'.format(int(resp), size=size)
            else:
                result = '{:<{size}}'.format(resp, size=size)

            if len(result) != size:
                raise Exception("The length of value returned by function is not equal the size! Value return ed: {}, size value {}. the size must be {}".format(
                    resp, size, len(resp)))
        return result

    def generate(self, registro):
        s = ""
        if 'id' in registro and registro['id'] in self.data:
            reg_spec = self.data[registro['id']]
            for spec in reg_spec:
                s += self.fmt(spec, registro)
        else:
            raise Exception("Id is not in attributes specification!")

        return s

    def generate_all(self, registros):
        s = ""
        for registro in registros:
            row_str = self.generate(registro) + "{}".format(self.nl)
            s += row_str

        return s

    def builder_data(self, size, **kwargs):
        """Builds the dict with the attributes of the specification. 
        This dict will be used for generate method from PyFixedFlatFile generate linha of the flat file.
        """

        if not self.__current_id:
            raise Exception(
                "Id of line not especified: You must use 'eq' method of PyFixedFlatFile!")

        if kwargs['ident'] != 'constant' and not isinstance(size, int):
            raise ParamsException(
                "Size must be a int! Error in {} attribute.".format(kwargs['ident']))

        if 'tp' in kwargs and kwargs['tp'] not in ('numeric', 'float'):
            raise ParamsException(
                "tp value must be only 'numeric'! Error in {} attribute.".format(kwargs['ident']))

        if 'fmt' in kwargs and not callable(kwargs['fmt']):
            raise ParamsException(
                "fmt value must be only a callable! Error in {} attribute.".format(kwargs['ident']))

        try:
             kwargs['size'] = int(
                 size) if kwargs['ident'] != 'constant' else size
        except Exception as e:
            raise Exception(
                "size attribute must be int but its value has type {}".format(type(size)))

        kwargs['slice'] = slice(self.__start_column,
                                self.__start_column+kwargs['size'])
        self.__start_column += kwargs['size']
        self.data[self.__current_id].append(kwargs)

    def __getattr__(self, class_name):
        """implementation of builder pattern that turn possible write code like this:
        builder = PyFixedFlatFile()
        builder.eq("10") 
        builder.id(2).\
        cnpj(14, fmt=lambda v: "{:>14}".format(v)).\
        inscricaoEstadual(14, default='').\
        """
        def builder(size, **kwargs):
            kwargs.update({'ident': class_name})
            self.builder_data(size, **kwargs)

            return self
        return builder

    def to_csv(self, file_to_read, csv_file_name='csv_file'):
        result = self.read(file_to_read)
        import csv

        with open('{}.csv'.format(csv_file_name), 'w', newline='') as csvfile:
            for row in result:
                writer = csv.DictWriter(csvfile, fieldnames=row.keys())
                writer.writerow(row)
