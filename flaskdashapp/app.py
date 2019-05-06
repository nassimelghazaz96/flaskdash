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
from flaskdashapp import server
import time
from datetime import datetime as dt
import dateutil

# from keras.models import Sequential
# from keras.layers import LSTM
# from keras.layers import Dense
# import math
# import copy

from pylab import *
import base64
from fbprophet import Prophet



logout_img = "logout.png" # replace with your own image
encoded_image = base64.b64encode(open(logout_img, 'rb').read())

#Importation des données organisées
datasets={}
num_voies=[]

#######################Tabs Style###############

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'backgroundColor': 'black',
    'color': 'white',
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#5e0000',
    'color': 'white',
    'padding': '6px'
}

#################################################
for i in range (1,25):
    num_voies.append(i)
    df=pd.read_csv('CSVs/organized'+str(i)+'.csv', sep=';')
    df['P2HTU_TRANSACTION'] = pd.to_datetime(df['P2HTU_TRANSACTION'])
    datasets[str(i)]=df








# Importation des données
usecols=["P2NUM_VOIE", "P2HTU_TRANSACTION", "P2NUM_GARE","P2NUM_CLASSE_DAC", "P2NUM_GARE","P2NUM_CLASSE_PREDAC"]

df=pd.read_csv('output.csv', sep=';' ,error_bad_lines=False,nrows=1000,
                         low_memory=False,memory_map=True,usecols=usecols)

df = df[pd.notnull(df['P2HTU_TRANSACTION'])]
df['P2HTU_TRANSACTION'] = df['P2HTU_TRANSACTION'].apply(dateutil.parser.parse, dayfirst=True)

#Préparation des données pour les filtres
num_gares=list(df['P2NUM_GARE'].unique())
# num_voies= list(df['P2NUM_VOIE'].unique())
first_gare=num_gares[0]
first_voie=[num_voies[0]]





plotly.tools.set_credentials_file(username='nassimppcmarketer@gmail.com', api_key='8K3odOzrKSx6pmaP8ubP')
# mapbox_access_token='pk.eyJ1IjoibmFzc2ltMjgiLCJhIjoiY2p1bzFza3E2MDhuMjQzc2o4dW85ZWZndiJ9.wlgnuyzjaaZM0ecOgZ2FKw'
app = dash.Dash(__name__, sharing=True, server=server, url_base_pathname='/dashapp/')


######STYLE#########
#Graph Style
background_color_graph="#2d2d2d"
graph_style={'backgroundColor':'black', 'border-style': 'solid', 'border-color': 'white', 'margin-top':'10'}
text_color='#eaeaea'
#Style bootstrap pour le layout grid (rows & columns)
app.css.append_css({'external_url': 'https://codepen.io/nassim28/pen/jRxxNN.css'})  # noqa: E501

app.scripts.config.serve_locally = True


#####FUNCTIONS###################

#LSTM_splitter
def split_sequence(sequence, n_steps):
    X, y = list(), list()
    for i in range(len(sequence)):
        end_ix = i + n_steps
        if end_ix > len(sequence) - 1:
            break
        seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)


app.layout =  html.Div([
                 html.Div([
                        html.Div([
                            html.Div([

                                html.Img(
                                    src="https://upload.wikimedia.org/wikipedia/commons/1/17/APRR.svg",
                                    className='three columns',
                                    style={
                                        'height': '46%',
                                        'width': '46%',

                                        'position': 'relative',
                                        'padding-top': 30,
                                        'padding-right': 15,
                                        'margin-left':30
                                    },
                                ),
                            ], className='two columns'),

                            # Filtre Gare
                            html.Div([
                                html.P('N° Gare : ', style={'color': text_color, 'font-weight': 'bold', 'font-family':'"Courier New", Courier, monospace'}),
                                dcc.Dropdown(
                                    id='dropdown_gare',
                                    options=[
                                        {'label': num_gare, 'value': num_gare} for num_gare in num_gares

                                    ],
                                    value=first_gare,
                                    style={'height': 40,  'color':'black', 'width':150,'display': 'inline-block'},
                                    multi=False,

                                )
                            ],
                                className='two columns',
                                style={'margin-top': 5, 'color': text_color}
                            ),

                            # Filtre voie
                            html.Div([
                                html.P('N° VOIE : ', style={'color': text_color,'font-weight': 'bold'}),
                                dcc.Dropdown(
                                    id='dropdown_voie',
                                    options=[
                                        {'label': num_voie, 'value': num_voie} for num_voie in num_voies

                                    ],
                                    style={'color':'black', 'height':40},
                                    value=first_voie,
                                    multi=True,

                                )
                            ],
                                className='two columns',
                                style={'margin-top': 5, 'color': text_color, 'margin-left':50}
                            ),

                            html.Div([
                                html.Button(id='valider', n_clicks=0, children='valider',
                                            style={'fontSize': 12, 'margin-top': 30, 'color': text_color}),



                            ],
                                className='one columns',
                                style={'margin-top': 5, 'margin-left':50}
                            ),

                            html.Div([
                                html.A([
                                    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),style={
                                        'height': 40,
                                        'width': 40,
                                        'float':'right',
                                        'position': 'relative',
                                        'padding-top': 30,
                                        # 'padding-right': 15,
                                        # 'margin-left':30
                                    },),

                                ], href="/login")
                            ], className="three columns",style={'margin-top': 5, 'margin-left':50})






                        ],)



                    ], className='row', style={'background-color': '#8e1111', 'height':100} ),



