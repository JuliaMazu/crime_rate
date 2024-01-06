import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import os


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

df = pd.read_csv('crime_pris')
df_fr = pd.read_csv('france_crime').set_index('Unnamed: 0')
crim_hom = pd.read_csv('convicted_guilty')


dico_text = {2020 : 'Conséquence de la pandémie de Covid-19 et des confinements : la délinquance a chuté en 2020, sauf pour ce qui concerne les violences intrafamiliales et sexuelles, lesquelles continuent d’augmenter',
             2015: "Lors de la « crise » de 2015, qui est surtout une crise de la solidarité entre pays européens face à l'accueil des réfugiés, la première difficulté d'une réponse solidaire a été le fait que les pays européens ont été inégalement confrontés à l'afflux d'immigrés et de demandeurs d'asile.",
             2009: "Lituaniens engloutissent 18,2 litres d’alcool pur par an, selon les données de l'Organisation mondiale de la santé (OMS). Ils sont les plus gros consommateurs d'alcool dans le monde.",
             2010: "Lituaniens engloutissent 18,2 litres d’alcool pur par an, selon les données de l'Organisation mondiale de la santé (OMS). Ils sont les plus gros consommateurs d'alcool dans le monde.",
             2011: "Lituaniens engloutissent 18,2 litres d’alcool pur par an, selon les données de l'Organisation mondiale de la santé (OMS). Ils sont les plus gros consommateurs d'alcool dans le monde.",
             2012: "Lituaniens engloutissent 18,2 litres d’alcool pur par an, selon les données de l'Organisation mondiale de la santé (OMS). Ils sont les plus gros consommateurs d'alcool dans le monde.",
             2013: "Lituaniens engloutissent 18,2 litres d’alcool pur par an, selon les données de l'Organisation mondiale de la santé (OMS). Ils sont les plus gros consommateurs d'alcool dans le monde.",
             2014: "Lituaniens engloutissent 18,2 litres d’alcool pur par an, selon les données de l'Organisation mondiale de la santé (OMS). Ils sont les plus gros consommateurs d'alcool dans le monde.",
             2016: "L'arrivée massive de migrants en Europe en 2015-2016 a souligné l'absence d'une politique migratoire européenne structurée et efficace.",
             2017: "La zone euro affiche un record de croissance en 2017. Les dix-neuf pays de la zone euro ont enregistré l'année dernière une hausse du PIB de 2,5 %, leur meilleure performance depuis 2007.",
             2021: '',
             2018: '',
             2019: '' 
             }

import plotly.express as px

app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("La carte criminalité d'Europe"), style={'textAlign': 'center', 'margin-bottom' : '30px'})),
    dbc.Row([
        dbc.Col([
            dbc.Row(html.H6('sex de criminel'), style={'margin-top' : '20px'}),
            dbc.Row(dcc.Dropdown(
                id='sex',
                options=[
                    {'label': 'Homme', 'value': 'M'},
                    {'label': 'Femme', 'value': 'F'},
                    {'label': 'General', 'value': 'T'}
                ],
                value='T')),  # valeur par défaut
            dbc.Row(html.H6('type de crime'), style={'margin-top' : '25px'}),
            dbc.Row(dcc.Dropdown(
                id='crime',
                options=[
                    {'label': 'Homicide intentionnel', 'value': 'ICCS0101'},
                    {'label': 'Agression sexuelle', 'value': 'ICCS03012'},
                    {'label': 'Viol', 'value': 'ICCS03011'}
                    ],
                value='ICCS0101'  # valeur par défaut
                        )),
            dbc.Row(html.H6("l'année d'interée"), style={'margin-top' : '25px'}),
            dbc.Row(dcc.Slider(id='year', min=2009, max=2021, step=1, value=2015, 
                               marks={i: '{}'.format(int(i)) for i in range(2008, 2022)}))
                 ]),
        dbc.Col(html.Img(src='/assets/legal-advice-technology-service-concept-with-businesswon-hand-working-with-modern-ui-computer.jpg', width='500', style={'margin-left' : '100px'}))
            ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='output-graph'), style={'margin-top' : '50px'}),
                dbc.Col(html.H5(id='output-text'), style={'margin-top' : '200px'})
            ]),
    dbc.Row(html.H3("L'évolution de taux criminalité en France"), style={'textAlign': 'center', 'margin-top': '50px'}),
    dcc.Graph(id='taux-France'), 
    dcc.Checklist(
        id="checklist",
        options=["Homme", "Femme", "Total", 'Intentional homicide', 'Rape', 'Sexual assault'],
        value=['Total', 'Rape'],
        inline=True), 
    dbc.Row(html.H3("La proportion des victime et des condamné en France"), style={'textAlign': 'center', 'margin-top': '50px', 'margin-bottom' : '25px'}),
    dbc.Row([dbc.Col(html.Img(src='/assets/5bac1c511f0000df002278b3.jpeg', width=450, style={'margin-top' : '60px'}), class_name='col1'),
            dbc.Col([dcc.Slider(id='year_proportion', min=2008, max=2021, step=1, value=2015, 
                               marks={i: '{}'.format(int(i)) for i in range(2008, 2022)}),
                    dcc.Graph(id='proportion'),
                    dcc.Checklist(id='checklist2',
                        options=['Homme', 'Femme', 'Total'],
                        value=['Total'],
                        inline=True)], class_name='col2')
            ])                         
    ]
)

