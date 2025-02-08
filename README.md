# Automacao Financeira

Este projeto está em desenvolvimento.

## Descrição
O **StockAnalyzer** é uma ferramenta desenvolvida em Python para obter e analisar dados históricos de ações. Ele utiliza a API da Alpha Vantage para coletar informações de preços diários e fornece métricas estatísticas e visualizações interativas dos dados.

## Funcionalidades
- Obtenção de dados históricos de ações via API.
- Tratamento e limpeza dos dados para análise.
- Cálculo de métricas estatísticas dos retornos diários.
- Geração de gráficos interativos para análise do preço de fechamento e retorno acumulado.

## Requisitos
- Python 3.x
- Bibliotecas: `requests`, `pandas`, `plotly`, `dotenv`

## Como Usar
1. Clone o repositório:
   ```sh
   git clone https://github.com/seu-usuario/AutomacaoFinanceira.git
   cd AutomacaoFinanceira
   ```
2. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```
3. Configure sua chave da API Alpha Vantage em um arquivo `.env`:
   ```
   API_KEY=seu_token_aqui
   ```
4. Execute o script:
   ```sh
   python main.py
   ```

## Observação
Caso o limite de requisições da API seja atingido, será carregado um conjunto de dados mockado para análise.

## Status do Projeto
🚧 **Em desenvolvimento** 🚧

Futuramente, mais funcionalidades serão adicionadas para melhorar a experiência e a precisão das análises.

