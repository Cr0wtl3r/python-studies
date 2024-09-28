from Agencias import AgenciaVirtual, AgenciaComum, AgenciaPremium
from ContasBancos import ContaCorrente, CartaoCredito

conta_albino = ContaCorrente("Albus Maximus", "123.456.789-10", "3662", "6538-9")
cartao_albino = CartaoCredito(conta_albino)

conta_albino.depositar_dinheiro(1500)

print(
    f"""
• O nome do titular do cartão é: {cartao_albino.titular}
• O número do cartão é: {cartao_albino.numero}
• Referente a conta: {conta_albino.num_conta}
"""
)
conta_albino.consultar_saldo()


agencia_virtual = AgenciaVirtual(
    "www.agenciavirtual.com.br", 55963989634, 12654378000153
)
agencia_comum = AgenciaComum(55985327924, 15346753000154)
agencia_premium = AgenciaPremium(55985157924, 15346353000154)

agencia_virtual.depositar_paypal(20000)
agencia_virtual.verificar_caixa()
print(agencia_virtual.caixa_paypal)

agencia_premium.adicionar_cliente("Albino", 123456789, 15000000)
agencia_premium.adicionar_cliente("Albus Maximus", 123456789, 15000)
agencia_comum.adicionar_cliente("Albus Maximus", 123456789, 15000)

print(agencia_comum.clientes)
print(agencia_premium.clientes)
