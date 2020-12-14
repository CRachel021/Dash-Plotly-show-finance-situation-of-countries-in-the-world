import dash
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from map import world_map, debt_rank, top_10, finance


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

all_countries = finance['CountryName'].unique()
all_indicator = finance['IndicatorName'].unique()

app.layout = html.Div([
    html.H1('Total external debt stocks in global countries', style={'textAlign':'center','font-size': '35px','color':'#343434'}),
    html.Div([
        dcc.Graph(id='world_map',
                  figure = px.choropleth(debt_rank,locations='CountryCode',color='Value',projection='natural earth',
                                         title='Overall external debt stocks in countries',hover_name=debt_rank['CountryName'],
                                         color_continuous_scale=px.colors.sequential.Blues,range_color=(1,190)
                                                )
                         )
              ], className = 'twelve columns'),
    html.Div([
        html.Div('Compare any two countries in terms of finance situation',
                 style={'color':'#343434','margin-bottom':'10px','font-weight':'bold','font-size':'18px'}),
        dcc.Dropdown(id='country1', options=[{'label':i, 'value':i} for i in all_countries],
                     value='Brazil',style={'width': '50%','margin-bottom': '10px'}),
        dcc.Dropdown(id='country2', options=[{'label':i, 'value':i} for i in all_countries],
                     value='Zimbabwe',style={'width':'50%'}),
        html.Div('Select a metric to compare',
                 style={'color':'#343434','margin-top':'10px','font-weight':'bold','font-size': '18px'}),
        dcc.Dropdown(id='indicator',options=[{'label':i,'value':i} for i in all_indicator],
                     value='External debt stocks, total (DOD, current US$)',style={'width':'70%'}
                     )
        ], className='nine columns'

    ),
    html.Div([
        html.Div([dcc.Graph('one_grap')],className = 'six columns'),
        html.Div([dcc.Graph(
            id='top_debt',
            figure={
                'data':[{'x':top_10['CountryName'],'y':top_10['Value'],'type':'bar'}],
                'layout':
                dict(title=('Top 10 countries in terms of total external debt stocks'),
                     xaxis={'title':'Countries'},
                     yaxis={'title':'Ratings'}
                     )
            }
        )],className='six columns'),
        ],className='row')
    ])

@app.callback(Output(component_id='one_grap',component_property='figure'),
                     [Input(component_id='country1', component_property='value'),
                      Input('country2',component_property='value'),
                      Input('indicator','value')])

def fin_comp(country1,country2,indicator):
    fir = finance[finance.CountryName == country1]
    sec = finance[finance.CountryName == country2]
    fir_ind = fir[fir.IndicatorName == indicator]
    sec_ind = sec[sec.IndicatorName == indicator]
    fir_dic = {'x':fir_ind.Year,'y':fir_ind.Value,'name':country1}
    sec_dic = {'x':sec_ind.Year,'y':sec_ind.Value,'name':country2}
    return {
        'data':[fir_dic,sec_dic],
        'layout': dict(title='Comparing the finance situation in two countries',
            xaxis={'title':'Years'},
            yaxis={'title':'Value as per Indicator selection'}
        )
    }

if __name__=='__main__':
    app.run_server(debug=True, use_reloader=False)

