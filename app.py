import dash
from flask import Flask
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.plotly as py
import pandas as pd
import numpy as np
import plotly
import time



server = Flask(__name__)
server.secret_key = os.environ.get('secret_key', 'secret')
app = dash.Dash(name = __name__, server = server)
app.config.supress_callback_exceptions = True




plotly.tools.set_credentials_file(username='nassimppcmarketer@gmail.com', api_key='8K3odOzrKSx6pmaP8ubP')

# x = np.random.randn(500)
# data = [go.Histogram(x=x)]

# py.iplot(data, filename='basic histogram')



#Graph Style
graph_style={'backgroundColor':'black', 'border-style': 'solid', 'border-color': 'white', 'margin-top':'10'}


mapbox_access_token='pk.eyJ1IjoibmFzc2ltMjgiLCJhIjoiY2p1bzFza3E2MDhuMjQzc2o4dW85ZWZndiJ9.wlgnuyzjaaZM0ecOgZ2FKw'
text_color='#eaeaea'
#catégorisation (pour le filtrage par pays)
pays={
    'France':['Lyon','Paris','Toulouse','Marseille'],
    'Italie':['Rome','Milan','Turin'],
    'All':['Lyon','Paris','Toulouse','Marseille','Rome','Milan','Turin']
}



#nested dictionnary for data
data={
    'Lyon':{'x':[i for i in range (15)],'y':list(abs(np.random.randn(15)*100)), 'lat':45.75 , 'long':4.85},
    'Paris':{'x':[i for i in range (15)],'y':list(abs(np.random.randn(15)*100)), 'lat':48.8534, 'long':2.3488},
    'Toulouse':{'x':[i for i in range (15)],'y':list(abs(np.random.randn(15)*100)), 'lat':43.6043, 'long':1.4437},
    'Marseille':{'x':[i for i in range (15)],'y':list(abs(np.random.randn(15)*100)), 'lat':43.3 , 'long':5.4},

    'Rome':{'x':[i for i in range (15)],'y':list(abs(np.random.randn(15)*100)), 'lat':41.9 , 'long':12.4833},
    'Milan':{'x':[i for i in range (15)],'y':list(abs(np.random.randn(15)*100)), 'lat':45.4612 , 'long':9.1878},
    'Turin': {'x': [i for i in range (15)], 'y':list(abs(np.random.randn(15)*100)), 'lat':45.05 , 'long':7.6667},
}


#Style bootstrap pour le layout grid (rows & columns)
app.css.append_css({'external_url': 'https://codepen.io/nassim28/pen/jRxxNN.css'})  # noqa: E501


app.scripts.config.serve_locally = True


app.layout = html.Div([
                html.Div([


                        # First ROW
                        html.Div([



                                html.Div([
                                    html.H4('DASH APP', style={'color':text_color})
                                ], className='two columns'),


                            html.Div([
                                html.P('Villes : ', style={'color':text_color}),
                                dcc.Checklist(
                                    id='Villes',
                                    options=[{'label': i, 'value': i} for i in data.keys()],
                                    values=['Lyon','Paris','Toulouse','Marseille','Rome','Milan','Turin'],
                                    labelStyle={'display': 'inline-block'}
                                )
                            ],
                            className='four columns',
                            style={'margin-top':'20', 'color':text_color}
                            ),

                            html.Div([
                                html.P("Pays", style={'color':text_color}),
                                dcc.RadioItems(
                                    id='Pays',
                                    options=[{'label': i, 'value': i} for i in pays.keys()],
                                    labelStyle={'display': 'inline-block'},
                                    value='All'

                                )


                            ],
                        className='four columns',
                        style = {'margin-top': '20','color':text_color}
                        ),

                            html.Div([
                              html.Button(id='valider', n_clicks=0, children='valider', style={'fontSize':12, 'color':text_color})


                            ],
                                className='two columns',
                                style={'margin-top': '20'}
                            ),
                        ],
                        className='row'),




                        #Div numéro 2
                        html.Div([

                            html.Div([
                            dcc.Graph(
                                id='graph1',
                            ),
                        ], className='six columns',
                            style=graph_style),

                            html.Div([
                                dcc.Graph(
                                    id='graph2',
                                ),
                            ], className='six columns',
                            style=graph_style),

                        ]
                        ,className='row'
                        ),


                        # Div numéro 3
                        html.Div([

                            html.Div([
                                dcc.Graph(
                                    id='graph3',

                                    # style={'height': 500},

                                ),
                            ], className='four columns', style=graph_style),



                            #MAP graph
                            html.Div([
                                dcc.Graph(
                                    id='graph4',

                                ),
                            ], className='eight columns'
                            , style=graph_style),


                        ]
                            , className='row'
                        ),


                        html.Div([
                            html.Div(children = [
                                    dcc.Input(id="input-1", value='Input triggers local spinner'),
                                 dcc.Loading(id="loading-1", children=[html.Div(id="loading-output-1")], type="default"),])



                        ], className='row')

], className='ten columns offset-by-one',
)

], className='row', style={'backgroundColor':'black', 'height': '100000px !veryimportant' })


@app.callback(
        Output('Villes', 'options'),
        [Input('Pays', 'value')])
def update_check_boxes(selected_country):
    return [{'label': i, 'value': i} for i in pays[selected_country]]


@app.callback(
        Output('Villes', 'values'),
        [Input('Pays', 'value')])
def update_check_boxes(selected_country):
    values=pays[selected_country]
    return values




@app.callback(
    Output('graph1', 'figure'),
    [Input('valider', 'n_clicks')],
    [State('Villes', 'values')])
