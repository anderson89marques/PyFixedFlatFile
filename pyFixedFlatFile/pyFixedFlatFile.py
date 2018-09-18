"""module to build fixed flat files"""
import inspect
from pyFixedFlatFile.specs import Spec


class PyFixedFlatFile:
    """implements the logics to build the flat files"""

    def __init__(self, *args, **kwargs):
        self.__spec = Spec()
        self.nl = '\r\n' if kwargs.get('NL') == 'dos' else '\n'

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
            # o valor que está em size é o valor da constante
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
                resp = ' '  # o campo será preenchido com espaços em branco
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
            raise Exception("Id is not in attributes specification!")

        return s

    def generate_all(self, registros):
        s = ""
        for registro in registros:
            row_str = self.generate(registro) + "{}".format(self.nl)
            s += row_str

        return s

    def read(self, file_path):
        result = []
        with open(file_path, 'r') as file_:
            for line in file_:
                # get the size of the identifier  in self.data
                # This size will be used to get the identifier in line string
                line_id_size = len(list(self.data.keys())[0])

                line_id = line[:line_id_size]
                reg_spec = self.data[line_id]
                position = 0
                dict_line = {}
                for spec in reg_spec:
                    resp, pos = self.fmt_file(spec, line, position, result)
                    dict_line.update(resp)
                    position = pos
                result.append(dict_line)
        return result

    def fmt_file(self, spec, line, position, dict_line):
        ident = spec['ident']
        size = spec['size']
        if ident == 'constant':
            # o valor que está em size é o valor da constante
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

    def to_csv(self, file_to_read, csv_file_name='csv_file'):
        result = self.read(file_to_read)
        import csv

        with open('{}.csv'.format(csv_file_name), 'w', newline='') as csvfile:
            for row in result:
                writer = csv.DictWriter(csvfile, fieldnames=row.keys())
                writer.writerow(row)

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