##################Tabs bar##########################

                     html.Div([
                        dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
                            dcc.Tab(label='Transactions', value='tab-1', style=tab_style, selected_style=tab_selected_style),
                            dcc.Tab(label='Méthodes de Paiement', value='tab-2', style=tab_style, selected_style=tab_selected_style),
                            dcc.Tab(label="Modes d\'exploitations", value='tab-3', style=tab_style, selected_style=tab_selected_style),
                        ], style=tabs_styles),
                        html.Div(id='tabs-content-inline')
                    ]),








####################################################



    html.Div([


                html.Div([








                    ################################## Second ROW ############################################
                    html.Div([
                        html.Div([

                            dcc.Loading(
                                id="loading-1",
                                children=html.Div([html.Div([

                                    dcc.Graph(
                                        id="graph_nbtransac"
                                    )

                                ],)]),
                                type="circle",
                            )



                        ],className='twelve columns',style=graph_style
                        )
                    ],
                    className='row'),

                    ################################## Third ROW ############################################

                    html.Div([
                        html.Div([
                            dcc.Loading(
                                id="loading-2",
                                children=html.Div([html.Div([
                                    dcc.Graph(
                                        id="graph_nbcategoryvehicule"
                                    )
                                ])]),
                                type="circle",
                            ),
                        ],className='twelve columns',style=graph_style
                        )
                    ],
                    className='row'),


                    ################################## Fourth ROW ############################################


                    html.Div([

                        html.Div([




                        dcc.Loading(
                        id="loading-3",
                        children=html.Div([html.Div([
                            dcc.Graph(
                                id="graph_distribution"
                            )
                        ])]),
                        type="circle",
                            ),

                        ], className='twelve columns', style=graph_style
                        )


                    ],
                        className='row'),

                    ################################## Fifth ROW ############################################

                    # html.Div([
                    #
                    #     html.Div([
                    #
                    #         dcc.Loading(
                    #             id="loading-4",
                    #             children=html.Div([html.Div([
                    #                 dcc.Graph(
                    #                     id="graph_prev"
                    #                 )
                    #             ])]),
                    #             type="circle",
                    #         ),
                    #
                    #     ], className='twelve columns', style=graph_style
                    #     )
                    #
                    # ],
                    #     className='row'),


                    ###################################### Sixth ROW##############################################

                    html.Div([

                        html.Div([

                            dcc.Loading(
                                id="loading-5",
                                children=html.Div([html.Div([
                                    dcc.Graph(
                                        id="graph_moy_paiement1",

                                    )
                                ],)]),
                                type="circle",
                            ),

                        ], className='five columns', style=graph_style
                        ),

                        html.Div([

                            dcc.Loading(
                                id="loading-6",
                                children=html.Div([html.Div([
                                    dcc.Graph(
                                        id="graph_moy_paiement2"
                                    )
                                ])]),
                                type="circle",
                            ),

                        ], className='seven columns', style=graph_style
                        ),




                    ],
                        className='row'),





                    #######################SEVEnth ROW#########################################################

                    html.Div([

                        html.Div([

                            dcc.Loading(
                                id="loading-7",
                                children=html.Div([html.Div([
                                    dcc.Graph(
                                        id="graph_expl1"
                                    )
                                ])]),
                                type="circle",
                            ),

                        ], className='five columns', style=graph_style
                        ),

                        html.Div([

                            dcc.Loading(
                                id="loading-8",
                                children=html.Div([html.Div([
                                    dcc.Graph(
                                        id="graph_expl2"
                                    )
                                ])]),
                                type="circle",
                            ),

                        ], className='seven columns', style=graph_style
                        ),

                    ],
                        className='row'),

                    ####Forecasting Row ###############################################
                    html.Div([
                        html.Div([

                            dcc.Loading(
                                id="loading-9",
                                children=html.Div([html.Div([

                                    dcc.Graph(
                                        id="graph_prev"
                                    )

                                ], )]),
                                type="circle",
                            )

                        ], className='twelve columns', style=graph_style
                        )
                    ],
                        className='row'),















                ], style={'margin-left':20, 'margin-right':20 },
)

], className='row', style={'backgroundColor':'black', 'height': '100000px !veryimportant'})

],)


