
# PyFixedFlatFile
 
Em vários ambientes corporativos, empresas trocam dados através de arquivos de textos que obedecem uma determinada estrutura, uma determinada especificação acordada entre elas. Esses arquivos são chamados de arquivos `flat file` 
com conteúdo de tamanho fixo.
A biblioteca então facilita a criação desses arquivos do tipo `flat file`.

## Instalação

``` 
pip install pyFixedFlatFile
```

## Agora o pyfixedFlatFile possui o módulo cnabs de extratos

No modulo cnabs tem(terá) como ler arquivos de extratos dos principais bancos.
Por enquanto tem os módulos dos bancos itau, bradesco, santander.

```python
from pyFixedFlatFile.cnabs import Itau

result = Itau.read('Path_para_arquivo_extrato_itau')
print(result)
```

```python
from pyFixedFlatFile.cnabs import Bradesco

result = Bradesco.read('Path_para_arquivo_extrato_bradesco')
print(result)
```

```python
from pyFixedFlatFile.cnabs import Santander

result = Santander.read('Path_para_arquivo_extrato_bradesco')
print(result)
```

## Como usar?
Como demonstração será usada uma especificação fictícia que definirá como o conteúdo do arquivo deve ser estruturado. 
Após essa definição geraremos o um arquivo com dados também fictícios que obedecem a especificação..

#### Especificação
O arquivo vai ser referente a informações de um empresa fictícia chamada MyCompany. 
No arquivo cada registro (linha) deve possuir um identificador com tamanho dois(as duas primeiras colunas), afim de identificar quais são os dados que aquele registro possui.

O registro que começar com 10, vai ter as seguintes informações:

| Nome   | Tamanho | tipo | 
| ------ | ------  | ---- |
| id                | 2       | n (Númerico) |
|cnpj               | 14      | a (Alfa-númerico) |
|inscrição estadual | 14      | a (Alfa-númerico) |
|nome administradora| 34      | a (Alfa-númerico) |
|valor fixo 2       | 1       | a (Alfa-númerico) |
|data criação       | 8       | a (Alfa-númerico) |

O registro que começar com 11, vai ter as informações:

| Nome   | Tamanho | tipo | 
| ------ | ------  | ---- |
| id                 | 2       | n (Númerico) |
| logradouro         | 34      | a (Alfa-númerico) |
| numero             | 5       | n (Númerico) |
| bairro             | 15      | a (Alfa-númerico) |

O registro que começar com 90, vai ter as seguintes informações:

| Nome   | Tamanho | tipo | 
| ------ | ------  | ---- |
| id                 | 2       | n (Númerico) |
| cnpj               | 14      | a (Alfa-númerico) |
| total registros    | 12      | n (Númerico) |

Agora que foi definido como os dados devem ser representados no arquivo, iremos ver como descrever essa especificação no pyFixedFlatFile e então gerar o nosso arquivo `flat file`.

#### Usando o pyFixedFlatFile.
O código abaixo é como definimos atráves da biblioteca a especificação descrita no sub-seção anterior.

```python
from pyFixedFlatFile import PyFixedFlatFile
from datetime import datetime


builder = PyFixedFlatFile() # instânciando um objeto PyFixedFlatFile 

# Aqui definimos a construção do flat file
# registros que começam com 10
builder.eq("10") 
builder.id(2).\
        cnpj(14, fmt=lambda v: "{:>14}".format(v)).\
        inscricaoEstadual(14, default='').\
        nomeAdm(33).\
        constant('2').\
        dataCriacao(8, fmt=lambda d: format(d, '%d%m%Y'))
# registros que começam com 11        
builder.eq(11)
builder.id(2).\
        logradouro(34).\
        numero(5, tp='numeric').\
        bairro(15)
# registros que começam com 90        
builder.eq("90")
builder.id(2).\
        cnpj(14, fmt=lambda v: "{:>14}".format(v)).\
        totalReg(12, tp='numeric').\
        constant('99')
```

Abaixo uma explicação do código acima.

Primeiro importamos o PyFixedFlatFile. Importamos também o datetime pois iremos utilizar no exemplo.
```python
from pyFixedFlatFile import PyFixedFlatFile
from datetime import datetime
```

Então instânciamos o objeto responsável por criar a estrutura ou especificação.
```python
builder = PyFixedFlatFile() # a quebra de linha default será o '\n'

# ou

builder = PyFixedFlatFile(NL='dos') # a quebra de linha será '\r\n'
```

E assim começamos a criar as nossas definições.
```python
builder.eq("10")
```

O trecho de código acima informa ao PyFixedFlatFile que se nos dados que forem passados para ele tiver um id igual a 10, é para vincular os dados com as definições logo após o .eq 
```python
builder.eq("10") 
builder.id(2).\ 
        cnpj(14, fmt=lambda v: "{:>14}".format(v)).\
        inscricaoEstadual(14, default='').\
        nomeAdm(33).\
        constant('2').\
        dataCriacao(8, fmt=lambda d: format(d, '%d%m%Y'))
```

