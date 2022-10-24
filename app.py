# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc,Input, Output,State
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, date
app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP,dbc.icons.BOOTSTRAP],meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])
server=app.server
app.config.suppress_callback_exceptions=True
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

data=pd.read_csv('https://www.dropbox.com/s/phwy8nlf0e6dcr3/movies.csv?dl=1')
#remove the rows not having any information on the budget and revenue
selected_rows = data[(~data['Major Genre'].isnull())&(~data['Worldwide Gross'].isnull())&(~data['Production Budget'].isnull())&(data['Worldwide Gross']!="Unknown")&(data['US Gross']!="Unknown")&(~data['IMDB Rating'].isnull())&((~data['Rotten Tomatoes Rating'].isnull()))]
#convert the columns to float
selected_rows['Worldwide Gross']=selected_rows['Worldwide Gross'].astype(float)
selected_rows['US Gross']=selected_rows['US Gross'].astype(float)
selected_rows['Production Budget']=selected_rows['Production Budget'].astype(float)
#date to year
selected_rows['Date'] = pd.to_datetime(selected_rows['Release Date'])

selected_rows['Date'] =selected_rows['Date'].apply(lambda x: x.year-100 if x.year>2020 else x.year)
selected_rows['Profit']=selected_rows['Worldwide Gross']-selected_rows['Production Budget']

fig1 = px.scatter(selected_rows, x=selected_rows['Production Budget'], y=selected_rows['IMDB Rating'])

fig3 = px.scatter_matrix(selected_rows,dimensions=['Production Budget','US Gross','Worldwide Gross','IMDB Rating','Rotten Tomatoes Rating','IMDB Votes','Date'])
fig3.update_layout(
    title='Scatter Matrix Plot',
    width=1500,
    height=1000,)
fig3.update_traces(diagonal_visible=False,showlowerhalf=False)

fig4=px.box(selected_rows,y='Production Budget',x='Major Genre',color='Major Genre',hover_data=["Title"])
fig5=px.box(selected_rows,y='Worldwide Gross',x='Major Genre',color='Major Genre',hover_data=["Title"])
fig6=px.scatter(selected_rows,x='Date',y='Production Budget')
fig7=px.scatter(selected_rows,x='Date',y='Worldwide Gross')
navbar = dbc.NavbarSimple(
    children=[
        
        html.A(
            dbc.NavItem(dbc.NavLink(html.H2(html.I(className="bi bi-linkedin me-2 m-3")))),
            href="https://www.linkedin.com/in/ya%C4%9Fmur-g%C3%BCle%C3%A7-a52111204/"
        ),
        html.A(
            dbc.NavItem(dbc.NavLink(html.H2(html.I(className="bi bi-github me-2 m-3")))),
            href="https://www.linkedin.com/in/ya%C4%9Fmur-g%C3%BCle%C3%A7-a52111204/"
        ),
       html.A(
            dbc.NavItem(dbc.NavLink(html.H2(html.I(className="bi bi-medium me-2 m-3")))),
            href="https://medium.com/@yagmurgulec89"
        ),
        
    ],
    brand="Created by Yagmur Gulec",
    brand_href="#",
    color="primary",
    dark=True,
)

app.layout = html.Div([
    navbar,
     dbc.Row([
        html.H1([html.I(className="bi bi-film me-2 m-3"),'Data Visualization for Movies Database',html.I(className="bi bi-film me-2 m-3")]),
        
        ],
    className="row text-center px-3 mt-3"),
    dcc.Tabs(id="tabs-example-graph", value='matrix', children=[
        dcc.Tab(label='Scatter Matrix Plot', value='matrix'),
        dcc.Tab(label='Select columns', value='select'),
        dcc.Tab(label='Bugdets of Genres', value='genre'),
        dcc.Tab(label='Profits in Time', value='profit'),
    ]),
    html.Div(id='tabs-content-example-graph')
])

@app.callback(Output('tabs-content-example-graph', 'children'),
              Input('tabs-example-graph', 'value'))
def render_content(tab):
    if tab == 'matrix':
        return html.Div([
        dbc.Row([
            html.H3([html.I(className="bi bi-film me-2 m-3"),'Which features are correlated?',html.I(className="bi bi-film me-2 m-3")]),
            dbc.Col(dbc.Card(dcc.Graph(figure=fig3,id="plot3")),width=12,className="col text-center"),
    ],
    className="row text-center px-3 mt-3 mb-3"),
        ])
    elif tab == 'select':
        return html.Div([
            dbc.Row([
        html.H3([html.I(className="bi bi-film me-2 m-3"),'3-D Scatter Plot with Selected Axis',html.I(className="bi bi-film me-2 m-3")]),
        dbc.Col(dbc.Card(dcc.Graph(figure=fig1,id="plot")),width=10),
        dbc.Col([
            dbc.Row([html.H5('Bubble size'),dcc.RadioItems(['Worldwide Gross', 'Production Budget'], 'Production Budget',id='size'),html.H5('X'),dcc.Dropdown(selected_rows.columns, 'Production Budget', id='dropdown_x')],className="text-center mb-3 px-3"),
            dbc.Row([html.H5('Y'),dcc.Dropdown(selected_rows.columns, 'IMDB Rating', id='dropdown_y')],className="text-center mb-3 px-3"),
        ],width=2)
        
        ],className="row text-center px-3 mt-3 mb-3"),
        ])
    elif tab == 'genre':
        return html.Div([
            dbc.Row([
        html.H3([html.I(className="bi bi-film me-2 m-3"),'Which genre is the cheapest and the most profitable?',html.I(className="bi bi-film me-2 m-3")]),
        dbc.Col(dbc.Card(dcc.Graph(figure=fig4,id="plot4")),width=12,className='col mb-3'),
        dbc.Col(dbc.Card(dcc.Graph(figure=fig5,id="plot5")),width=12,className='col mb-3'),
        #dbc.Col(dbc.Card(dcc.Graph(figure=fig6,id="plot6")),width=12,className='col mb-3'),
       
        
        ],className="row text-center px-3 mt-3 mb-3"),
        ])
    elif tab=='profit':
        return html.Div([
            dbc.Row([
        html.H3([html.I(className="bi bi-film me-2 m-3"),'Time-varying Profit of Cinema',html.I(className="bi bi-film me-2 m-3")]),
        dbc.Col(dbc.Card(dcc.Graph(figure=fig6,id="plot6")),width=12,className='col mb-3'),
        dbc.Col(dbc.Card(dcc.Graph(figure=fig7,id="plot7")),width=12,className='col mb-3'),
        #dbc.Col(dbc.Card(dcc.Graph(figure=fig6,id="plot6")),width=12,className='col mb-3'),
       
        
        ],className="row text-center px-3 mt-3 mb-3"),
        ])
        
@app.callback(
    Output('plot', 'figure'),
    Input('dropdown_x', 'value'),
    Input('dropdown_y', 'value'),
    Input('size', 'value'),
)
def update_output(x,y,size):
    fig1 = px.scatter(selected_rows, x=x, y=y,color='Major Genre',size=size)
    return fig1


if __name__ == '__main__':
    app.run_server(debug=True)
