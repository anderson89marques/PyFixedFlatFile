"""Layout de Arquivos – CNAB240 – Versão 5.0"""
from pyFixedFlatFile import PyFixedFlatFile
from pyFixedFlatFile.exceptions import LineSizeException


class CNAB240(PyFixedFlatFile):
    def __init__(self, *args, **kwargs):
        super(CNAB240, self).__init__(*args, **kwargs)

    def read(self, file_path):
        result = []
        with open(file_path, 'r') as file_:
            for line in file_:
                if len(line) > 241:
                    raise LineSizeException(
                        "Line has its size bigger than 240!!")
                result.append(self.process_line(line))
        return result
