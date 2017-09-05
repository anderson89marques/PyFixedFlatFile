
# PyFixedFlatFile

Biblioteca python que facilita a criação de arquivos de texto do tipo `flat file` que possuam dados de tamanho fixo. 
Em vários ambientes corporativos, empresas trocam dados através de arquivos de textos que obedecem uma determinada estrutura, uma determinada especificação acordada entre elas.

## Instalação

``` 
pip install pyFixedFlatFile
```

## Como usar?
O seu uso é simples e como demonstração será usada uma especificação fictícia de exemplo. A especificação definirá como o conteúdo do arquivo deve ser estruturado e na sequência será usado o PyFixedFlatFile(Py3F :D) para gerar o arquivo desejado.
#### Especificação
O arquivo vai ser referente a informações de um empresa fictícia chamada MyCompany. 
No arquivo cada resgistro (linha) deve possuir um identificador com tamanho dois, afim de identificar quais são os dados que aquele registro possui.

O resgistro que começar com 10, vai ter as seguintes informações:

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

Agora que foi definido como os dados devem ser representados no arquivo, iremos ver como usar o PyFixedFlatFile para criar o `flat file`.

#### Usando o PyFixedFlatFile.
O código abaixo é como definimos atráves da biblioteca a especificação descrita no sub-seção anterior.

```python
from pyFixedFlatFile import PyFixedFlatFile
from datetime import datetime


builder = PyFixedFlatFile() # instânciando um objeto PyFixedFlatFile 

# Aqui definimos a construção do flat file através do objeto 
builder.eq("10") 
builder.id(2).\
        cnpj(14, fmt=lambda v: "{:>14}".format(v)).\
        inscricaoEstadual(14, default='').\
        nomeAdm(33).\
        constant('2').\
        dataCriacao(8, fmt=lambda d: format(d, '%d%m%Y'))
builder.eq(11)
builder.id(2).\
        logradouro(34).\
        numero(5, tp='numeric').\
        bairro(15)
builder.eq("90")
builder.id(2).\
        cnpj(14, fmt=lambda v: "{:>14}".format(v)).\
        totalReg(12, tp='numeric').\
        constant('99')
```

Primeiro importamos o PyFixedFlatFile, além o datetime pois iremos utilizar no exemplo.
```python
from pyFixedFlatFile import PyFixedFlatFile
from datetime import datetime
```

Então é instânciado o objeto responsável por criar a estrutura ou especificação.
```python
builder = PyFixedFlatFile() 
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

Existem três parâmetros nomeados que podemos passar:
1. `default`, onde dizemos um valor padrão para aquele campo caso ele estja vazio (string vazia). 
2. `fmt`, onde passamos uma função que deve ter sempre um único argumento. Esse argumento será o valor do próprio atributo. 
3. `tp`, que é usado em conjunto com seu valor 'numeric', para indicar que o campo é numérico, pois por default os atributos serão tratados como strings.

Na específicação é definido que tem um valor fixo para a posição após o nomeAdm quando o registro começar com o identificador '10'. Esse valor fixo é 2. Para esse tipo de situção foi criado o atributo constant, que na nossa construção fica contant('2').

Com isso já sabemos tudo o que é necessário para definir a nossa especificação usando a biblioteca.
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
Assim o dicionário
```python
{
        "id": "10", "cnpj": "00644422230", "inscricaoEstadual": "", "nomeAdm": "AnjosCompany",
        "dataCriacao": datetime.now(),
}
```
será tratado pelo bloco:
```python
builder.eq("10") 
builder.id(2).\
        cnpj(14, fmt=lambda v: "{:>14}".format(v)).\
        inscricaoEstadual(14, default='').\
        nomeAdm(33).\
        constant('2').\
        dataCriacao(8, fmt=lambda d: format(d, '%d%m%Y'))
```
Percebam que as chaves dos dicionários devem ser iguais ao que foi especificado, exceto pelo atributo `constant`, que não é passado pelo dicionário, pois o seu parâmetro ('2'), já é o seu valor.

Abaixo como passar os dados para a biblioteca:
```python
s = ""    
for registro in registros:
    print(registro)
    s += builder.generate(registro) + "\n"
print(s)
with open("fixed_flat_file.txt", "w") as f:
    f.write(s)
```
O método generate irá retorna uma string formatada de acordo com a específicação representando um registro (uma linha) do arquivo.
No exemplo, esse retorno é concatenado na variável s, que será salva em um arquivo .txt, que é o `fixed flat file`

Meta
----
 Anderson Marques - andersonoanjo18@gmail.com
 
 Distribuído sobre lincensa MIT. Veja ``LICENSE.txt`` para mais informções.