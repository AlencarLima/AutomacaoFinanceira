import os
import json
import requests
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px

class StockAnalyzer:
    def __init__(self, ticker: str):
        """Inicializa a classe carregando a chave da API e o ticker informado."""
        load_dotenv()
        self.api_key = os.getenv("API_KEY")
        self.ticker = ticker.upper()
        self.data = None
        self.cleaned_data = None

    def get_dataset(self):
        """Obtém os dados da API ou carrega os dados mockados se houver erro."""
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={self.ticker}&apikey={self.api_key}'
        
        r = requests.get(url)
        data = r.json()

        if "Error Message" in data:
            print("⚠️ Nome do ticker inválido ou API Key incorreta. Tente novamente.\n")
            return None
        elif "Information" in data:
            print("🔴 Limite de requisições diárias atingido. Carregando dados mockados para IBM...")
            with open("./mocks/ibm_data.json") as file:
                data = json.load(file)
            self.ticker = "IBM"  # Atualiza o ticker para o mock
        self.data = data
        return data

    def format_and_clean_dataset(self):
        """Formata e limpa os dados do JSON para um DataFrame do Pandas."""
        if not self.data:
            print("Nenhum dado carregado. Execute `get_dataset()` primeiro.")
            return None

        df = pd.DataFrame(self.data['Time Series (Daily)']).transpose()
        df.columns = ["Open", "High", "Low", "Close", "Volume"]

        # Convertendo colunas para valores numéricos
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df.dropna(inplace=True)  # Remove linhas com valores nulos
        self.cleaned_data = df
        return df

    def calculate_metrics(self):
        """Calcula métricas estatísticas dos retornos diários."""
        if self.cleaned_data is None:
            print("⚠️ Dados não estão limpos. Execute `format_and_clean_dataset()` primeiro.")
            return None

        self.cleaned_data['Daily_Return'] = self.cleaned_data["Close"].pct_change()

        metrics = {
            "Média dos retornos diários": self.cleaned_data['Daily_Return'].mean(),
            "Desvio padrão": self.cleaned_data['Daily_Return'].std(),
            "Mediana dos retornos diários": self.cleaned_data['Daily_Return'].median(),
            "Maior retorno diário": self.cleaned_data['Daily_Return'].max(),
            "Menor retorno diário": self.cleaned_data['Daily_Return'].min(),
        }
        
        for key, value in metrics.items():
            print(f"{key}: {value:.5f}")
        
        return metrics

    def plot_stock_prices(self):
        """Gera um gráfico do preço de fechamento da ação."""
        if self.cleaned_data is None:
            print("⚠️ Dados não estão limpos. Execute `format_and_clean_dataset()` primeiro.")
            return None

        fig = px.line(self.cleaned_data, x=self.cleaned_data.index, y='Close', 
                      title=f'Preço de Fechamento da Ação {self.ticker}')
        fig.show()

    def plot_cumulative_return(self):
        """Gera um gráfico do retorno acumulado da ação."""
        if self.cleaned_data is None:
            print("⚠️ Dados não estão limpos. Execute `format_and_clean_dataset()` primeiro.")
            return None

        self.cleaned_data['Cumulative_Return'] = (1 + self.cleaned_data['Close'].pct_change()).cumprod()

        fig = px.line(self.cleaned_data, x=self.cleaned_data.index, y='Cumulative_Return', 
                      title=f'Retorno Diário Acumulado da Ação {self.ticker}')
        fig.show()

if __name__ == "__main__":
    ticker = input("Insira o nome de algum ticker (ex: AAPL, GOOGL, TSLA): ").strip().upper()

    analyzer = StockAnalyzer(ticker)
    analyzer.get_dataset()
    analyzer.format_and_clean_dataset()
    analyzer.calculate_metrics()
    analyzer.plot_stock_prices()
    analyzer.plot_cumulative_return()
