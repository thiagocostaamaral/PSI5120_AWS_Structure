from flask import Flask, render_template
import plotly.graph_objs as go
import plotly.offline as pyo
import datetime
import numpy as np  # Import numpy to calculate mean
import requests

# Simulated API response
session = requests.Session()
var_url = 'https://9ks86gdmzd.execute-api.us-east-1.amazonaws.com/prod/var'
vars = session.get(var_url)

data = vars.json()
#data = {
#    'Items': [
#        {'value': 32.38, 'var_id': 3, 'time': 1725818749000, 'var_name': 'Temperature'},
#        {'value': 81.2, 'var_id': 10000, 'time': 1725818734000, 'var_name': 'Humidity'},
#        {'value': 87.6, 'var_id': 1, 'time': 1725818532000, 'var_name': 'Humidity'},
#        {'value': 27, 'var_id': 0, 'time': 1725811758000, 'var_name': 'Temperature'}
#    ]
#}

app = Flask(__name__)

@app.route('/')
def index():
    # Separate temperature and humidity data
    #temperature_data = [item for item in data['Items'] if item['var_name'] == 'Temperature']
    #humidity_data = [item for item in data['Items'] if item['var_name'] == 'Humidity']

    temperature_data = sorted([item for item in data['Items'] if item['var_name'] == 'Temperature'], key=lambda x: x['time'])
    humidity_data = sorted([item for item in data['Items'] if item['var_name'] == 'Humidity'], key=lambda x: x['time'])

    # Convert timestamps to readable datetime format
    def convert_time(epoch_time):
        return datetime.datetime.fromtimestamp(epoch_time / 1000.0)

    # Extract times and values
    temperature_times = [convert_time(item['time']) for item in temperature_data]
    temperature_values = [item['value'] for item in temperature_data]

    humidity_times = [convert_time(item['time']) for item in humidity_data]
    humidity_values = [item['value'] for item in humidity_data]

    # Calculate the mean values
    temperature_mean = '%.2f'%np.mean(temperature_values)
    humidity_mean = '%.2f'%np.mean(humidity_values)

    # Create Plotly traces for temperature and humidity
    temperature_trace = go.Scatter(x=temperature_times, y=temperature_values, mode='lines+markers', name='Temperature', line=dict(color='red'))
    humidity_trace = go.Scatter(x=humidity_times, y=humidity_values, mode='lines+markers', name='Humidity', line=dict(color='blue'))

    # Layout for the plots
    temperature_layout = go.Layout(title='Temperature Timeline', xaxis_title='Time', yaxis_title='Value', hovermode='closest')
    humidity_layout = go.Layout(title='Humidity Timeline', xaxis_title='Time', yaxis_title='Value', hovermode='closest')

    # Generate the figures
    temperature_figure = go.Figure(data=[temperature_trace], layout=temperature_layout)
    humidity_figure = go.Figure(data=[humidity_trace], layout=humidity_layout)

    # Generate the HTML divs with the plots
    temperature_graph_div = pyo.plot(temperature_figure, output_type='div')
    humidity_graph_div = pyo.plot(humidity_figure, output_type='div')

    return render_template('index.html', temperature_graph_div=temperature_graph_div, humidity_graph_div=humidity_graph_div, 
                           temperature_mean=temperature_mean, humidity_mean=humidity_mean)

if __name__ == '__main__':
    app.run(debug=True)