@app.callback([Output('graph_nbtransac','figure'),Output('graph_nbtransac','style')],
              [Input('valider','n_clicks'),  Input('tabs-styled-with-inline','value')],
              [State('dropdown_voie','value')])
def update_graph1(n_clicks,value,selected_values):
    arranged_data = []
    figure = {
        'data': arranged_data,
        'layout': {

            'title': 'Nombre de transactions',

            'font': dict(family='Courier New, monospace', size=15, color=text_color),
            'xaxis': dict(
                title='Temps',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=15,
                    color=text_color
                ),
                tickfont=dict(
                    # family='Courier New, monospace',
                    size=15,
                    color=text_color
                ),

                showgrid=False,

                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label='1m',
                             step='month',
                             stepmode='backward'),

                        dict(count=6,
                             label='6m',
                             step='month',
                             stepmode='backward'),
                        dict(count=1,
                             label='YTD',
                             step='year',
                             stepmode='todate'),
                        dict(count=1,
                             label='1y',
                             step='year',
                             stepmode='backward'),
                        dict(step='all')
                    ], ), bgcolor='#000000',
                    bordercolor='#FFFFFF',
                    font=dict(size=11)
                ),

                rangeslider=dict(
                    visible=True
                ),
                tickangle=45,
            ),
            'yaxis': dict(
                title='Nombre de Transactions',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=15,
                    color=text_color
                ),
                tickfont=dict(
                    family='Courier New, monospace',
                    size=15,
                    color=text_color
                ),

                showgrid=False,

            ),
            'paper_bgcolor': background_color_graph,
            'plot_bgcolor': background_color_graph,

        }
    }
    if(value=='tab-1'):
        style={'display': 'block'}

        for value in selected_values:
            selected_data=datasets[str(int(value))]
            # s = pd.to_datetime(selected_data['P2HTU_TRANSACTION'])
            # ts= pd.DataFrame(selected_data).set_index('P2HTU_TRANSACTION').resample('D').size().reset_index(name='nbr_transac')
            arranged_data.append({'x': list(selected_data['P2HTU_TRANSACTION']),
                                  'y': list(selected_data['nbr_transac']),
                                  'type': 'line', 'name': 'voie N°'+str(value), 'line':dict(
                    shape="spline",
                    smoothing="2",), 'mode':'lines+markers','marker':dict(symbol='diamond-open')})



        return figure,style
    else:
        style = {'display': 'none'}

        return figure,style





@app.callback(Output('graph_nbcategoryvehicule','figure'),
              [Input('valider','n_clicks')],
              [State('dropdown_voie','value')])
def update_graph2(n_clicks,selected_values):
    categories = [0, 1, 2, 3, 4, 5, 'nan']
    make_datasets=[]
    arranged_data=[]
    if selected_values:
        if (len(selected_values)>1):
            for value in selected_values:
                make_datasets.append(datasets[str(int(value))])
            arranged=pd.concat((make_datasets))

            for categorie in categories:
                this = arranged[['P2HTU_TRANSACTION', 'cat' + str(categorie)]]
                ts = this.set_index(['P2HTU_TRANSACTION'])
                # ts.index = pd.to_datetime((ts.index))
                g_daily = ts.groupby(pd.Grouper(freq="D")).sum().reset_index()
                arranged_data.append({
                    'x': list(g_daily['P2HTU_TRANSACTION']), 'y': list(g_daily['cat' + str(categorie)]), 'type': 'line',
                    'name': 'categorie ' + str(categorie),
                    'line': dict(
                        shape="spline",
                        smoothing="2", ), 'mode': 'lines+markers', 'marker': dict(symbol='diamond-open')
                })




        else:
            arranged=datasets[str(int(selected_values[0]))]
            for categorie in categories:
                arranged_data.append({
                    'x': list(arranged['P2HTU_TRANSACTION']), 'y': list(arranged['cat' + str(categorie)]), 'type': 'line',
                    'name': 'categorie ' + str(categorie),
                    'line': dict(
                        shape="spline",
                        smoothing="2", ), 'mode': 'lines+markers', 'marker': dict(symbol='diamond-open')
                })



    figure = {
        'data': arranged_data,
        'layout': {

            'title': 'Nombre de vehicules par catégorie',

            'font': dict(family='Courier New, monospace', size=15, color=text_color),
            'xaxis': dict(
                title='Temps',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=15,
                    color=text_color
                ),
                tickfont=dict(
                    family='Courier New, monospace',
                    size=15,
                    color=text_color
                ),

                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label='1m',
                             step='month',
                             stepmode='backward'),

                        dict(count=6,
                             label='6m',
                             step='month',
                             stepmode='backward'),
                        dict(count=1,
                             label='YTD',
                             step='year',
                             stepmode='todate'),
                        dict(count=1,
                             label='1y',
                             step='year',
                             stepmode='backward'),
                        dict(step='all')
                    ], ), bgcolor='#000000',
                    bordercolor='#FFFFFF',
                    font=dict(size=11)
                ),

                rangeslider=dict(
                    visible=True
                ),
                tickangle=45,

                showgrid=False
            ),
            'yaxis': dict(
                title='Nombre de Transactions',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=15,
                    color=text_color
                ),
                tickfont=dict(
                    family='Courier New, monospace',
                    size=15,
                    color=text_color
                ),

                showgrid=False,

            ),
            'paper_bgcolor': background_color_graph,
            'plot_bgcolor': background_color_graph,

        }
    }

    return figure









