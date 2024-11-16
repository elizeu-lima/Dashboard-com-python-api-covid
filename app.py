from flask import Flask, render_template
import requests
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

# Função para buscar os dados da API
def get_data_from_api():
    url = "https://disease.sh/v3/covid-19/countries"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Função para processar os dados e criar gráficos
def create_charts():
    data = get_data_from_api()
    if data:
        # Convertendo para DataFrame
        df = pd.DataFrame(data)
        
        # Criando um gráfico de casos confirmados por país
        fig = px.bar(df, x='country', y='cases', title='COVID-19: Casos Confirmados por País')
        fig.update_layout(xaxis_title='País', yaxis_title='Casos Confirmados')
        
        # Renderizando o gráfico como HTML
        graph_html = pio.to_html(fig, full_html=False)
        return graph_html
    else:
        return "<p>Erro ao carregar dados da API.</p>"

# Rota principal para o dashboard
@app.route('/')
def index():
    chart = create_charts()
    return render_template('index.html', chart=chart)

if __name__ == '__main__':
    app.run(debug=True)
