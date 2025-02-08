import os
import json
import requests
import argparse
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px

class StockAnalyzer:
    def __init__(self, ticker1: str, ticker2: str = None):
        """Inicializa a classe carregando a chave da API e o ticker informado."""
        load_dotenv()
        self.api_key = os.getenv("API_KEY")
        self.ticker1 = ticker1.upper()
        self.ticker2 = ticker2.upper() if ticker2 else None
        self.data = {}
        self.cleaned_data = {}

    def get_dataset(self, ticker):
        """Obtém os dados da API ou carrega os dados mockados se houver erro."""
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={self.api_key}'
        
        r = requests.get(url)
        data = r.json()

        if "Error Message" in data:
            print("⚠️ Nome do ticker inválido ou API Key incorreta. Tente novamente.\n")
            return None
        elif "Information" in data:
            print("🔴 Limite de requisições diárias atingido. Carregando dados mockados para AAPL...")
            with open("./mocks/AAPL_data.json") as file:
                data = json.load(file)

        self.data[ticker] = data
        return self.data

    def format_and_clean_dataset(self, ticker):
        """Formata e limpa os dados do JSON para um DataFrame do Pandas."""
        if not self.data:
            print("Nenhum dado carregado. Execute `get_dataset()` primeiro.")
            return None

        df = pd.DataFrame(self.data[ticker]['Time Series (Daily)']).transpose()
        df.columns = ["Open", "High", "Low", "Close", "Volume"]

        # Convertendo colunas para valores numéricos
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df.dropna(inplace=True)  # Remove linhas com valores nulos
        self.cleaned_data[ticker] = df
        return df

    def calculate_metrics(self, ticker):
        """Calcula métricas estatísticas dos retornos diários."""
        if self.cleaned_data[ticker] is None:
            print("⚠️ Dados não estão limpos. Execute `format_and_clean_dataset()` primeiro.")
            return None

        self.cleaned_data[ticker]['Daily_Return'] = self.cleaned_data[ticker]["Close"].pct_change()

        metrics = {
            "Média dos retornos diários": self.cleaned_data[ticker]['Daily_Return'].mean(),
            "Desvio padrão": self.cleaned_data[ticker]['Daily_Return'].std(),
            "Mediana dos retornos diários": self.cleaned_data[ticker]['Daily_Return'].median(),
            "Maior retorno diário": self.cleaned_data[ticker]['Daily_Return'].max(),
            "Menor retorno diário": self.cleaned_data[ticker]['Daily_Return'].min(),
        }
        
        for key, value in metrics.items():
            print(f"{key}: {value:.5f}")
        
        return metrics

    def plot_stock_prices(self, ticker):
        """Gera um gráfico do preço de fechamento da ação."""
        if self.cleaned_data[ticker] is None:
            print("⚠️ Dados não estão limpos. Execute `format_and_clean_dataset()` primeiro.")
            return None

        fig = px.line(self.cleaned_data[ticker], x=self.cleaned_data[ticker].index, y='Close', 
                      title=f'Preço de Fechamento da Ação {self.ticker1}')
        fig.show()

    def plot_cumulative_return(self, ticker):
        """Gera um gráfico do retorno acumulado da ação."""
        if self.cleaned_data[ticker] is None:
            print("⚠️ Dados não estão limpos. Execute `format_and_clean_dataset()` primeiro.")
            return None

        self.cleaned_data[ticker]['Cumulative_Return'] = (1 + self.cleaned_data[ticker]['Close'].pct_change()).cumprod()

        fig = px.line(self.cleaned_data[ticker], x=self.cleaned_data[ticker].index, y='Cumulative_Return', 
                      title=f'Retorno Diário Acumulado da Ação {self.ticker1}')
        fig.show()

    def save_query_in_csv(self, ticker):
        self.cleaned_data[ticker].reset_index(inplace=True)
        df = self.cleaned_data[ticker].rename(columns={"index": "Date"})
        df.to_csv(f'data/{self.ticker1}_data.csv', encoding='utf-8', index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analisador de ações")

    parser.add_argument("ticker1", type=str, help="Nome do ticker1 (ex: AAPL, GOOGL, TSLA)")

    parser.add_argument(
        "--ticker2",
        type=str,
        help="Nome do ticker2 (ex: AAPL, GOOGL, TSLA)"
    )

    parser.add_argument(
        "--save",
        action="store_true",
        help="Acionar o salvamento do dataset em CSV"
    )

    args = parser.parse_args()

    analyzer = StockAnalyzer(args.ticker1, args.ticker2)
    analyzer.get_dataset(args.ticker1)
    analyzer.format_and_clean_dataset(args.ticker1)

    if args.save:
        analyzer.save_query_in_csv(args.ticker1)

    analyzer.calculate_metrics(args.ticker1)
    analyzer.plot_stock_prices(args.ticker1)
    analyzer.plot_cumulative_return(args.ticker1)

    if args.ticker2:
        analyzer.get_dataset(args.ticker2)
        analyzer.format_and_clean_dataset(args.ticker2)

        if args.save:
            analyzer.save_query_in_csv(args.ticker2)

        analyzer.calculate_metrics(args.ticker2)
        analyzer.plot_stock_prices(args.ticker2)
        analyzer.plot_cumulative_return(args.ticker2)
