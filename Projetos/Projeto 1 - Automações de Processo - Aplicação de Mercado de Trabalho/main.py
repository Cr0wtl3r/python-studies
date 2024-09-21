import os
import pathlib
import time

import pandas as pd
import win32com.client as win32


def get_path(pasta:str):
    path_files = os.path.join(os.getcwd(), pasta)
    return path_files

emails = pd.read_excel(get_path(r"Bases de Dados\Emails.xlsx"))
lojas = pd.read_csv(get_path(r"Bases de Dados\Lojas.csv"), encoding="latin1", sep=';')
vendas = pd.read_excel(get_path(r"Bases de Dados\Vendas.xlsx"))

META_FATURAMENTO_DIA = 1000
META_FATURAMENTO_ANO = 1650000
META_QTDE_PRODUTOS_DIA = 4
META_QTDE_PRODUTOS_ANO = 120
META_TICKET_MEDIO_DIA = 500
META_TICKET_MEDIO_ANO = 500

vendas = vendas.merge(lojas, on='ID Loja')

dicionario_lojas = {}
for loja in lojas['Loja']:
    dicionario_lojas[loja] = vendas.loc[vendas['Loja']==loja, :]

indicador_dia = vendas['Data'].max()

caminho_backup = pathlib.Path(r'Backup Arquivos Lojas')
arquivos_pasta_backup = caminho_backup.iterdir()
nomes_arquivos_backup = [file.name for file in arquivos_pasta_backup]

for loja in dicionario_lojas:
    if loja not in nomes_arquivos_backup:
        nova_pasta = caminho_backup / loja
        nova_pasta.mkdir()

    nome_arquivo = f'{indicador_dia.month}_{indicador_dia.day}_{loja.replace(' ', '_')}.xlsx'
    local_arquivo = caminho_backup / loja / nome_arquivo

    dicionario_lojas[loja].to_excel(local_arquivo)


for loja in dicionario_lojas:
    vendas_loja = dicionario_lojas[loja]
    vendas_lojas_sem_date = vendas_loja.drop('Data', axis=1)
    vendas_loja_dia = vendas_loja.loc[vendas_loja['Data']==indicador_dia, :]
    vendas_lojas_dia_sem_date = vendas_loja_dia.drop('Data', axis=1)


    # Faturamento
    faturamento_ano = vendas_loja['Valor Final'].sum()
    faturamento_dia = vendas_loja_dia['Valor Final'].sum()

    # Diversidade de Produtos
    qtde_produtos_ano = len(vendas_loja['Produto'].unique())
    qtde_produtos_dia = len(vendas_loja_dia['Produto'].unique())

    # Ticket Médio por Venda
    valor_venda = vendas_lojas_sem_date.groupby('Código Venda').sum()
    valor_venda_dia = vendas_lojas_dia_sem_date.groupby('Código Venda').sum()

    ticket_medio_ano =  valor_venda['Valor Final'].mean()
    ticket_medio_dia = valor_venda_dia['Valor Final'].mean()


    outlook = win32.Dispatch('outlook.application')

    nome = emails.loc[emails['Loja']==loja,'Gerente'].values[0] # type: ignore
    mail = outlook.CreateItem(0)
    mail.To = emails.loc[emails['Loja']==loja,'E-mail'].values[0] # type: ignore
    mail.Subject = f"OnePage Dia {indicador_dia.day}/{indicador_dia.month} - Loja {loja}"

    if faturamento_dia >= META_FATURAMENTO_DIA:
        cor_fat_dia = 'green'
    else:
        cor_fat_dia = 'red'
    if faturamento_ano >= META_FATURAMENTO_ANO:
        cor_fat_ano = 'green'
    else:
        cor_fat_ano = 'red'
    if qtde_produtos_dia >= META_QTDE_PRODUTOS_DIA:
        cor_qtde_dia = 'green'
    else:
        cor_qtde_dia = 'red'
    if qtde_produtos_ano >= META_QTDE_PRODUTOS_ANO:
        cor_qtde_ano = 'green'
    else:
        cor_qtde_ano = 'red'
    if ticket_medio_dia >= META_TICKET_MEDIO_DIA:
        cor_ticket_dia = 'green'
    else:
        cor_ticket_dia = 'red'
    if ticket_medio_ano >= META_TICKET_MEDIO_ANO:
        cor_ticket_ano = 'green'
    else:
        cor_ticket_ano = 'red'

    mail.HTMLBody = f'''
    <p>Bom dia, {nome}</p>

    <p>O resultado de ontem <strong>({indicador_dia.day}/{indicador_dia.month})</strong> da <strong>Loja {loja}</strong> foi:</p>

    <table>
      <tr>
        <th>Indicador</th>
        <th>Valor Dia</th>
        <th>Meta Dia</th>
        <th>Cenário Dia</th>
      </tr>
      <tr>
        <td>Faturamento</td>
        <td style="text-align: center">R${faturamento_dia:.2f}</td>
        <td style="text-align: center">R${META_FATURAMENTO_DIA:.2f}</td>
        <td style="text-align: center"><font color="{cor_fat_dia}">◙</font></td>
      </tr>
      <tr>
        <td>Diversidade de Produtos</td>
        <td style="text-align: center">{qtde_produtos_dia}</td>
        <td style="text-align: center">{META_QTDE_PRODUTOS_DIA}</td>
        <td style="text-align: center"><font color="{cor_qtde_dia}">◙</font></td>
      </tr>
      <tr>
        <td>Ticket Médio</td>
        <td style="text-align: center">R${ticket_medio_dia:.2f}</td>
        <td style="text-align: center">R${META_TICKET_MEDIO_DIA:.2f}</td>
        <td style="text-align: center"><font color="{cor_ticket_dia}">◙</font></td>
      </tr>
    </table>
    <br>
    <table>
      <tr>
        <th>Indicador</th>
        <th>Valor Ano</th>
        <th>Meta Ano</th>
        <th>Cenário Ano</th>
      </tr>
      <tr>
        <td>Faturamento</td>
        <td style="text-align: center">R${faturamento_ano:.2f}</td>
        <td style="text-align: center">R${META_FATURAMENTO_ANO:.2f}</td>
        <td style="text-align: center"><font color="{cor_fat_ano}">◙</font></td>
      </tr>
      <tr>
        <td>Diversidade de Produtos</td>
        <td style="text-align: center">{qtde_produtos_ano}</td>
        <td style="text-align: center">{META_QTDE_PRODUTOS_ANO}</td>
        <td style="text-align: center"><font color="{cor_qtde_ano}">◙</font></td>
      </tr>
      <tr>
        <td>Ticket Médio</td>
        <td style="text-align: center">R${ticket_medio_ano:.2f}</td>
        <td style="text-align: center">R${META_TICKET_MEDIO_ANO:.2f}</td>
        <td style="text-align: center"><font color="{cor_ticket_ano}">◙</font></td>
      </tr>
    </table>

    <p>Segue em anexo a planilha com todos os dados para mais detalhes.</p>

    <p>Qualquer dúvida estou à disposição.</p>
    <p>Att., Albino Marques</p>
    '''
    attachment = pathlib.Path.cwd() / caminho_backup / loja / f'{indicador_dia.month}_{indicador_dia.day}_{loja.replace(' ', '_')}.xlsx'
    mail.Attachments.Add(str(attachment))

    mail.Send()


