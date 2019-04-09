"""module to build fixed flat files"""
import inspect
from collections import defaultdict

from pyFixedFlatFile.exceptions import LineIdentifierException, ParamsException


class PyFixedFlatFile:
    """Implements the logic to build a flat file"""

    def __init__(self, *args, **kwargs):
        """
        Parameters:
            NL (str): line break
            start (int): start position of the line identifier
            stop (int): stop position of the line identifier
            identifier_name (str): This is MANDATORY to write the flat file. 
        """

        self.data = defaultdict(list)
        self.nl = '\r\n' if kwargs.get('NL') == 'dos' else '\n'

        # File specification don't initialize a line indexed by zero
        self.position = slice(kwargs.get('start')-1, kwargs.get('stop') -
                              1) if kwargs.get('start') and kwargs.get('start') else slice(0, 1)
        self.identifier_name = kwargs.get('identifier_name', None)
        
        self.__current_id = None  # identifier of the line
        self.__start_column = 0
        self.__identifier_position = 0  # used in generate file from list of tuples data

    def eq(self, id):
        """Set line ident"""

        self.__current_id = str(id)
        self.__start_column = 0

    def read_to_dict(self, file_path):
        return self._read(file_path, self._process_line_to_dict)

    def read_to_tuple(self, file_path):
        return self._read(file_path, self._process_line_to_tuple)

    def generate_from_dict(self, registros):
        return self.generate(registros, self._generate_from_dict)

    def generate_from_tuple(self, registros):
        return self.generate(registros, self._generate_from_tuple)

    def generate(self, registros, generate_function):
        s = ""
        for registro in registros:
            row_str = generate_function(registro) + "{}".format(self.nl)
            s += row_str

        return s

    def fmt(self, spec, value):
        result = ""
        ident = spec['ident']
        size = spec['size']

        if ident == 'constant':
            # the size will be used as constant value
            result = str(size)
        else:
            if 'fmt_w' in spec:
                resp = spec['fmt_w'](value)
            elif ident == 'filler':
                resp = ' '
            else:
                resp = value

            if 'tp' in spec:
                # Put zeros in string's left
                resp = ('{0:.2f}'.format(resp)).replace(
                    '.', '') if isinstance(resp, float) else resp
                result = '{:0>{size}}'.format(int(resp), size=size)
            else:
                result = '{:<{size}}'.format(resp, size=size)

            if len(result) != size:
                raise Exception("The length of value returned by function is not equal the size! Value return ed: {}, size value {}. the size must be {}".format(
                    resp, size, len(resp)))
        return result

    def _read(self, file_path, process_line):
        result = []
        with open(file_path, 'r') as file_:
            for line in file_:
                result.append(self._process_line(line, process_line))
        return result

    def _process_line(self, line, process_line):
        line_id = line[self.position]
        if line_id not in list(self.data.keys()):
            raise LineIdentifierException(
                f"Line identifier not in specification: {self.data.keys()}")

        reg_spec = self.data[line_id]
        line_result = process_line(reg_spec, line)

        return line_result

    def _process_line_to_dict(self, reg_spec, line):
        line_result = {}
        for spec in reg_spec:
            _, resp = self._process_column(spec, line, line_result)
            line_result.update(resp)
        return line_result

    def _process_line_to_tuple(self, reg_spec, line):
        line_result = []
        aux = {}
        for spec in reg_spec:
            resp, dict_resp = self._process_column(spec, line, aux)
            line_result.append(resp)
            aux.update(dict_resp)
        return tuple(line_result)

    def _process_column(self, spec, line, line_dict):
        ident = spec['ident']
        size = spec['size']
        if ident == 'constant':
            size = len(size)

        param = line[spec['slice']].strip()
        if 'fmt_r' in spec:
            if len(inspect.signature(spec['fmt_r']).parameters) == 1:
                param = spec['fmt_r'](param)
            else:
                param = spec['fmt_r'](param, line_dict)

        if 'tp' in spec:
            param = spec['tp'](param)

        return param, {ident: param}

    def _generate_from_dict(self, registro):
        s = ""
        if self.identifier_name in registro and self.data.get(registro[self.identifier_name], None):
            reg_spec = self.data[registro[self.identifier_name]]
            for spec, value in zip(reg_spec, registro.values()):
                s += self.fmt(spec, value)
        else:
            raise Exception("Id is not in attributes specification!")

        return s

    def _generate_from_tuple(self, registro):
        s = ""
        if self.data.get(registro[self.__identifier_position], None):
            reg_spec = self.data[registro[self.__identifier_position]]
            for spec, value in zip(reg_spec, registro):
                s += self.fmt(spec, value)
        else:
            raise Exception("Id is not in attributes specification!")

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

        if ('tp' in kwargs) and (not any((kwargs['tp'] is int, kwargs['tp'] is float))):
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

        if kwargs['ident'] == self.identifier_name:
            self.__identifier_position = len(self.data[self.__current_id]) - 1

    def __getattr__(self, class_name):
        """implementation of builder pattern that turn possible write code like this:
        builder = PyFixedFlatFile()
        builder.eq("10") 
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