@app.callback(
    [Output('output-graph', 'figure'),
     Output('output-text', 'children'),
     Output('taux-France', 'figure'),
     Output('proportion', 'figure')],
    [Input('sex', 'value'), Input('crime', 'value'), 
     Input('year', 'value'), Input('checklist', 'value'),
     Input('year_proportion', 'value'), Input('checklist2', 'value')]
)
def update_graph(value_sex, value_crime, value_year, france_sex, year_prop, sex_prop):
    mask = []
    if 'Homme' in france_sex:
        if 'Intentional homicide' in france_sex:
            mask.append('Intentional homicide male')
        if 'Rape' in france_sex:
            mask.append('Rape male')
        if 'Sexual assault' in france_sex:
            mask.append('Sexual assault male')
    if 'Femme' in france_sex:
        if 'Intentional homicide' in france_sex:
            mask.append('Intentional homicide fem')
        if 'Rape' in france_sex:
            mask.append('Rape fem')
        if 'Sexual assault' in france_sex:
            mask.append('Sexual assault fem')
    if 'Total' in france_sex:
        if 'Intentional homicide' in france_sex:
            mask.append('Intentional homicide')
        if 'Rape' in france_sex:
            mask.append('Rape')
        if 'Sexual assault' in france_sex:
            mask.append('Sexual assault')


    fig_line = px.scatter(df_fr[mask], labels={
                     "Unnamed: 0": "Année",
                     "value": "Pour cent mille habitants"
                     }, 
                     color='value', color_continuous_scale=px.colors.sequential.Blues_r,
                     trendline="ols", trendline_scope='trace',
                     trendline_color_override='white')
    fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend_font_color="white",
                           xaxis_showgrid=False, yaxis_showgrid=False)
    fig_line.update_traces(marker={'size': 15})
    fig_line.update_yaxes(title_font_color="white", color="white", title_font_size=18)
    fig_line.update_xaxes(title_font_color="white", color="white", title_font_size=18)



    fig_carte = px.choropleth(df[(df['unit']=='P_HTHAB') & (df['sex']==value_sex) & (df['iccs'] == value_crime)], locations="iso_alpha",
                    color=str(value_year) + " ", 
                    color_continuous_scale=px.colors.sequential.Redor, 
                    scope="europe")
                   # range_color=(0,0.4))
    fig_carte.update_layout(margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(1,1,1,1)')
    fig_carte.update_layout(legend_font_color="white")




    dico_sex = {'Total' : 'T', 'Femme' : 'F', 'Homme' : 'M'}
    mask_sex = dico_sex[sex_prop[0]]
    if len(mask_sex)>0:
        fig_bar = px.bar(crim_hom[(crim_hom['iso_alpha']=='FRA') & (crim_hom['sex']==mask_sex)], color='legal status', x='crime', y = str(year_prop)+' ', 
                     barmode='group', text_auto=True, color_discrete_sequence=['#990303', '#9c9999', '#71706e', '#292323'])
    else:
        fig_bar = px.bar(crim_hom[(crim_hom['iso_alpha']=='FRA')], color='legal status', x='crime', y = str(year_prop)+' ', 
                     barmode='group', text_auto=True, color_discrete_sequence=['#990303', '#9c9999', '#71706e', '#292323'])
    fig_bar.update_layout(margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    fig_bar.update_yaxes(title_font_color="white", color="white")
    fig_bar.update_xaxes(title_font_color="white", color="white")
    fig_bar.update_layout(legend_font_color="white")

    text = dico_text[value_year]

    return fig_carte, text, fig_line, fig_bar
    

if __name__ == '__main__':
    app.run(port=os.environ['PORT'])
