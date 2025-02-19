import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

def parse_temperature_log(file_path):
    # Lists to store the data
    timestamps = []
    temperatures = []
    
    # Read the file line by line
    with open(file_path, 'r') as file:
        for line in file:
            # Skip empty lines
            if not line.strip():
                continue
                
            try:
                # Split the line into timestamp and temperature
                timestamp_str, temp_str = line.strip().split()
                
                # Parse timestamp
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d_%H:%M:%S')
                
                # Parse temperature (remove 'temp=' and '\'C')
                temperature = float(temp_str.split('=')[1].replace('\'C', ''))
                
                timestamps.append(timestamp)
                temperatures.append(temperature)
                
            except (ValueError, IndexError) as e:
                print(f"Skipping invalid line: {line.strip()}")
                continue
    
    # Create a DataFrame
    df = pd.DataFrame({
        'timestamp': timestamps,
        'temperature': temperatures
    })
    
    return df

def create_interactive_plot(df):
    # Create the figure
    fig = go.Figure()
    
    # Add the temperature trace
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['temperature'],
        mode='lines',
        name='Temperature',
        line=dict(color='red', width=2)
    ))
    
    # Update layout
    fig.update_layout(
        title='Temperature Over Time',
        xaxis_title='Date and Time',
        yaxis_title='Temperature (°C)',
        hovermode='x unified',
        showlegend=True
    )
    
    # Configure zoom and pan options without range slider
    fig.update_xaxes(rangeslider_visible=False)
    
    # Show the plot
    fig.show()

def main():
    # Replace with your file path
    file_path = '/home/chmamai/Documents/proxyconf/temperature.log'
    
    # Parse the data
    df = parse_temperature_log(file_path)
    
    # Create and display the interactive plot
    create_interactive_plot(df)

if __name__ == "__main__":
    main()