> o *.id(2)* indica que o atributo id deve ter o tamanho 2. primeiro parâmetro  é sempre o tamanho que o atributo deve ter.

> o *.cnpj(14, fmt=lambda v: "{:>14}".format(v))*, indica que o cnpj deve ter o tamanho 14 e como segundo parâmetro é passado um função para formatar o cnpj. Essa função será executada pelo builder e aplicada ao campo passado, no caso o cnpj.

>o *.inscricaoEstadual(14, default='')*, indica que a inscrição estadual deve ter o tamanho 14 e é passado também o parâmetro nomeado default. Com ele podemos indicar um valor para quando esse atributo for passado uma string vazia.

Existem 4 parâmetros nomeados que podemos passar:
1. `default`, onde definimos um valor padrão para aquele campo caso ele esteja vazio (string vazia). 
2. `fmt`, onde passamos uma função que deve ter sempre um único argumento. Esse argumento será o valor do próprio atributo. 
3. `tp`, que é usado em conjunto com seu valor 'numeric', para indicar que o campo é numérico, pois por default os atributos serão tratados como strings.

Na específicação é definido que tem um valor fixo para a posição após o nomeAdm quando o registro começar com o identificador '10'. Esse valor fixo é 2. Para esse tipo de situção foi criado o atributo constant, que na nossa construção fica constant('2').

Com isso já definimos a nossa especificação usando a biblioteca.
## Criando um flat file

Agora precisamos passar os dados para que ela trate e gere o que precisamos.
Suponha que vamos buscar os dados em um banco de dados e montamos uma estruta como abaixo.
```python
registros = [
    {
        "id": "10", "cnpj": "00644422230", "inscricaoEstadual": "", "nomeAdm": "AnjosCompany",
        "dataCriacao": datetime.now(),
    },
    {
        "id": "11", "logradouro": "Av Dario Lopes dos Santos", "numero": "2197", "bairro": "Jardim Botanico", 
    },
    {
        "id": "90", "cnpj": "01234567891234", "totalReg": 23,   
    }
]
```

Os ids nos dicionários presentes na lista registros, não são ids objetos vindo dos bancos de dados e sim a indicação de qual bloco da especificação do PyFixedFlatFile vai tratar o dicionário específico.
Assim a lista acima será tratado pelo bloco:

```python
builder.eq("10") 
builder.id(2).\
        cnpj(14, fmt=lambda v: "{:>14}".format(v)).\
        inscricaoEstadual(14, default='').\
        nomeAdm(33).\
        constant('2').\
        dataCriacao(8, fmt=lambda d: format(d, '%d%m%Y'))
# registros que começam com 11        
builder.eq(11)
builder.id(2).\
        logradouro(34).\
        numero(5, tp='numeric').\
        bairro(15)
# registros que começam com 90        
builder.eq("90")
builder.id(2).\
        cnpj(14, fmt=lambda v: "{:>14}".format(v)).\
        totalReg(12, tp='numeric').\
        constant('99')
```
Percebam que as chaves dos dicionários devem ser iguais ao que foi especificado, exceto pelo atributo `constant`, que não é passado pelo dicionário, pois o seu parâmetro ('2'), já é o seu valor.

Abaixo como passar os dados para a biblioteca:

```python
s = builder.generate_all(registros)
print(s)
with open("fixed_flat_file.txt", "w") as f:
    f.write(s)
```
O método generate irá retorna uma string formatada de acordo com a específicação representando um registro (uma linha) do arquivo. No exemplo, esse retorno é concatenado na variável s, que será salva em um arquivo .txt, que é o `fixed flat file`. Com o método generate_all é retornado uma string com todo o conteúdo que deve ser salvo no arquivo .txt.

Pronto, com o pyFixedFlatFile nós definimos uma especificação para os dados e também processamos os dados com base nessa 
especificação para construir o nosso arquivo.

## Lendo um flat file
Usando como exemplo o arquivo gerado no item anterior.

```python
builder_r = PyFixedFlatFile() # a quebra de linha default será o '\n'

builder_r.eq("10") 
builder_r.id(2).\
        cnpj(14).\
        inscricaoEstadual(14).\
        nomeAdm(33).\
        constant('2').\
        dataCriacao(8, fmt=lambda d: datetime.strptime(d, '%d%m%Y'))

# registros que começam com 11        
builder_r.eq(11)
builder_r.id(2).\
        logradouro(34).\
        numero(5, tp='numeric').\
        bairro(15)
# registros que começam com 90        
builder_r.eq("90")
builder_r.id(2).\
        cnpj(14).\
        totalReg(12, tp='numeric').\
        constant('99')

# Passando a path do arquivo a ser lido
result = builder_r.read("fixed_flat_file.txt")
print(result)

# or

# Criando .csv a partir do arquivo 
builder_r.to_csv("fixed_flat_file.txt")
```

Meta
----
 Anderson Marques - andersonoanjo18@gmail.com
 
 Distribuído sobre lincensa MIT. Veja ``LICENSE.txt`` para mais informções.