@app.callback(Output('graph_distribution','figure'),
              [Input('valider','n_clicks')],
              [State('dropdown_voie','value')])
def update_graph3(n_clicks,selected_values):

        if selected_values:
            dist_voie = []
            for value in selected_values:
                arranged=datasets[str(int(value))]
                pre_dist = []
                for cat in list(arranged.columns[2:9]):
                    pre_dist.append({'cat_name': cat, 'value': arranged[cat].sum()})
                dist = []


                for i in range(len(pre_dist)-1):
                    for j in range(int(pre_dist[i]['value'])):
                        dist.append(pre_dist[i]['cat_name'])
                trace_withoutna = go.Histogram(
                    x=list(dist),
                    name='voie N°' + str(value),
                    opacity=0.75,
                )
                dist_voie.append(trace_withoutna)

                dist = []
                for i in range(len(pre_dist)):
                    for j in range(int(pre_dist[i]['value'])):
                        if(pre_dist[i]['cat_name']=='catnan'):
                             dist.append(7)
                        else:
                            dist.append(pre_dist[i]['cat_name'])

                trace_withna = go.Histogram(
                    x=list(dist),
                    name='voie N°' + str(value)+' avec NaN',
                    opacity=0.75,
                )
                dist_voie.append(trace_withna)

            figure = go.Figure(
                data=dist_voie,
                layout=go.Layout(
                    title='Distribution des catégorie de voitures',
                    font=dict(family='Courier New, monospace', size=15, color=text_color),
                    paper_bgcolor=background_color_graph,
                    plot_bgcolor=background_color_graph
                )
            )
            return figure






@app.callback(Output('graph_moy_paiement1','figure'),
              [Input('valider','n_clicks')],
              [State('dropdown_voie','value')])
def update_graph4(n_clicks,selected_values):
    make_datasets=[]
    if selected_values:
        if (len(selected_values) > 1):
            for value in selected_values:
                make_datasets.append(datasets[str(int(value))])
            arranged = pd.concat((make_datasets))
            categories_2 = list(arranged.columns[9:22])

        else:
            arranged = datasets[str(int(selected_values[0]))]
            categories_2 = list(arranged.columns[9:22])
    values=[]
    for categorie in categories_2:
        values.append(arranged[categorie].sum())

    data = [
        dict(
            type='pie',
            labels=categories_2,
            values=values,
            name='Production Breakdown',
            text=categories_2,  # noqa: E501
            hoverinfo="text+value+percent",
            textinfo="label+percent+name",
            hole=0.5,
            marker=dict(
                colors=['#fac1b7', '#a9bb95', '#92d8d8']
            ),
            domain={"x": [0, .45], 'y': [0.2, 0.8]},
        ),
    ]
    layout= dict(
            autosize=True,
            title =" Répartition des moyens de paiement",
            bgcolor = '#000000',
            bordercolor = '#FFFFFF',
            paper_bgcolor =background_color_graph,
            plot_bgcolor = background_color_graph,
            font=dict(color='white'),
            margins=dict(
                t=30,
                d=0
            ),
            legend = dict(
            font=dict(size='10'),
            bgcolor='rgba(0,0,0,0)'
        ),
    )


    figure = dict(data=data, layout=layout)
    return figure





@app.callback(Output('graph_moy_paiement2','figure'),
              [Input('valider','n_clicks')],
              [State('dropdown_voie','value')])
