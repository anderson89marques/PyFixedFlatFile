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
                    resp, pos = self.fmt_file(spec, line, position, dict_line)
                    dict_line.update(resp)
                    position = pos
                result.append(dict_line)
        return result

Santander = SantanderFlatFile()

# REGISTRO HEADER DE ARQUIVO - TAMANHO DO REGISTRO = 240 Bytes
Santander.eq('0')
(Santander
    .codigo_banco(3, tp='numeric')
    .codigo_lote(4, tp='numeric')
    .tipo_registro(1)
    .vazio1(9)
    .tipo_inscricao(1)
    .numero_inscricao(14, tp='numeric')
    .codigo_convenio(20)
    .codigo_agencia(5)
    .digito_verificador_agencia(1)
    .numero_conta(12, tp='numeric')
    .digito_verificador_conta(1)
    .digito_verificador_conta_agencia(1)
    .nome_empresa(30)
    .nome_banco(30)
    .vazio2(10)
    .codigo_retorno(1)
    .data_geracao_arquivo(8, fmt=lambda d: datetime.strptime(d, '%d%m%Y'))
    .hora_arquivo(6, fmt=lambda date, data:  datetime.strptime(data['data_geracao_arquivo'].strftime('%d%m%Y') + ' ' + date , '%d%m%Y %H%M%S'))
    .arquivo_sequencia(5)
    .layout(3)
    .densidade_gravacao(5)
    .vazio3(70))

# REGISTRO HEADER LOTE - TAMANHO DO REGISTRO = 240 Bytes
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
    .data_geracao_arquivo(8)
    .saldo_inicial(18)
    .situacao_saldo_inicial(1)
    .posicao_saldo_inicial(1)
    .moeda_referenciada_extrato(3)
    .numero_sequencia_extrato(5)
    .vazio3(16)
    .vazio4(47))

# REGISTRO SEGMENTO E - TAMANHO DO REGISTRO = 240 Bytes
Santander.eq('3')
(Santander
    .codigo_banco(3, tp='numeric')
    .codigo_lote(4, tp='numeric')
    .tipo_registro(1)
    .numero_registro(5, tp='numeric')    
    .segmento(1)
    .vazio1(3)
    .tipo_inscricao(1)
    .numero_inscricao(14)
    .codigo_convenio(20)
    .codigo_agencia(5)
    .digito_verificador_agencia(1)
    .numero_conta(12)
    .digito_verificador_conta(1)
    .digito_verificador_conta_agencia(1)
    .nome_empresa(30)
    .reservado(6)
    .natureza(3)
    .tipo_complemento(2)
    .reservado2(20)
    .cpmf(1)
    .data_contabil(8, fmt=lambda d: datetime.strptime(d, '%d%m%Y') if d else '')
    .data_lancamento(8, fmt=lambda d: datetime.strptime(d, '%d%m%Y') if d else '')
    .valor_lancamento(18, fmt=lambda value: value[:16] + '.' + value[16:], tp='float')
    .lancamento(1)
    .categoria(3)
    .codigo_lancamento(4)
    .historico(25)
    .numero_documento(6)
    .complemento_historico(25)
    .reservado3(8))

# REGISTRO TRAILER DE LOTE - TAMANHO DO REGISTRO = 240 Bytes
Santander.eq('5')
(Santander
    .codigo_banco(3, tp='numeric')
    .codigo_lote(4, tp='numeric')
    .tipo_registro(1)
    .vazio1(9)
    .tipo_inscricao(1)
    .numero_inscricao(14, tp='numeric')
    .codigo_convenio(20)
    .codigo_agencia(5)
    .digito_verificador_agencia(1)
    .numero_conta(12, tp='numeric')
    .digito_verificador_conta(1)
    .digito_verificador_conta_agencia(1)
    .saldo(16, fmt=lambda value: value[:14] + '.' + value[14:], tp='float')
    .vazio2(18)
    .limite(18, fmt=lambda value: value[:16] + '.' + value[16:], tp='float')
    .saldo_bloqueado(18, fmt=lambda value: value[:16] + '.' + value[16:], tp='float')
    .data_final(8, fmt=lambda d: datetime.strptime(d, '%d%m%Y'))
    .saldo_final(18, fmt=lambda value: value[:16] + '.' + value[16:], tp='float')
    .situacao(1)
    .posicao_final(1)
    .total_registros(6, tp='numeric')
    .total_valor_debito(18, fmt=lambda value: value[:16] + '.' + value[16:], tp='float')
    .total_valor_credito(18, fmt=lambda value: value[:16] + '.' + value[16:], tp='float')
    .vazio3(28))

#REGISTRO TRAILER DE ARQUIVO - TAMANHO DO REGISTRO = 240 Bytes
Santander.eq('9')
(Santander
    .codigo_banco(3, tp='numeric')
    .codigo_lote(4)
    .tipo_registro(1)
    .vazio1(9)
    .total_quantidade_lotes(6, tp='numeric')
    .total_quantidade_registros(6, tp='numeric')
    .total_contas_conciliadas(6, tp='numeric')
    .vazio2(205))