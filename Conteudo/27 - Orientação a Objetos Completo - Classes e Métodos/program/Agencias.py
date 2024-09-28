from random import randint


class Agencia:

    def __init__(self, telefone, cnpj, numero):

        self.telefone = telefone
        self.cnpj = cnpj
        self.numero = numero
        self.clientes = []
        self.caixa = 0
        self.emprestimos = []

    def verificar_caixa(self):
        if self.caixa < 1000000:
            print(f"Caixa abaixo do nível recomendado. Caixa Atual: {self.caixa}")
        else:
            print(f"O valor do Caixa está ok. Caixa Atual: {self.caixa}")

    def emprestar_dinheiro(self, valor, cpf, juros):
        if self.caixa > valor:
            self.emprestimos.append((valor, cpf, juros))
        else:
            print("Empréstimo não é possível. Dinheiro não disponível em caixa.")

    def adicionar_cliente(self, nome, cpf, patrimonio):
        self.clientes.append((nome, cpf, patrimonio))


# Agencia Virtual - Irá Herdar tudo da classe Agencia
class AgenciaVirtual(Agencia):

    def __init__(self, site, telefone, cnpj):

        self.site = site
        super().__init__(telefone, cnpj, numero=randint(1000, 9999))
        self.caixa = 1000000
        self.caixa_paypal = 0

    def depositar_paypal(self, valor):

        if valor <= self.caixa:
            self.caixa -= valor
            self.caixa_paypal += valor
        else:
            print(
                f"Você não possuí saldo suficiente para fazer este saque: Saldo atual R$ {self.caixa}"
            )

    def sacar_paypal(self, valor):

        if valor <= self.caixa_paypal:
            self.caixa_paypal -= valor
            self.caixa += valor
        else:
            print(
                f"Você não possuí saldo suficiente para fazer este saque: Saldo atual R$ {self.caixa_paypal}"
            )


# Agencia Comum - Irá Herdar tudo da classe Agencia
class AgenciaComum(Agencia):

    def __init__(
        self,
        telefone,
        cnpj,
    ):
        super().__init__(telefone, cnpj, numero=randint(1000, 9999))
        self.caixa = 1000000


# Agencia Premium - Irá Herdar tudo da classe Agencia
class AgenciaPremium(Agencia):

    def __init__(self, telefone, cnpj):
        super().__init__(telefone, cnpj, numero=randint(1000, 9999))
        self.caixa = 10000000

    def adicionar_cliente(self, nome, cpf, patrimonio):
        PATRIMONIO_MINIMO: int = 1000000
        if patrimonio > 1000000:
            super().adicionar_cliente(nome, cpf, patrimonio)
        else:
            print(
                f"""
O cliente não tem o patrimonio necessário para entrar na agência. 
• Patrimônio do cliente R${patrimonio}.
• Patrimônio necessário R${PATRIMONIO_MINIMO} 
"""
            )