def update_graph5(n_clicks,selected_values):
    make_datasets = []

    if selected_values:
        if (len(selected_values) > 1):
            for value in selected_values:
                make_datasets.append(datasets[str(int(value))])
            arranged = pd.concat((make_datasets))
            categories_2 = list(arranged.columns[9:22])
            arranged_data_categories=[]
            for categorie in categories_2:
                this = arranged[['P2HTU_TRANSACTION', categorie]]
                ts = this.set_index(['P2HTU_TRANSACTION'])
                g_daily = ts.groupby(pd.Grouper(freq="D"))
                g_daily = g_daily.sum().reset_index()
                arranged_data_categories.append(g_daily)


        else:
            arranged = datasets[str(int(selected_values[0]))]
            categories_2 = list(arranged.columns[9:22])
            arranged_data_categories = []
            for categorie in categories_2:
                this = arranged[['P2HTU_TRANSACTION', categorie]]
                ts = this.set_index(['P2HTU_TRANSACTION'])
                g_daily = ts.groupby(pd.Grouper(freq="D"))
                g_daily = g_daily.sum().reset_index()
                arranged_data_categories.append(g_daily)

    arranged_data=[]

    for data in arranged_data_categories:
        arranged_data.append({
            'x': list(arranged['P2HTU_TRANSACTION']), 'y': list(data[data.columns[1]]), 'type': 'line',
            'name': data.columns[1],
            'line': dict(
                shape="spline",
                smoothing="2", ), 'mode': 'lines+markers', 'marker': dict(symbol='diamond-open')
        })



    figure = {
        'data': arranged_data,
        'layout': {

            'title': 'Transactions par catégorie de paiement',

            'font': dict(family='Courier New, monospace', size=15, color=text_color),
            'xaxis': dict(
                title='Temps',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=15,
                    color=text_color
                ),
                tickfont=dict(
                    # family='Courier New, monospace',
                    size=15,
                    color=text_color
                ),

                showgrid=False,

                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label='1m',
                             step='month',
                             stepmode='backward'),

                        dict(count=6,
                             label='6m',
                             step='month',
                             stepmode='backward'),
                        dict(count=1,
                             label='YTD',
                             step='year',
                             stepmode='todate'),
                        dict(count=1,
                             label='1y',
                             step='year',
                             stepmode='backward'),
                        dict(step='all')
                    ], ), bgcolor='#000000',
                    bordercolor='#FFFFFF',
                    font=dict(size=11)
                ),

                rangeslider=dict(
                    visible=True
                ),
                tickangle=45,
            ),
            'yaxis': dict(
                title='Nombre de Transactions',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=15,
                    color=text_color
                ),
                tickfont=dict(
                    family='Courier New, monospace',
                    size=15,
                    color=text_color
                ),

                showgrid=False,

            ),
            'paper_bgcolor': background_color_graph,
            'plot_bgcolor': background_color_graph,

        }
    }

    return figure




@app.callback(Output('graph_expl1','figure'),
              [Input('valider','n_clicks')],
              [State('dropdown_voie','value')])
def update_graph6(n_clicks,selected_values):
    make_datasets=[]
    if selected_values:
        if (len(selected_values) > 1):
            for value in selected_values:
                make_datasets.append(datasets[str(int(value))])
            arranged = pd.concat((make_datasets))
            categories_3 = list(arranged.columns[22:24])

        else:
            arranged = datasets[str(int(selected_values[0]))]
            categories_3 = list(arranged.columns[22:24])
    values=[]
    for categorie in categories_3:
        values.append(arranged[categorie].sum())

    data = [
        dict(
            type='pie',
            labels=categories_3,
            values=values,
            name='Répartition des modes exploitations',
            text=categories_3,  # noqa: E501
            hoverinfo="text+value+percent",
            textinfo="label+percent+name",
            hole=0.5,
            marker=dict(
                colors=['#fac1b7', '#a9bb95', '#92d8d8']
            ),
            domain={"x": [0, .45], 'y': [0.2, 0.8]},
        ),
    ]
    layout= dict(
            title =" Répartition des moyens de paiement",
            bgcolor = '#000000',
            bordercolor = '#FFFFFF',
            paper_bgcolor =background_color_graph,
            plot_bgcolor = background_color_graph,
            font=dict(color='white'),
            height= 350
    )
    figure = dict(data=data, layout=layout)
    return figure



















@app.callback(Output('graph_expl2','figure'),
              [Input('valider','n_clicks')],
              [State('dropdown_voie','value')])
