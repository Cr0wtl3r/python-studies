
import pandas as pd
import win32com.client as win32
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

buscas = pd.read_excel('buscas.xlsx')
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument(r'--user-data-dir=C:\Users\albin\AppData\Local\Google\Chrome\User Data\Selenium')
nav = webdriver.Chrome(service=service, options=options)

def verificar_existencia_termos_banidos(lista_termos_banidos, name):
    tem_termos_banidos = False
    for termo in lista_termos_banidos:
        if termo in name:
            tem_termos_banidos = True
    return tem_termos_banidos

def verificar_existencia_todos_termos_produtos(lista_termos_nomes, name):
    tem_todos_termos_produtos = True
    for termo in lista_termos_nomes:
        if termo not in name:
            tem_todos_termos_produtos = False
    return tem_todos_termos_produtos

def busca_google_shoping(nav, produto, termos_banidos, preco_minimo, preco_maximo):

    produto = produto.lower()

    termos_banidos = termos_banidos.lower()

    lista_termos_banidos = termos_banidos.split(" ")
    lista_termos_nomes = produto.split(" ")

    lista_ofertas = []
    preco_minimo = float(preco_minimo)
    preco_maximo = float(preco_maximo)


    link = "https://www.google.com/"

    nav.get(link)


    search_field = nav.find_element(By.CLASS_NAME, "gLFyf")

    search_field.click()

    search_field.send_keys(produto)

    search_field.send_keys(Keys.ENTER)


    shoping = nav.find_element(
        By.XPATH, '//*[@id="hdtb-sc"]/div/div/div[1]/div/div[2]/a'
    )

    shoping.click()


    nav.execute_script("window.scrollTo(0, 700)")


    list_results = nav.find_elements(By.CLASS_NAME, "i0X6df")


    for result in list_results:

        name = result.find_element(By.CLASS_NAME, "tAxDx").text

        name = name.lower()


        tem_termos_banidos = verificar_existencia_termos_banidos(
            lista_termos_banidos, name
        )
        tem_todos_termos_produtos = verificar_existencia_todos_termos_produtos(
            lista_termos_nomes, name
        )


        if not tem_termos_banidos and tem_todos_termos_produtos:

            price = result.find_element(By.CLASS_NAME, "a8Pemb").text
            price = (
                price.replace("R$", "")
                .replace(" ", "")
                .replace(".", "")
                .replace(",", ".")
            )
            if price.isdigit():
                price = float(price)
            else:
                price = price.replace('+impostos', '')
                price = float(price)


            if preco_minimo <= price <= preco_maximo:

                link_reference = result.find_element(By.CLASS_NAME, "bONr3b")

                link_parent = link_reference.find_element(By.XPATH, "..")

                link = link_parent.get_attribute("href")


                lista_ofertas.append((name, price, link))


    return lista_ofertas

def busca_buscape(nav, produto, termos_banidos, preco_minimo, preco_maximo):
    produto = produto.lower()
    termos_banidos = termos_banidos.lower()
    lista_termos_banidos = termos_banidos.split(" ")
    lista_termos_nomes = produto.split(" ")
    lista_ofertas = []
    preco_minimo = float(preco_minimo)
    preco_maximo = float(preco_maximo)

    nav.get("https://www.buscape.com.br/")
    nav.find_element(
        By.XPATH,
        '//*[@id="new-header"]/div[1]/div/div/div[3]/div/div/div[2]/div/div[1]/input',
    ).send_keys(produto, Keys.ENTER)

    while len(nav.find_elements(By.CLASS_NAME, "Select_Select__1HNob")) < 1:
        time.sleep(1)
    nav.execute_script("window.scrollTo(0, 250)")

    lista_resultados = nav.find_elements(
        By.CLASS_NAME, "ProductCard_ProductCard_Inner__gapsh"
    )

    for result in lista_resultados:
        price = result.find_element(By.CLASS_NAME, "Text_MobileHeadingS__HEz7L").text
        name = result.find_element(
            By.CLASS_NAME, "ProductCard_ProductCard_Name__U_mUQ"
        ).text
        name = name.lower()
        link = result.get_attribute("href")

        tem_termos_banidos = verificar_existencia_termos_banidos(
            lista_termos_banidos, name
        )
        tem_todos_termos_produtos = verificar_existencia_todos_termos_produtos(
            lista_termos_nomes, name
        )

        if not tem_termos_banidos and tem_todos_termos_produtos:
            price = (
                price.replace("R$", "")
                .replace(" ", "")
                .replace(".", "")
                .replace(",", ".")
            )
            price = float(price)

            if preco_minimo <= price <= preco_maximo:
                lista_ofertas.append((name, price, link))

    return lista_ofertas

tabela_ofertas = pd.DataFrame()

for linha in buscas.index:
    produtos_pesquisa = buscas['Nome']
    preco_mínimo_comparacao = buscas['Preço mínimo']
    produto = buscas.loc[linha, 'Nome']
    termos_banidos = buscas.loc[linha, 'Termos banidos']
    preco_minimo = buscas.loc[linha, 'Preço mínimo']
    preco_maximo = buscas.loc[linha, 'Preço máximo']

    lista_ofertas_google_shoping = busca_google_shoping(nav, produto, termos_banidos, preco_minimo, preco_maximo)
    if lista_ofertas_google_shoping:
        tabela_google_shopping = pd.DataFrame(lista_ofertas_google_shoping, columns=['Produto', 'Preço', 'Link'])
        tabela_ofertas = pd.concat([tabela_ofertas, tabela_google_shopping])
    else:
        tabela_google_shopping = None
    lista_ofertas_buscape = busca_buscape(nav, produto, termos_banidos, preco_minimo, preco_maximo)
    if lista_ofertas_buscape:
        tabela_buscape = pd.DataFrame(lista_ofertas_buscape, columns=['Produto', 'Preço', 'Link'])
        tabela_ofertas = pd.concat([tabela_ofertas, tabela_buscape])
    else:
        tabela_buscape = None

display(tabela_ofertas)

tabela_ofertas.to_excel("Ofertas.xlsx", index=False)

outlook = win32.Dispatch('outlook.application')

if len(tabela_ofertas) > 0:
    mail = outlook.CreateItem(0)
    mail.To = 'crowtler@proton.me'
    mail.Subject = "Produto(s) encontrado(s) na faixa de preço desejada."
    mail.HTMLBody = f"""
    <p>Prezado,</p>
    <p>Encontramos alguns produtos em oferta dentro da faixa de preço desejada. </p>
    {tabela_ofertas.to_html(index=False)}
    <p>Att. Albino Marques</p>
    """
    mail.Send()
    nav.quit()


