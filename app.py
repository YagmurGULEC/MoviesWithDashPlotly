# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc,Input, Output,State
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objects as go
app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


data=pd.read_csv('https://www.dropbox.com/s/phwy8nlf0e6dcr3/movies.csv?dl=1')
#remove the rows not having any information on the budget and revenue
selected_rows = data[(~data['Major Genre'].isnull())&(~data['Worldwide Gross'].isnull())&(~data['Production Budget'].isnull())&(data['Worldwide Gross']!="Unknown")&(data['US Gross']!="Unknown")&(~data['IMDB Rating'].isnull())&((~data['Rotten Tomatoes Rating'].isnull()))]
#convert the columns to float
selected_rows['Worldwide Gross']=selected_rows['Worldwide Gross'].astype(float)
selected_rows['US Gross']=selected_rows['US Gross'].astype(float)


Budget=selected_rows.groupby('Major Genre').mean()
fig3 = px.scatter_matrix(selected_rows,
    dimensions=['Production Budget','US Gross','Worldwide Gross','IMDB Rating','Rotten Tomatoes Rating'])
fig3.update_layout(
    title='Scatter Matrix Plot',
    width=1000,
    height=1000,
)

fig3.update_traces(diagonal_visible=False)

X=selected_rows[['Production Budget','US Gross','Worldwide Gross','IMDB Rating','Rotten Tomatoes Rating']]
X_scaled=X.apply(lambda r:(r-r.mean())/r.std(),axis=0)
Covariance=np.cov(X_scaled.T)
fig2 = px.imshow(Covariance,text_auto=True)
fig2.update_traces(showscale=False)
fig2.update_layout(
  
    yaxis = dict(
        tickmode = 'array',
        tickvals = [0, 1, 2, 3,4],
        ticktext = ['Production Budget','US Gross','Worldwide Gross','IMDB Rating','Rotten Tomatoes Rating']
    ),
    xaxis = dict(
        tickmode = 'array',
        tickvals = [0, 1, 2, 3,4],
        ticktext = ['Production Budget','US Gross','Worldwide Gross','IMDB Rating','Rotten Tomatoes Rating']
    ),
    
)


#Max=Budget[['Production Budget','Worldwide Gross']].max().max()
#Min=Budget[['Production Budget','Worldwide Gross']].min().min()

fig1 = px.scatter(selected_rows, x=selected_rows['Production Budget'], y=selected_rows['IMDB Rating'])
   

fig = go.Figure(data=[
    go.Bar(name='Budget', x=Budget.index, y=Budget['Production Budget']),
    go.Bar(name='Revenue', x=Budget.index, y=Budget['Worldwide Gross'])
])
fig.update_layout(barmode='group')







app.layout = dbc.Container(
    [
        dbc.Container([html.H3('Select columns'),dbc.Container([html.H5('X'),dcc.Dropdown(selected_rows.columns, 'Production Budget', id='dropdown_x')],className="col"),dbc.Container([html.H5('Y'),dcc.Dropdown(selected_rows.columns, 'IMDB Rating', id='dropdown_y')],className="col")],className="row"),
        dbc.Container(dcc.Graph(figure=fig1,id="plot"),className="row"),
        dbc.Container(dcc.Graph(figure=fig3,id="plot2"),className="row"),
        dbc.Container([html.H3('Correlation Matrix'),dcc.Graph(figure=fig2)],className="row"),
        dbc.Container([html.H3('Bugdet-Revenue Based on Genres'),dcc.Graph(figure=fig)],className="row"),
    ],
 
  className="text-center px-4",
)

@app.callback(
    Output('plot', 'figure'),
    Input('dropdown_x', 'value'),
    Input('dropdown_y', 'value')
)
def update_output(x,y):
    fig1 = px.scatter(selected_rows, x=x, y=y,color='Major Genre',size="Worldwide Gross")
    return fig1


if __name__ == '__main__':
    app.run_server(debug=False)