def update_graph7(n_clicks,selected_values):
    make_datasets = []

    if selected_values:
        if (len(selected_values) > 1):
            for value in selected_values:
                make_datasets.append(datasets[str(int(value))])
            arranged = pd.concat((make_datasets))
            categories_3 = list(arranged.columns[22:24])

            arranged_data_categories=[]
            for categorie in categories_3:
                this = arranged[['P2HTU_TRANSACTION', categorie]]
                ts = this.set_index(['P2HTU_TRANSACTION'])
                g_daily = ts.groupby(pd.Grouper(freq="D"))
                g_daily = g_daily.sum().reset_index()
                arranged_data_categories.append(g_daily)


        else:
            arranged = datasets[str(int(selected_values[0]))]
            categories_3 = list(arranged.columns[22:24])
            arranged_data_categories = []
            for categorie in categories_3:
                this = arranged[['P2HTU_TRANSACTION', categorie]]
                ts = this.set_index(['P2HTU_TRANSACTION'])
                g_daily = ts.groupby(pd.Grouper(freq="D"))
                g_daily = g_daily.sum().reset_index()
                arranged_data_categories.append(g_daily)

    arranged_data=[]

    for data in arranged_data_categories:
        arranged_data.append({
            'x': list(arranged['P2HTU_TRANSACTION']), 'y': list(data[data.columns[1]]), 'type': 'line',
            'name': data.columns[1],
            'line': dict(
                shape="spline",
                smoothing="2", ), 'mode': 'lines+markers', 'marker': dict(symbol='diamond-open')
        })



    figure = {
        'data': arranged_data,
        'layout': {

            'title': 'Transactions par mode exploitation',

            'font': dict(family='Courier New, monospace', size=15, color=text_color),
            'xaxis': dict(
                title='Temps',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=15,
                    color=text_color
                ),
                tickfont=dict(
                    # family='Courier New, monospace',
                    size=15,
                    color=text_color
                ),

                showgrid=False,

                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label='1m',
                             step='month',
                             stepmode='backward'),

                        dict(count=6,
                             label='6m',
                             step='month',
                             stepmode='backward'),
                        dict(count=1,
                             label='YTD',
                             step='year',
                             stepmode='todate'),
                        dict(count=1,
                             label='1y',
                             step='year',
                             stepmode='backward'),
                        dict(step='all')
                    ], ), bgcolor='#000000',
                    bordercolor='#FFFFFF',
                    font=dict(size=11)
                ),

                rangeslider=dict(
                    visible=True
                ),
                tickangle=45,
            ),
            'yaxis': dict(
                title='Nombre de Transactions',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=15,
                    color=text_color
                ),
                tickfont=dict(
                    family='Courier New, monospace',
                    size=15,
                    color=text_color
                ),

                showgrid=False,

            ),
            'paper_bgcolor': background_color_graph,
            'plot_bgcolor': background_color_graph,

        }
    }

    return figure



