def update_graph1(n_clicks,selected_values):
    # arrange data to be digested by dcc.Graph()
    arranged_data = []
    for ville in selected_values:
        arranged_data.append({'x': data[ville]['x'], 'y': data[ville]['y'],
                              'type': 'line', 'name': ville})
    figure = {
        'data': arranged_data,
        'layout': {
            'margin' : go.layout.Margin(
                        l=0,
                        r=0,
                        b=0,
                        t=30,
                        pad=4
                    ),



            'title': 'Graph 1',

            'font' : dict(family='Courier New, monospace', size=15, color=text_color),
            'xaxis': dict(
                title='Temps',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=15,
                    color=text_color
                ),
                tickfont=dict(
                    family='Old Standard TT, serif',
                    size=15,
                    color=text_color
                ),

                showgrid=False
            ),
            'yaxis': dict(
                title='montant net TCC',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=15,
                    color=text_color
                ),
                tickfont=dict(
                    family='Old Standard TT, serif',
                    size=15,
                    color=text_color
                ),

                showgrid=False,


            ),
            'paper_bgcolor':'rgba(0,0,0,0)',
            'plot_bgcolor' :'rgba(0,0,0,0)',

        }
    }
    return figure


@app.callback(
    Output('graph2', 'figure'),
   [Input('valider', 'n_clicks')],
    [State('Villes', 'values')])
def update_graph2(n_clicks,selected_values):
    # arrange data to be digested by dcc.Graph()
    arranged_data = []
    for ville in selected_values:
        arranged_data.append({'x': data[ville]['x'], 'y': data[ville]['y'],
                              'type': 'bar', 'name': ville})
    figure = {
        'data': arranged_data,
        'layout': {
            'title': 'Graph 2',
            'font': dict(family='Courier New, monospace', size=15, color=text_color),
            'xaxis': dict(
                title='Temps',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=15,
                    color=text_color
                ),
                tickfont=dict(
                    family='Old Standard TT, serif',
                    size=15,
                    color=text_color
                ),
                showgrid=False,

            ),
            'yaxis': dict(
                title='montant net TCC',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=15,
                    color=text_color
                ),
                tickfont=dict(
                    family='Old Standard TT, serif',
                    size=15,
                    color=text_color
                ),
                showgrid=False,
                showline=True
            ),
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'rgba(0,0,0,0)'
        }
    }
    return figure


@app.callback(
        Output('graph3', 'figure'),
        [Input('valider', 'n_clicks')],
        [State('Villes','values')])
def update_graph3(n_clicks,selected_villes):
    x=[]
    for ville in selected_villes:
        x+=data[ville]['y']
    figure = go.Figure(
        data=[
            go.Histogram(x=x)
        ],
        layout=go.Layout(
            title='Distribution des revenus par jour',
            font = dict(family='Courier New, monospace', size=15, color=text_color),
            paper_bgcolor = 'rgba(0,0,0,0)',
            plot_bgcolor = 'rgba(0,0,0,0)'
        )
    )
    return figure


@app.callback(
    Output('graph4', 'figure'),
    [Input('valider', 'n_clicks')],
    [State('Villes', 'values')])
def update_graph4(n_clicks,selected_values):
    lat=[]
    long=[]
    text=[]
    ca=[]
    for ville in selected_values:
        lat.append(data[ville]['lat'])
        long.append(data[ville]['long'])
        text+=ville
        ca.append(sum(data[ville]['y'])*0.004)

    figure=go.Figure(
            data = [
                go.Scattermapbox(
                    lat=lat,
                    lon=long,
                    mode='markers',
                    marker=go.scattermapbox.Marker(
                        #size=9
                        size= ca,
                        sizeref = 0.1,
                        sizemin = 1,
                        sizemode = 'diameter'
                    ),
                    text=text,
                )
            ],

            layout = go.Layout(
                #autosize=True,
                height=400,
                hovermode='closest',
                mapbox=go.layout.Mapbox(
                    accesstoken=mapbox_access_token,
                    bearing=0,
                    center=go.layout.mapbox.Center(
                        lat=data['Paris']['lat'],
                        lon=data['Paris']['long']
                    ),
                    pitch=0,
                    zoom=3.1,
                    style='dark'
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=go.layout.Margin(
                    l=0,
                    r=0,
                    b=0,
                    t=0,
                    pad=4
                ),
            )
    )
    return figure


#Test Spinner
# @app.callback(Output("loading-output-1", "children"), [Input("input-1", "value")])
# def input_triggers_spinner(value):
#     time.sleep(5000)
#     return value

if __name__ == "__main__":
    app.run_server(debug=True)



















    # app.layout = html.Div([html.H4('Demo'),
    #                        html.Div([html.P('Chercher le numéro de société  ', style={'display': 'inline-block'}),
    #                                  dcc.Input(type='text', value='', id='input1'),
    #                                  dt.DataTable(
    #                                      rows=df.head(100).to_dict('records'),
    #                                      columns=sorted(df.columns),
    #                                      filterable=False,
    #                                      sortable=True,
    #                                      selected_row_indices=[],
    #                                      id='datatable'
    #                                  )])])
    #
    #
    # def filter(val):
    #     # """
    #     # For user selections, return the relevant in-memory data frame.
    #     # """
    #     # if clicks:
    #     #     if clicks % 2 == 1:
    #     #         df.sort_values('number', ascending=False, inplace=True)
    #     #     else:
    #     #         df.sort_values('number', ascending=True, inplace=True)
    #     return df.loc[df.P2NUM_VOIE == val]
    #
    #
    # @app.callback(Output('datatable', 'rows'), [Input('input1', 'value')])
    # def update(val):
    #     df = filter(val)
    #     return df.head(100).to_dict('records')
