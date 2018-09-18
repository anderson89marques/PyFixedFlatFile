"""
Layout Santander 240 posições versão 8.2 com complemento
"""
from pyFixedFlatFile import PyFixedFlatFile
from datetime import datetime


class SantanderFlatFile(PyFixedFlatFile):
    def __init__(self, *args, **kwargs):
        super(SantanderFlatFile, self).__init__(*args, **kwargs)
    
    def read(self, file_path):
        result = []
        with open(file_path, 'r') as file_:
            for line in file_:
                line_id = line[7]
                reg_spec = self.data[line_id]
                position = 0
                dict_line = {}
                for spec in reg_spec:
                    resp, pos = self.fmt_file(spec, line, position)
                    dict_line.update(resp)
                    position = pos
                result.append(dict_line)
        return result

Santander = SantanderFlatFile()

# Header
Santander.eq('0')
(Santander
    .numero_banco(3)
    .lote_servico(4)
    .tipo_registro(1)
    .vazio1(9)
    .tipo_inscricao_empresa(1)
    .numero_inscricao_empresa(14)
    .codigo_convenio(20)
    .codigo_agencia(5)
    .digito_verificador_agencia(1)
    .numero_conta(12)
    .digito_verificador_conta(1)
    .digito_verificador_conta_agencia(1)
    .nome_empresa(30)
    .nome_banco(30)
    .vazio2(10)
    .codigo_remessa(1)
    .data_geracao_arquivo(8, fmt=lambda d: datetime.strptime(d, '%d%m%Y'))
    .hora_arquivo(6)
    .arquivo_sequencia(5)
    .versao_layout(3)
    .densidade_gravacao(5)
    .vazio3(70))

# Header Lote
Santander.eq('1')
(Santander
    .numero_banco(3)
    .lote_servico(4)
    .tipo_registro(1)
    .tipo_operacao(1)
    .tipo_servico(2)
    .forma_lancamento(2)
    .numero_versao_layout_lote(3)
    .vazio1(1)
    .tipo_inscricao_empresa(1)
    .numero_inscricao_empresa(14)
    .codigo_convenio(20)
    .codigo_agencia(5)
    .digito_verificador_agencia(1)
    .numero_conta(12)
    .digito_verificador_conta(1)
    .digito_verificador_conta_agencia(1)
    .nome_empresa(30)
    .vazio2(38)
    .data_geracao_arquivo(8, fmt=lambda d: datetime.strptime(d, '%d%m%Y'))
    .saldo_inicial(18)
    .situacao_saldo_inicial(1)
    .posicao_saldo_inicial(1)
    .moeda_referenciada_extrato(3)
    .numero_sequencia_extrato(5)
    .vazio3(16)
    .vazio4(47))

# Registro Detalhe de Lote

# Registro Trailer