# @app.callback(Output('graph_prev','figure'),
#               [Input('valider','n_clicks')],
#               [State('dropdown_voie','value')])
# def update_graph4(n_clicks,selected_values):
#
#     import math
#     from keras.models import Sequential
#     from keras.layers import LSTM
#     from keras.layers import Dense
#     import copy
#     import pandas as pd
#     import numpy as np
#
#
#     selected_voie = df[df.P2NUM_VOIE == selected_values[-1]][['P2HTU_TRANSACTION']]
#
#     #Preparation sous-format de time series
#     ts = selected_voie.groupby(df.P2HTU_TRANSACTION.dt.floor('d')).size().reset_index(name='nbr_transac')
#     ts.index = ts.P2HTU_TRANSACTION
#     ts.drop('P2HTU_TRANSACTION', axis=1, inplace=True)
#
#
#
#
#
#     #Train Test Split
#     trainSize = math.floor(ts.shape[0] * 0.85)
#     train = ts[:trainSize]
#     test_data = ts[trainSize:]
#
#     #Preparation des données pour le LSTM
#
#     train_set = list(train.nbr_transac)
#
#     raw_seq = train_set
#     # Choix du nombre du LookBack (les pas)
#     n_steps =  (len(test_data) // 4)
#     # split inputs-outputs(target)
#     X, y = split_sequence(raw_seq, n_steps)
#     # reshape (préparation des données pour le LSTM)
#
#     # Problème univarié (donc 1 seul feature)
#     n_features = 1
#     print(X)
#     X = X.reshape((X.shape[0], X.shape[1], n_features))
#     # Definition du modèle avec un dropout non nul pour éviter l'overfitting
#     model = Sequential()
#     model.add(LSTM(100, activation='relu', input_shape=(n_steps, n_features), dropout=0.09))
#     model.add(Dense(1))
#     model.compile(optimizer='adam', loss='mse')
#     model.fit(X, y, epochs=5000, verbose=0)
#
#     # Préparation des données pour la visualisation des données réelles Vs données prédites
#
#     trainpred = copy.deepcopy(train_set)
#     predi = []
#     # demonstration des prédiction ()
#     for i in range(len(train_set) - n_steps):
#         x_input = np.array([[trainpred[i:i + n_steps]]])
#         x_input = x_input.reshape((1, n_steps, n_features))
#         predi.append(model.predict(x_input, verbose=0))
#
#
#
#     # Liste qui va contenir les données prédites par le modèle dans la base d'entraînement
#     prev = []
#     for i in range(len(train_set) - n_steps):
#         prev.append(float(predi[i]))
#
#     nexter = copy.deepcopy(train_set)
#     for i in range(len(test_data)):
#         x_input = np.array([[nexter[-n_steps:]]])
#         x_input = x_input.reshape((1, n_steps, n_features))
#         nexter.append(model.predict(x_input, verbose=0))
#
#     # Liste qui va contenir les données prédites par le modèle dans la base de test
#     prev2 = []
#     for i in range(len(train_set) - 1, len(train_set) + len(test_data) - 1):
#         prev2.append(float(nexter[i]))
#
#     testo = list(test_data.nbr_transac)
#     ##Préparation des données pour l'affichage
#
#     #training_set
#     train_data = pd.DataFrame(train_set, columns=['value'])
#     train_date = pd.DataFrame(list(ts.index[:trainSize]), columns=['date'])
#     train_data['date'] = train_date['date']
#
#     #Entraînement du modèle
#     prev_data = pd.DataFrame(prev, columns=['value'])
#
#
#     #testing_set
#     test_data = pd.DataFrame(testo, columns=['value'])
#     test_date = pd.DataFrame(list(ts.index[trainSize:]), columns=['date'])
#     test_data['date'] = test_date['date']
#
#     # Test du Modèle
#     prev2_data = pd.DataFrame(prev2, columns=['value'])
#
#
#     train_trace = go.Scatter(
#         x=list(train_data['date']),
#         y=list(train_data['value']),
#         mode='lines+markers',
#         name='training_data'
#     ),
#     prev_trace = go.Scatter(
#         x=list(train_data['date'])[n_steps:],
#         y=list(prev_data['value']),
#         mode='lines+markers',
#         name='LSTM_training'
#     ),
#     test_trace = go.Scatter(
#         x=list(test_data['date']),
#         y=list(test_data['value']),
#         mode='lines+markers',
#         name='test_data'
#     ),
#     prev2_trace = go.Scatter(
#         x=list(test_data['date']),
#         y=list(prev2_data['value']),
#         mode='lines+markers',
#         name='LSTM_test',
#         line=dict(
#             color=('rgb(22, 96, 167)'),
#             width=4,
#             dash='dot')
#     )
#     arranged_data = [train_trace ,prev_trace, test_trace, prev2_trace]
#
#     figure = go.Figure(
#         data=arranged_data,
#         layout=go.Layout(
#             title='Distribution des catégorie de voitures',
#             font=dict(family='Courier New, monospace', size=15, color=text_color),
#             paper_bgcolor=background_color_graph,
#             plot_bgcolor=background_color_graph
#         )
#     )
#
#
#
#
#     return figure
#








@app.callback(Output('dropdown_voie','value'),[Input('dropdown_gare','value')])
def change_voie(selected_gare):
    return list(df[df['P2NUM_GARE'] == selected_gare].P2NUM_VOIE.unique())



@app.callback(Output('graph_prev','figure'),
              [Input('valider','n_clicks')],
              [State('dropdown_voie','value')])
