"""module to build fixed flat files"""
import inspect
from collections import defaultdict
from pyFixedFlatFile.exceptions import ParamsException


class PyFixedFlatFile:
    """implements the logics to build the flat files"""

    def __init__(self, *args, **kwargs):
        self.current_id = None  # identifier of the line
        self.data = defaultdict(list) # contains the steps from builder definition
        self.nl = '\r\n' if kwargs.get('NL') == 'dos' else '\n'
    
    def eq(self, id):
        """Set line ident"""
        self.current_id = str(id)

    def read(self, file_path):
        result = []
        with open(file_path, 'r') as file_:
            for line in file_:
                # get the size of the identifier in self.data
                # This size will be used to get the identifier in line string
                line_id_size = len(list(self.data.keys())[0])

                line_id = line[:line_id_size]
                reg_spec = self.data[line_id]
                position = 0
                dict_line = {}
                for spec in reg_spec:
                    resp, pos = self.process_column(spec, line, position, result)
                    dict_line.update(resp)
                    position = pos
                result.append(dict_line)
        return result

    def process_column(self, spec, line, position, dict_line):
        ident = spec['ident']
        size = spec['size']
        if ident == 'constant':
            size = len(size)

        end = position+size
        param = line[position:end].strip()
        if 'fmt' in spec:
            if len(inspect.signature(spec['fmt']).parameters) == 1:
                param = spec['fmt'](param)
            else:
                param = spec['fmt'](param, dict_line)
            
        if 'tp' in spec and spec['tp'] == 'numeric':
            param = int(param)
        
        if 'tp' in spec and spec['tp'] == 'float':
            param = float(param)

        result = {ident: param}
        return result, end

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
                resp = ' '  #   o campo será preenchido com espaços em branco
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
                # Coloca zero(a) a esquerda
                result = '{:0>{size}}'.format(int(resp), size=size)
            else:
                # alinha os dados a esquerda e preenche com espaços em branco a direita
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

        if not self.current_id:
            raise Exception(
                "Id of line not especified: You must use 'eq' method of PyFixedFlatFile!")

        self.data[self.current_id].append(kwargs)

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
