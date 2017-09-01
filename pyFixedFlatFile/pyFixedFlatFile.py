__author__ = "Anderson Marques Morais"

"""
O objetivo desse projeto é desenvolver um biblioteca que facilite a criação de arquivos cujo
o seu conteúdo é preeenchido por dados(campos) que possuem tamanho fixo.

Para que o método generate funcione de forma correta é preciso antes escrever um descritor,
que informará quais são os campos, seus respectivos tamanhos e possíveis tratamentos antes da transformação.

Ex:
Baseado na especificação da confaz.

registros = [
    {
        "id": "10", "cnpj": "06308851000182", "inscricaoEstadual": "", "nomeAdm": "Mooz", "municipio": "Curitiba", 
        "uf": "PR", "fax": "4134069149" , "dataInicial": datetime.now(), "dataFinal": datetime.now(), "natInfo": "4", "finalidadeArquivo": "1"
    },
    {
        "id": "11", "logradouro": "Av Dario Lopes dos Santos", "numero": "2197", "complemento": "", "bairro": "Jardim Botanico", 
        "cep": "80210010", "nomeContato": "Diego Urtado", "telefone": "4134069149"   
    },
    {
        "id": "90", "cnpj": "01234567891234", "inscricaoEstadual": "", "totalReg65": 0, "totalReg66": 23, "totalReg": 23, "montCartaoCredito": "", "montCartaoDebito": ""   
    }
]
 
# Especificação dos atributos
builder = PyFixedFlatFile()

builder.eq("10") # header
builder.id(2).\
        cnpj(14).\
        inscricaoEstadual(14, default='').\
        nomeAdm(33).\
        constant('2').\
        municipio(30).\
        uf(2).fax(10, tp='numeric').\
        dataInicial(8, fmt=lambda d : format(d, '%d%m%Y')).\
        dataFinal(8, fmt=lambda d : format(d, '%d%m%Y')).\
        constant('2').\
        natInfo(1).\
        finalidadeArquivo(1)
builder.eq(11) # detalhe
builder.id(2).\
        logradouro(34).\
        numero(5, tp='numeric').\
        complemento(22).\
        bairro(15).\
        cep(8).\
        nomeContato(28).\
        telefone(12, tp='numeric')
builder.eq("90") # rodapé
builder.id(2).\
        cnpj(14).\
        inscricaoEstadual(14, default='').\
        constant('65').\
        totalReg65(12, tp='numeric').\
        constant('66').\
        totalReg66(12, tp='numeric').\
        constant('99').\
        totalReg(12, tp='numeric').\
        constant('1')

# gerando a string final
s = ""    
for registro in registros:
    print(registro)
    s += builder.generate(registro) + "\n"
"""

from pyFixedFlatFile.steps import Step

class PyFixedFlatFile:
    def __init__(self, *args, **kwargs):
        self.__step = Step()

    @property
    def step(self):
        return self.__step

    @property
    def steps(self):
        """return steps from specs definition"""
        return self.step.steps

    def fmt(self, spec, registro):
        result = ""
        ident = spec['ident']
        size = spec['size']

        if ident == 'constant':
            result = str(size) # o valor que está em size é o valor da constante     
        else:
            if 'fmt' in spec:
                resp = spec['fmt'](registro[ident])
                if len(resp) != size:
                    raise Exception("The length of value returned by function is not equal the size! Value return ed: {}, size value {}. the size must be {}".format(resp, size, len(resp)))
            elif ident == 'id':
                resp = registro[ident]
                if len(resp) != size:
                    raise Exception("The value of id parameter is not equal size! Id value: {}, size value {}. the size must be {}".format(resp, size, len(resp)))
            elif ident == 'filler':
                resp = ' ' # o campo será preenchido com espaços em branco
            else:
                resp = registro[ident]
            
            if 'tp' in spec and spec['tp'] == 'numeric':
                # Coloca zero(a) a esquerda
                result = '{:0>{size}}'.format(int(resp), size=size)
            else:
                # alinha os dados a esquerda e preenche com espaços em branco a direita
                result = '{:<{size}}'.format(resp, size=size)

        return result

    def eq(self, id):
        """Setando o identicador da linha"""
        self.step.eq(id)

    def generate(self, registro):
        s = ""
        if 'id' in registro and registro['id'] in self.steps:
            reg_spec = self.steps[registro['id']]
            for spec in reg_spec:
                s += self.fmt(spec, registro)
        else:
            raise Exception("Id is not in attributes specification!") # melhorar essas mensagens em inglês
        
        return s

    def __getattr__(self, class_name):

        def builder(size, **kwargs):
            """Esse método retorna o próprio objeto
            para que seja possível escrever a especificação da seguinte maneira:
            builder
            """
            keys = {'ident': class_name, **kwargs}
            self.step.builder(size, **keys)
            
            return self 
        return builder