def update_graph8(n_clicks,selected_values):
    one_df=datasets[str(selected_values[-1])]
    trainSize=int(len(one_df)*0.90)
    one_df=one_df[['P2HTU_TRANSACTION','nbr_transac']]
    one_df.rename(index=str, columns={'P2HTU_TRANSACTION': 'ds', 'nbr_transac': 'y'}, inplace=True)
    one_df.y=np.log(one_df.y+2)
    one_df['floor']=1
    one_df['cap'] = 1500
    train_df=one_df[:trainSize+1]
    test_df = one_df[trainSize:]
    m = Prophet(changepoint_prior_scale=10)
    m.add_seasonality(name='mid-month', period=7, fourier_order=12)
    m.fit(train_df)
    portee=len(test_df)
    future = m.make_future_dataframe(periods=portee)
    future['floor'] = 1
    future['cap'] = 1500
    forecast = m.predict(future)


    # m2=Prophet(changepoint_prior_scale=50)
    # m2.fit(one_df)
    # portee2=10
    # future2=m2.make_future_dataframe(periods=portee2)
    # future2['floor'] = 1.5
    # future2['cap'] = 1500
    # forecast2 = m.predict(future2)













    trace_0 = {
        "x": one_df.ds,
        "y": np.exp(one_df.y)-2,
        "line": {
            "color": "blue",
            "shape": "spline",
            "width": 4
        },
        "mode": "lines",
        "name": "Données réelles",
        "type": "scatter",
        "xaxis": "x",
        "yaxis": "y"
    }
    trace0 = {
        "x": train_df.ds,
        "y": np.exp(train_df.y)-2,
        "line": {
            "color": "rgb(244, 65, 208)",
            "shape": "spline",
            "width": 4
        },
        "mode": "lines",
        "name": "Données d'entraînement",
        "type": "scatter",
        "xaxis": "x",
        "yaxis": "y"
    }
    trace1 = {
        "x": list(forecast.ds)[-portee-1:],
        "y": np.exp(np.array(forecast.yhat_lower)[-portee-1:])-2,
        "line": {
            "color": "rgb(224, 125, 127)",
            "shape": "spline",
            "width": 0.1
        },
        "mode": "lines",
        "showlegend": False,
        "type": "scatter",
        "name": "(bande inf)",
        "xaxis": "x",
        "yaxis": "y"
    }
    trace2 = {
        "x": list(forecast.ds)[-portee-1:],
        "y": np.exp(np.array(forecast.yhat_upper)[-portee-1:])-2,
        "fill": "tonexty",
        "line": {
            "color": "rgb(224, 125, 127)",
            "shape": "spline",
            "width": 0.1
        },
        "showlegend": False,
        "mode": "lines",
        "name": "(bande sup)",
        "type": "scatter",
        "xaxis": "x",
        "yaxis": "y"
    }
    trace3 = {
        "x": list(forecast.ds)[-portee-1:],
        "y": np.exp(np.array(forecast.yhat)[-portee-1:])-2,
        "line": {
            "color": "red",
            "shape": "spline",
            "width": 4,
            "dash": "dot",
        },
        "mode": "lines",
        "name": "test du modèle",
        "type": "scatter",
        "xaxis": "x",
        "yaxis": "y"
    }

    trace4 = {
        "x": list(forecast.ds)[:-portee],
        "y": np.exp(np.array(forecast.yhat)[:-portee])-2,
        "line": {
            "color": "orange",
            "shape": "spline",
            "width": 4
        },
        "mode": "lines",
        "name": "Entraînement du modèles",
        "type": "scatter",
        "xaxis": "x",
        "yaxis": "y"
    }
    trace5={
        "x": list(test_df.ds),
        "y": np.exp(np.array(test_df.y))-2,
        "line": {
            "color": "green",
            "shape": "spline",
            "width": 4
        },
        "mode": "lines",
        "name": "Données de Test",
        "type": "scatter",
        "xaxis": "x",
        "yaxis": "y"
    }

    # trace6 = {
    #     "x": list(forecast2.ds)[-portee2: ],
    #     "y": list(forecast2.yhat)[-portee2: ],
    #     "line": {
    #         "color": "red",
    #         "shape": "spline",
    #         "width": 4
    #     },
    #     "mode": "lines",
    #     "name": "prevision sur "+str(portee2)+ " unités de temps",
    #     "type": "scatter",
    #     "xaxis": "x",
    #     "yaxis": "y"
    # }






    data = [trace_0,trace0,trace3,trace4,trace5]
    figure = go.Figure(
        data=data,
       layout=go.Layout(
                    title='Prévisions du nombre de transactions',
                    font=dict(family='Courier New, monospace', size=15, color=text_color),
                    paper_bgcolor=background_color_graph,
                    plot_bgcolor=background_color_graph
                )

    )
    return figure




#Gestion d'affichage des Tabs

# @app.callback([Output('graph_prev','')],
#              )
# def display_manegr(value):
#     print(value)




















# @app.callback( Output("dropdown", "options"),
#          [Input('dropdown', 'options')],)
# def option():
#     option={str(i):i for i in range(5)}
#     return option



#
# @app.callback(
#         Output("loading-output-1", "children"),
#         [Input('valider', 'n_clicks')],
#         [State('graph1','figure')])
# def read_file(n_clicks,value):
#     chunksize = 10 ** 3
#     df = []
#     for chunk in pd.read_csv('output.csv', sep=';', nrows=3000, error_bad_lines=False, chunksize=chunksize,
#                              low_memory=False):
#         df.append(chunk)
#     df = pd.concat(df)
#     return df.shape






# @app.callback(Output("loading-output-1", "children"), [Input("input-1", "value")])
# def input_triggers_spinner(value):
#     time.sleep(5000)
#     return value