vendas_sem_data = vendas.drop('Data', axis=1)
faturamento_lojas_ano = vendas_sem_data.groupby('Loja')[['Valor Final']].sum()
faturamento_lojas_ano = faturamento_lojas_ano.sort_values(by='Valor Final', ascending=False)

arquivo_ranking_anual = f'{indicador_dia.day}_{indicador_dia.month}_Ranking_Anual.xlsx'
faturamento_lojas_ano.to_excel(rf'Backup Arquivos Lojas\{arquivo_ranking_anual}')

vendas_dia = vendas.loc[vendas['Data'] == indicador_dia,:]
faturamento_lojas_dia = vendas_dia.groupby('Loja')[['Valor Final']].sum()
faturamento_lojas_dia = faturamento_lojas_dia.sort_values(by='Valor Final', ascending=False)

arquivo_ranking_diario = f'{indicador_dia.day}_{indicador_dia.month}_Ranking_Diario.xlsx'
faturamento_lojas_ano.to_excel(rf'Backup Arquivos Lojas\{arquivo_ranking_diario}')

time.sleep(2)
outlook = win32.Dispatch('outlook.application')

mail = outlook.CreateItem(0)
mail.To = emails.loc[emails['Loja']=='Diretoria','E-mail'].values[0] # type: ignore
mail.Subject = f"Ranking Dia {indicador_dia.day}/{indicador_dia.month}"
mail.Body = f'''
Prezados, bom dia.

Melhor loja do Dia em faturamento: Loja {faturamento_lojas_dia.index[0]} com faturamento R${faturamento_lojas_dia.iloc[0,0]:.2f}.
Pior loja do Dia em faturamento: Loja {faturamento_lojas_dia.index[-1]} com faturamento R${faturamento_lojas_dia.iloc[-1,0]:.2f}.

Melhor loja do Ano em faturamento: Loja {faturamento_lojas_ano.index[0]} com faturamento R${faturamento_lojas_ano.iloc[0,0]:.2f}.
Pior loja do Ano em faturamento: Loja {faturamento_lojas_ano.index[-1]} com faturamento R${faturamento_lojas_ano.iloc[-1,0]:.2f}.

Segue em anexo os rankings dos faturamentos das lojas do dia {indicador_dia.day}/{indicador_dia.month} e do ano {indicador_dia.year}.

Qualquer dúvida estou a disposição.

Att., Albino Marques
'''

attachment = pathlib.Path.cwd() / caminho_backup / f'{indicador_dia.day}_{indicador_dia.month}_Ranking_Anual.xlsx'
mail.Attachments.Add(str(attachment))
attachment = pathlib.Path.cwd() / caminho_backup / f'{indicador_dia.day}_{indicador_dia.month}_Ranking_Diario.xlsx'
mail.Attachments.Add(str(attachment))

mail.Send()


