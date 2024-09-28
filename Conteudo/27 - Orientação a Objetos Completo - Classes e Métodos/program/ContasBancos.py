from datetime import datetime
from random import randint
import pytz

class ContaCorrente:
    """
    Representa uma conta corrente para gerenciar as finanças dos clientes.

    Atributos:
        nome (str): Nome completo do cliente. (Ex.: Albus Maximus)
        cpf (str): CPF do cliente. Deve ser formatado com pontos e traço (Ex.: 123.456.789-90).
        agencia (str): Código da agência bancária, com no máximo 4 dígitos. (Ex.: 1234)
        num_conta (str): Número da conta corrente com dígito verificador, separado por hífen. (Ex.: 12345-6)
        saldo (float): Saldo atual da conta, iniciado como 0.0.
        limite (float): Limite do cheque especial, iniciado como None.
        transacoes (list): Histórico de transações, iniciado como uma lista vazia.
    """

    def __init__(self, nome: str, cpf: str, agencia: str, num_conta: str):
        """
        Inicializa uma nova instância da classe ContaCorrente.

        Args:
            _nome (str): Nome completo do cliente.
            _cpf (str): CPF do cliente, no formato xxx.xxx.xxx-xx.
            _agencia (str): Código da agência bancária.
            _num_conta (str): Número da conta corrente com dígito verificador.
        """
        self.nome: str = nome
        self.cpf: str = cpf
        self.agencia: str = agencia
        self.num_conta: str = num_conta
        self._saldo: float = 0.0
        self._limite: float = None
        self.transacoes: list = []
        self.cartoes = []

    def consultar_saldo(self):
        """
        Exibe o saldo atual da conta do cliente.
        """
        print(f"Seu saldo atual é de {self._saldo:,.2f}")

    def _limite_conta(self):
        """
        Define o limite do cheque especial para a conta.

        Returns:
            float: O valor do limite de cheque especial definido.
        """
        self._limite = -1000
        return self._limite

    def depositar_dinheiro(self, valor: float):
        """
        Deposita um valor na conta corrente do cliente e registra a transação.

        Args:
            valor (float): Valor a ser depositado na conta.
        """
        self._saldo += valor
        self.transacoes.append((valor, self._saldo, ContaCorrente._data_hora()))

    def sacar_dinheiro(self, valor: float):
        """
        Realiza um saque na conta corrente do cliente, verificando o limite.

        Se o valor do saque exceder o saldo disponível, será utilizado o cheque especial.

        Args:
            valor (float): Valor a ser sacado da conta.
        """
        if self._saldo - valor < self._limite_conta():
            print("Você não tem saldo suficiente para sacar esse valor.")
            self.consultar_saldo()
        elif 0 > self._saldo - valor > self._limite_conta():
            print(f"Será sacado R${valor:,.2f}, isso deixará sua conta no negativo. Entrando no cheque especial.")
            self._saldo -= valor
            self.transacoes.append((-valor, self._saldo, ContaCorrente._data_hora()))
            self.consultar_saldo()
        else:
            self._saldo -= valor
            self.transacoes.append((-valor, self._saldo, ContaCorrente._data_hora()))

    def consultar_limite_cheque_especial(self):
        """
        Exibe o limite disponível do cheque especial.
        """
        print(f'Seu limite de Cheque Especial é de R${self._limite_conta():,.2f}')

    def consultar_historico_transacoes(self):
        """
        Exibe o histórico de transações realizadas na conta corrente.
        """
        print('Histórico de Transações:')
        print('Valor, Saldo, Data e Hora')
        for transacao in self.transacoes:
            print('===' * 40)
            print(transacao)

    def transferencia_entre_contas(self, valor: float, conta_destino):
        """
        Realiza uma transferência de valor entre contas correntes.

        Args:
            valor (float): Valor a ser transferido.
            conta_destino (ContaCorrente): Conta de destino para a transferência.
        """
        self._saldo -= valor
        self.transacoes.append((-valor, self._saldo, ContaCorrente._data_hora()))
        conta_destino._saldo += valor
        conta_destino.transacoes.append((valor, conta_destino._saldo, ContaCorrente._data_hora()))

    @staticmethod
    def _data_hora():
        """
        Retorna a data e a hora atual no fuso horário do Brasil.

        Returns:
            str: Data e hora formatada no padrão dd/mm/aaaa HH:MM:SS.
        """
        fuso_BR = pytz.timezone('Brazil/East')
        horario_BR = datetime.now(fuso_BR)
        return horario_BR.strftime('%d/%m/%Y %H:%M:%S')

class CartaoCredito:

    @staticmethod
    def _data_hora():
        """
        Retorna a data e a hora atual no fuso horário do Brasil.

        Returns:
            str: Data e hora formatada no padrão dd/mm/aaaa HH:MM:SS.
        """
        fuso_BR = pytz.timezone('Brazil/East')
        horario_BR = datetime.now(fuso_BR)
        return horario_BR

    def __init__(self, conta_corrente:ContaCorrente):
        self.conta_corrente = conta_corrente
        self.numero = randint(1000000000000000,9999999999999999)
        self.titular = conta_corrente.nome
        self.validade = f'{CartaoCredito._data_hora().month}/{CartaoCredito._data_hora().year}'
        self.cod_seguranca = f'{randint(0,9)}{randint(0,9)}{randint(0,9)}'
        self._senha = '1234'
        self.limite = 1000

        conta_corrente.cartoes.append(self)

    @property
    def senha(self):
        return self._senha

    @senha.setter
    def senha(self, valor):
        if len(valor) == 4 and valor.isnumeric():
            self._senha = valor
        else:
            print('Nova senha inválida!')







