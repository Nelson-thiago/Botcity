# Import for the Web Bot
from botcity.web import WebBot, Browser, By

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *

# --- Importado lib de data
from datetime import datetime

# --- Importado lib de data relativa (realizado o 'pip install python-dateutil')
from dateutil.relativedelta import relativedelta
import pandas as pd
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.drawing.image import Image

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False

from webdriver_manager.chrome import ChromeDriverManager

bot = WebBot()


# Função para obter as datas inicial e final (últimos 30 dias)
def obterDatas():
    dataFinal = datetime.today()
    dataInicio = dataFinal - relativedelta(months=1)
    dataFinalFormatada = dataFinal.strftime("%d/%m/%Y")
    dataInicioFormatada = dataInicio.strftime("%d/%m/%Y")

    return dataFinalFormatada, dataInicioFormatada

#Função para baixar o arquivo csv com as cotações
def ObterCotacoes(dataInicio,dataFinal):
    # Link para download do CSV com as datas
    linkDownload = (f"https://ptax.bcb.gov.br/ptax_internet/consultaBoletim.do?method=gerarCSVFechamentoMoedaNoPeriodo&ChkMoeda=61&DATAINI={dataInicio}&DATAFIM={dataFinal}")
    bot.browse(linkDownload)
    bot.wait(10000)
    bot.stop_browser()

# Função para recuperar o csv baixado
def RecuperarCSV(pathBot):
    caminho_CSV = bot.get_last_created_file(pathBot)
    print(caminho_CSV)
    bot.wait(3000)

    return caminho_CSV

# função para numear as colunas e retirar informções desnecessárias
def formatarDataframe(caminho_CSV):
    # Carregar o CSV baixado
    cotacoes_df = pd.read_csv(caminho_CSV, delimiter=';', encoding='latin1')
    # Renomear as colunas
    cotacoes_df.columns = ['Data', 'Codigo', 'Tipo', 'Simbolo', 'Cotacao_Compra', 'Cotacao_Venda', 'Fator_Conversao1', 'Fator_Conversao2']

    # Converter a coluna 'Data' para o formato datetime e formatar para pt-br
    cotacoes_df['Data'] = pd.to_datetime(cotacoes_df['Data'], format='%d%m%Y')
    cotacoes_df['Data'] = cotacoes_df['Data'].dt.strftime('%d/%m/%Y')
    
    # Substituir vírgulas por pontos nas colunas de cotação
    cotacoes_df['Cotacao_Compra'] = cotacoes_df['Cotacao_Compra'].str.replace(',', '.').astype(float)
    cotacoes_df['Cotacao_Venda'] = cotacoes_df['Cotacao_Venda'].str.replace(',', '.').astype(float)

    # Remover colunas desnecessárias
    cotacoes_df = cotacoes_df[['Data', 'Cotacao_Compra', 'Cotacao_Venda']]

    # Verificar e remover valores nulos
    cotacoes_df.dropna(inplace=True)
    print(cotacoes_df)

    return cotacoes_df

def salvarCsvFormatado(pathBot,df):
    # Obter a data final formatada para o nome do arquivo e salvar csv formatado
    dataFinal_formatada = datetime.today().strftime("%d_%m_%Y")
    nome_arquivo = f'/cotacoes_final_{dataFinal_formatada}.csv'
    nome_arquivo = pathBot + nome_arquivo
    df.to_csv(nome_arquivo, index=False, sep=';', encoding='utf-8')
    print(f"Arquivo salvo com sucesso: {nome_arquivo}")

# Função para carregar os dados do arquivo CSV
def carregar_dados(caminho_csv):
    df = pd.read_csv(caminho_csv, sep=';', encoding='utf-8')
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')

    return df

# Função para gerar o gráfico de cotação
def gerar_grafico(df):
    plt.figure(figsize=(10,6))
    # Plotando as linhas com um estilo diferente para melhor visualização
    plt.plot(df['Data'], df['Cotacao_Compra'], label='Cotação Compra', color='blue', linestyle='-', linewidth=2)
    plt.plot(df['Data'], df['Cotacao_Venda'], label='Cotação Venda', color='green', linestyle='--', linewidth=2)
    plt.xlabel('Data')
    plt.ylabel('Cotação (R$)')
    plt.title('Histórico da Cotação do Dólar')
    plt.xticks(rotation=45, ha='right', fontsize=10)  # Rotaciona as datas para não ficarem uma ecima 
    #plt.locator_params(axis='x', nbins=10)  # Limita o número de datas exibidas no eixo x
    plt.legend()
    plt.grid(True)

    # Salvando o gráfico
    caminho_grafico = 'grafico_cotacao_dolar.png'
    plt.tight_layout()  # Ajusta automaticamente os espaçamentos para evitar cortes
    plt.savefig(caminho_grafico, format='png')
    plt.close()

    return caminho_grafico

# Função para criar o relatório Excel e inserir o gráfico
def criar_relatorio_excel(df, caminho_grafico):
    wb = Workbook()
    ws = wb.active
    ws.title = "Cotacao Dolar"

    # Inserir os dados no Excel
    for i, coluna in enumerate(df.columns, 1):
        ws.cell(row=1, column=i, value=coluna)
    
    for row in df.itertuples(index=False):
        ws.append(row)

    # Inserir o gráfico no Excel
    img = Image(caminho_grafico)
    ws.add_image(img, 'E5')  # Posição para inserir o gráfico

    # Salvar o arquivo Excel
    caminho_relatorio = 'relatorio_cotacao_dolar.xlsx'
    wb.save(caminho_relatorio)

    return caminho_relatorio

def gerar_relatorio(df):
    caminho_grafico = gerar_grafico(df)
    caminho_relatorio = criar_relatorio_excel(df, caminho_grafico)

    print(f'Relatório gerado: {caminho_relatorio}')

def main():

    # Configurar o modo headless
    bot.headless = False

    bot.browser = Browser.CHROME
    bot.driver_path = ChromeDriverManager().install()
    pathBot = f"C:/Users/Nelson Thiago/Desktop/Area de Trabalho/Botcity/BotCotacao"

    dataFinal, dataInicio = obterDatas()
    print(dataFinal, dataInicio)

    ObterCotacoes(dataInicio,dataFinal)

    caminho_CSV = RecuperarCSV(pathBot)

    cotacoes_df = formatarDataframe(caminho_CSV)

    #salvarCsvFormatado(pathBot,cotacoes_df)

    gerar_relatorio(cotacoes_df)

def not_found(label):
    print(f"Element not found: {label}")

if __name__ == '__main__':
    main()
