from flask import Flask
import dash
from dash import html, dcc, Output, Input
import plotly.express as px
import data 

# Initialize Flask and Dash
server = Flask(__name__)
app = dash.Dash(__name__, server=server)

# Dashboard layout with headers, filters and graph
app.layout = html.Div([
    html.H1('Service Revenue and Costs Dashboard'),

    html.Label('Select Line of Business:'),
    dcc.Dropdown(
        id='line-of-business-filter',
        options=[{'label': i, 'value': i} for i in data.df_grouped['Line Of Business'].unique()],
        value=data.df_grouped['Line Of Business'].unique(),
        multi=True
    ),

    dcc.Graph(id='revenue-costs-graph')
])

# List of months with index for ordering the month axis in the graph and create a column to map order
month_order = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
               'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

data.df_grouped['MonthOrder'] = data.df_grouped['Month'].map(month_order)

# Graph's callback 
@app.callback(
    Output('revenue-costs-graph', 'figure'),
    [Input('line-of-business-filter', 'value')])
def update_graph(selected_lines_of_business):
    # Filter and sort the dataframe
    filtered_df = data.df_grouped[data.df_grouped['Line Of Business'].isin(selected_lines_of_business)].sort_values(by='MonthOrder')

    # Create the figure with two lines, blue for Revenue and red for Costs
    fig = px.line(filtered_df, x='Month', y=['Revenue', 'Costs'],
                  color_discrete_map={'Revenue': 'blue', 'Costs': 'red'},
                  title='Monthly Revenue and Costs')

    # Update the legend
    fig.update_layout(
        showlegend=True,
        legend_title_text='Category',
        legend=dict(
            traceorder='normal',
            font=dict(
                size=12,
            ),
        )
    )

    # Update the colors of the legend items
    fig.for_each_trace(lambda t: t.update(name=t.name.replace('=', ': '),
                                          legendgroup=t.name,
                                          marker=dict(color=t.marker.color)))

    return fig


# Run the Flask app
if __name__ == '__main__':
    app.run_server(debug=True)
