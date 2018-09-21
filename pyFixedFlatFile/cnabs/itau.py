"""
ITAU
EXTRATO DE CONTA CORRENTE
Layout de Arquivos – CNAB240 – Versão 5.0
"""
from pyFixedFlatFile import PyFixedFlatFile
from datetime import datetime


class ItauFlatFile(PyFixedFlatFile):
    def __init__(self, *args, **kwargs):
        super(ItauFlatFile, self).__init__(*args, **kwargs)
    
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

Itau = ItauFlatFile()

# REGISTRO HEADER DE ARQUIVO - TAMANHO DO REGISTRO = 240 Bytes
Itau.eq('0')
(Itau
    .codigo_banco(3, tp='numeric')
    .codigo_lote(4, tp='numeric')
    .tipo_registro(1)
    .vazio1(9)
    .tipo_inscricao(1)
    .numero_inscricao(14, tp='numeric')
    .vazio2(15)
    .codigo_convenio(5)
    .zeros1(1, tp='numeric')
    .codigo_agencia(4, tp='numeric')
    .digito_verificador_agencia(1)
    .zeros(7, tp='numeric')
    .numero_conta(5, tp='numeric')
    .vazio3(1)
    .digito_verificador_conta_agencia(1)
    .nome_empresa(30)
    .nome_banco(30)
    .vazio4(10)
    .codigo_retorno(1)
    .data_geracao_arquivo(8, fmt=lambda d: datetime.strptime(d, '%d%m%Y'))
    .hora_geracao_arquivo(6, fmt=lambda date, data:  datetime.strptime(data['data_geracao_arquivo'].strftime('%d%m%Y') + ' ' + date , '%d%m%Y %H%M%S'))
    .sequencia(6, tp='numeric')
    .layout(3)
    .zeros2(5, tp='numeric')
    .reservado(5)
    .vazio5(49))

# REGISTRO HEADER LOTE - TAMANHO DO REGISTRO = 240 Bytes
Itau.eq('1')
(Itau
    .codigo_banco(3, tp='numeric')
    .codigo_lote(4, tp='numeric')
    .tipo_registro(1)
    .tipo_operacao(1)
    .tipo_servico(2, tp='numeric')
    .forma_lancamento(2, tp='numeric')
    .layout(3)
    .vazio1(1)
    .tipo_inscricao(1)
    .numero_inscricao(14, tp='numeric')
    .tipo_conta(4)
    .vazio2(11)
    .codigo_convenio(5)
    .zeros1(1, tp='numeric')
    .codigo_agencia(4, tp='numeric')
    .digito_verificador_agencia(1)
    .zeros(7, tp='numeric')
    .numero_conta(5, tp='numeric')
    .vazio3(1)
    .digito_verificador_conta_agencia(1)
    .nome_empresa(30)
    .vazio4(40)
    .data_inicial(8, fmt=lambda d: datetime.strptime(d, '%d%m%Y'))
    .valor_inicial(18, fmt=lambda value: value[:16] + '.' + value[16:] , tp='float')
    .situacao_inicial(1)
    .status_inicial(1)
    .tipo_moeda(3)
    .sequencia_extrato(5, tp='numeric')
    .vazio5(62))

# REGISTRO SEGMENTO E - TAMANHO DO REGISTRO = 240 Bytes
Itau.eq('3')
(Itau
    .codigo_banco(3, tp='numeric')
    .codigo_lote(4, tp='numeric')
    .tipo_registro(1)
    .numero_registro(5, tp='numeric')    
    .segmento(1)
    .lancamento(1, tp='numeric')
    .vazio1(2)
    .tipo_inscricao(1)
    .numero_inscricao(14, tp='numeric')
    .vazio2(15)
    .codigo_convenio(5)
    .zeros1(1, tp='numeric')
    .codigo_agencia(4, tp='numeric')
    .digito_verificador_agencia(1)
    .zeros(7, tp='numeric')
    .numero_conta(5, tp='numeric')
    .vazio3(1)
    .digito_verificador_conta_agencia(1)
    .nome_empresa(30)
    .reservado(6)
    .natureza(3)
    .tipo_complemento(2, tp='numeric')
    .banco_origem(3, tp='numeric')
    .agencia_origem(5, tp='numeric')
    .agencia_conta_origem(12, tp='numeric')
    .cpmf(1)
    .data_contabil(8, fmt=lambda d: datetime.strptime(d, '%d%m%Y') if d else '')
    .data_lancamento(8, fmt=lambda d: datetime.strptime(d, '%d%m%Y') if d else '')
    .valor_lancamento(18, fmt=lambda value: value[:16] + '.' + value[16:], tp='float')
    .lancamento(1)
    .categoria(3)
    .codigo_lancamento(4)
    .historico(25)
    .vazio4(33)
    .numero_documento(6))


# REGISTRO TRAILER DE LOTE - TAMANHO DO REGISTRO = 240 Bytes
Itau.eq('5')
(Itau
    .codigo_banco(3, tp='numeric')
    .codigo_lote(4, tp='numeric')
    .tipo_registro(1)
    .vazio1(9)
    .tipo_inscricao(1)
    .numero_inscricao(14, tp='numeric')
    .vazio2(15)
    .codigo_convenio(5)
    .zeros1(1, tp='numeric')
    .codigo_agencia(4, tp='numeric')
    .digito_verificador_agencia(1)
    .zeros(7, tp='numeric')
    .numero_conta(5, tp='numeric')
    .vazio3(1)
    .digito_verificador_conta_agencia(1)
    .vazio4(16)
    .bloqueado(18, fmt=lambda value: value[:16] + '.' + value[16:], tp='float')
    .limite(18, fmt=lambda value: value[:16] + '.' + value[16:], tp='float')
    .saldo_bloqueado(18, fmt=lambda value: value[:16] + '.' + value[16:], tp='float')
    .data_final(8, fmt=lambda d: datetime.strptime(d, '%d%m%Y'))
    .saldo_final(18, fmt=lambda value: value[:16] + '.' + value[16:], tp='float')
    .situacao(1)
    .status(1)
    .total_registros(6, tp='numeric')
    .total_valor_debito(18, fmt=lambda value: value[:16] + '.' + value[16:], tp='float')
    .total_valor_credito(18, fmt=lambda value: value[:16] + '.' + value[16:], tp='float')
    .totais_valores_nao_contabeis(18, fmt=lambda value: value[:16] + '.' + value[16:], tp='float')
    .vazio5(10))

#REGISTRO TRAILER DE ARQUIVO - TAMANHO DO REGISTRO = 240 Bytes
Itau.eq('9')
(Itau
    .codigo_banco(3, tp='numeric')
    .codigo_lote(4)
    .tipo_registro(1)
    .vazio1(9)
    .total_quantidade_lotes(6, tp='numeric')
    .total_quantidade_registros(6, tp='numeric')
    .total_contas_conciliadas(6, tp='numeric')
    .vazio2(205))