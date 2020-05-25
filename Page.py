import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Output,Input,State
import plotly.graph_objs as go
from layout import html_layout

import datetime as dt
import pandas as pd

from twitterprocess import top_results

global yt_vid_comments
yt_vid_comments = []


from Youtube import search_vidid,all_cmt
from Senti import analyse_sentiment, pretty_txt


from Reddit import top_posts
from Reddit import to_id_list
from Reddit import mine_comments



#Ye Wala sbb Change karna hai...

# query="Donald Trump"
days = dt.timedelta(days=10)
end_date = dt.date.today()
begin_date = end_date - days

app = dash.Dash(__name__)

app.index_string = html_layout

tabs_styles = {
    'height': '44px',

}
tab_style = {
    'border': '3px solid #111111',
    'padding': '6px',
    'fontWeight': 'bold',
    'background':'#111111'
}

tab_selected_style = {
    'borderTop': '3px solid #000000',
    'borderBottom': '3px solid #282828',
    'color': '#ffffff',
    'padding': '6px',
    'fontWeight': 'bold',
    'background':'#282828'

}









app.layout = html.Div([
    dcc.Tabs(value='tab-0',children=
    [dcc.Tab(label='Home', value='tab-0', style=tab_style, selected_style=tab_selected_style, children=[
            html.P(""),
            html.H3("SentimentZION "),
            html.Div([html.H4("Know what the world thinks!"),
                    html.P("We at SentimentZION are focused to paint the true picture of the world for you. The information that is provided is mined from social media and analyzed by us, we provided an overview of data from websites like Youtube, Twitter, and Reddit about your topic for a relevant timeframe. This data is presented in a visual format that provides higher readability and ease of consumption."),
                    html.H4("So what am I seeing?"),
                    html.P("-- Youtube : 100 most relevant comments each from across 10 most popular videos, "),
                    html.P("for instance, 100x10=1000 comments !"),
                    html.P("-- Twitter: around 1000 most relevant tweets!"),
                    html.P("-- Reddit : 150 most relevant comments each from across 5 most active subreddits,  "),
                    html.P("for instance, 150x5=750 comments !"),
                    html.H4("What is the significance?"),
                    html.P("Most social networks project the views of the most vocal but a minority of users on their platforms, however, the majority of the users' opinion is not taken into consideration. We plan on providing a non-biased overview by mining each comment from various social media sites which returns a score on a scale of -1 to 1, which signifies the sentiments of people where '-1' being most negative sentiment i.e. people are unsatisfied with it and '+1' being most positive sentiment i.e. people are satisfied."),
                    html.P("Note: This data is changing every second and hence the results take time to analyze and convert this data into a consumable format so a little Patience will be appreciated")
                    ])

        ]),
        dcc.Tab(label='YouTube', value='tab-1', style=tab_style, selected_style=tab_selected_style, children=[
            html.Div([
                #html.Div(html.H1(children="Team Zion")),
                html.P(""),
                html.H3("Enter the term you want to analyse"),
                html.Div([
                    dcc.Input(
                        id = "yquery-input",
                        placeholder = "Enter the query you want to search",
                        type = "text",
                        value = "Covid19",
                        style={"margin-right": "15px"}
                    ),
                   html.Button('Submit', id='ysubmit-val', n_clicks=0),
                   html.P(""),
                ]),
                html.Div(
                    dcc.Graph(id="y-graph1", config={'displayModeBar': False})
                    ),
                html.P(""),
                html.Div(
                    dcc.Graph(id="y-graph2",)
                    ),
                html.P(""),
                html.Div(
                    dcc.Graph(id="y-graph3",)
                    ),
                html.P(""),
                html.Div(
                    dcc.Graph(id="y-graph4",)
                    )

            ])
        ]),
        dcc.Tab(label='Twitter', value='tab-2', style=tab_style, selected_style=tab_selected_style, children=[
            html.Div([
                #html.Div(html.H1(children="Team Zion")),
                html.P(""),
                html.H3("Enter the term you want to analyse"),
                html.Div([
                    dcc.Input(
                        id = "tquery-input",
                        placeholder = "Enter the query you want to search",
                        type = "text",
                        value = "Covid19",
                        style={"margin-right": "15px"}
                    ),

                   html.Button('Submit', id='tsubmit-val', n_clicks=0),
                   html.P(""),
                ]),
                html.Div(
                    dcc.Graph(id="t-graph1",)
                    ),
                html.P(""),
                html.Div(
                    dcc.Graph(id="t-graph2",)
                    ),
                html.P(""),
                html.Div(
                    dcc.Graph(id="t-graph3",)
                    ),
                html.P(""),
                html.Div(
                    dcc.Graph(id="t-graph4",)
                    )

            ])
        ]),
        dcc.Tab(label='Reddit', value='tab-3', style=tab_style, selected_style=tab_selected_style, children=[
            html.Div([
                #html.Div(html.H1(children="Team Zion")),
                html.P(""),
                html.H3("Enter the term you want to analyse"),
                html.Div([
                    dcc.Input(
                        id = "rquery-input",
                        placeholder = "Enter the query you want to search",
                        type = "text",
                        value = "Covid19",
                        style={"margin-right": "15px"}
                    ),

                   html.Button('Submit', id='rsubmit-val', n_clicks=0),
                   html.P(""),
                ]),
                html.Div(
                    dcc.Graph(id="r-graph1"),
                    ),
                html.P(""),
                html.Div(
                    dcc.Graph(id="r-graph2",)
                    ),
                html.P(""),
                html.Div(
                    dcc.Graph(id="r-graph3",)
                    ),
                html.P(""),
                html.Div(
                    dcc.Graph(id="r-graph4",)
                    )

            ])
        ]),
    ])
])




@app.callback(
    [dash.dependencies.Output("y-graph1","figure"),
    dash.dependencies.Output("y-graph2","figure"),
    dash.dependencies.Output("y-graph3","figure"),
    dash.dependencies.Output("y-graph4","figure")],
    [dash.dependencies.Input('ysubmit-val', 'n_clicks')],
    [dash.dependencies.State("yquery-input","value")])
def update_fig(n_clicks,input_value):
    videoid_list=search_vidid(begin_date, end_date, input_value)
    ansdf=all_cmt(videoid_list)
    ansdf = analyse_sentiment(ansdf,"comments")
    #answt = analyse_sentimentwt(ansdf,"comments")
    ansdf['Date'] = ansdf.apply(lambda row: str(row.CommentPublishDate).split("T", 1)[0], axis = 1)
    ansdf['RoundPolarity'] = round(ansdf['sentiment'],1)
    ansdf2 = ansdf.groupby('Date', as_index=False)[['sentiment']].sum()
    #yaha tkk toh bss dataframe creation hai jo tere paas hai
    data=[]
    trace_close = go.Scatter(x = list(ansdf2.Date),
                         y=list(ansdf2.sentiment),

                         name="Close"
                         )
    data.append(trace_close)
    figure1 = go.Figure(data)
    figure1.update_layout(
    title="Date-Wise Cumulative Sentiment Score Line Plot",
    xaxis_title="Date",
    yaxis_title="Cumulative Score",
    template='plotly_dark',
    plot_bgcolor= 'rgba(0, 0, 0, 0)'
    )

    data=[]
    trace_close = go.Scatter(x = list(ansdf.CommentPublishDate),
                         y=list(ansdf.sentiment),
                         mode='markers',
                         name='markers',
                         marker_color=ansdf['sentiment']
                         )

    data.append(trace_close)
    figure2 = go.Figure(data)
    figure2.update_layout(
    title="Date-Wise Sentiment Score Scatter Plot [negative(-1) to positive(+1)]",
    xaxis_title="Date",
    yaxis_title="(-ve) Sentiment Score (+ve)",
    template='plotly_dark',
    plot_bgcolor= 'rgba(0, 0, 0, 0)'
    )

    data=[]
    trace_close = go.Box(x = list(ansdf.Date),
                         y=list(ansdf.sentiment),
                         name="Close",
                         line=dict(color="#ff3333"))
    data.append(trace_close)
    figure3 = go.Figure(data)
    figure3.update_layout(
    title="Date-Wise Sentiment Score Box Plot [negative(-1) to positive(+1)]",
    xaxis_title="Date",
    yaxis_title="(-ve) Sentiment Score (+ve)",
    template='plotly_dark',
    plot_bgcolor= 'rgba(0, 0, 0, 0)'
    )

    data=[]
    trace_close = go.Pie(labels=list(ansdf.roundoff),
                         name="Close"
                         )
    data.append(trace_close)
    figure4 = go.Figure(data)
    figure4.update_layout(
    title="Pie-Chart",
    template='plotly_dark',
    plot_bgcolor= 'rgba(0, 0, 0, 0)'
    )

    return figure1, figure2, figure3, figure4

@app.callback(
    [dash.dependencies.Output("t-graph1","figure"),
    dash.dependencies.Output("t-graph2","figure"),
    dash.dependencies.Output("t-graph3","figure"),
    dash.dependencies.Output("t-graph4","figure")],
    [dash.dependencies.Input('tsubmit-val', 'n_clicks')],
    [dash.dependencies.State("tquery-input","value")])
def update_fig(n_clicks,input_value):
    andf = top_results(input_value)
    andf = analyse_sentiment(andf,"text")
    andf['Date'] = andf.apply(lambda row: str(row.timestamp).split(" ", 1)[0], axis = 1)
    andf['RoundPolarity'] = round(andf['sentiment'],1)
    andf2 = andf.groupby('Date', as_index=False)[['sentiment']].sum()
    # ansdf3 = ansdf.groupby('RoundPolarity', as_index=False)[['Likes']].sum()

    data=[]
    trace_close = go.Scatter(x = list(andf2.Date),
                         y=list(andf2.sentiment),
                         name="Close",
                         line=dict(color="#ff3333"))
    data.append(trace_close)
    figure1 = go.Figure(data)
    figure1.update_layout(
    title="Date-Wise Cumulative Sentiment Score Line Plot",
    xaxis_title="Date",
    yaxis_title="Cumulative Score",
    template='plotly_dark',
    plot_bgcolor= 'rgba(0, 0, 0, 0)'
    )

    data=[]
    trace_close = go.Scatter(x = list(andf.timestamp),
                          y=list(andf.sentiment),
                          mode='markers',
                          name="markers",
                          marker_color=andf['sentiment'])
    data.append(trace_close)
    figure2 = go.Figure(data)
    figure2.update_layout(
    title="Date-Wise Sentiment Score Scatter Plot [negative(-1) to positive(+1)]",
    xaxis_title="Date",
    yaxis_title="(-ve) Sentiment Score (+ve)",
    template='plotly_dark',
    plot_bgcolor= 'rgba(0, 0, 0, 0)'
    )

    data=[]
    trace_close = go.Box(x = list(andf.Date),
                         y=list(andf.sentiment),
                         name="Close",
                         line=dict(color="#ff3333"))
    data.append(trace_close)
    figure3 = go.Figure(data)
    figure3.update_layout(
    title="Date-Wise Sentiment Score Box Plot [negative(-1) to positive(+1)]",
    xaxis_title="Date",
    yaxis_title="(-ve) Sentiment Score (+ve)",
    template='plotly_dark',
    plot_bgcolor= 'rgba(0, 0, 0, 0)'
    )

    data=[]
    trace_close = go.Pie(labels=list(andf.roundoff),
                         name="Close"
                         )
    data.append(trace_close)
    figure4 = go.Figure(data)
    figure4.update_layout(
    title="Pie-Chart",
    template='plotly_dark',
    plot_bgcolor= 'rgba(0, 0, 0, 0)'
    )


    return figure1, figure2, figure3, figure4


@app.callback(
    [dash.dependencies.Output("r-graph1","figure"),
    dash.dependencies.Output("r-graph2","figure"),
    dash.dependencies.Output("r-graph3","figure"),
    dash.dependencies.Output("r-graph4","figure")],
    [dash.dependencies.Input('rsubmit-val', 'n_clicks')],
    [dash.dependencies.State("rquery-input","value")])
def update_fig(n_clicks,input_value):
    input_value = pretty_txt(input_value)
    df1=top_posts(input_value)
    list1=to_id_list(df1)
    comment=mine_comments(list1)
    comment=analyse_sentiment(comment,"comments")
    comment['Date'] = comment.apply(lambda row: str(row.c_date).split(" ", 1)[0], axis = 1)
    comment2 = comment.groupby('Date', as_index=False)[['sentiment']].sum()
    data=[]
    trace_close = go.Scatter(x = list(comment2.Date),
                         y=list(comment2.sentiment),
                         mode='lines',
                         name="Close",
                         line=dict(color="#ff3333"))
    data.append(trace_close)
    figure1 = go.Figure(data)
    figure1.update_layout(
    title="Date-Wise Cumulative Sentiment Score Line Plot",
    xaxis_title="Date",
    yaxis_title="Cumulative Score",
    template='plotly_dark',
    plot_bgcolor= 'rgba(0, 0, 0, 0)'
    )

    data=[]
    trace_close = go.Scatter(x = list(comment.c_date),
                          y=list(comment.sentiment),
                          mode='markers',
                          name="markers",
                          marker_color=comment['sentiment'])
    data.append(trace_close)
    figure2 = go.Figure(data)
    figure2.update_layout(
    title="Date-Wise Sentiment Score Scatter Plot [negative(-1) to positive(+1)]",
    xaxis_title="Date",
    yaxis_title="(-ve) Sentiment Score (+ve)",
    template='plotly_dark',
    plot_bgcolor= 'rgba(0, 0, 0, 0)'
    )

    data=[]
    trace_close = go.Box(x = list(comment.Date),
                         y=list(comment.sentiment),
                         name="Close",
                         line=dict(color="#ff3333"))
    data.append(trace_close)
    figure3 = go.Figure(data)
    figure3.update_layout(
    title="Date-Wise Sentiment Score Box Plot [negative(-1) to positive(+1)]",
    xaxis_title="Date",
    yaxis_title="(-ve) Sentiment Score (+ve)",
    template='plotly_dark',
    plot_bgcolor= 'rgba(0, 0, 0, 0)'
    )

    data=[]
    trace_close = go.Pie(labels=list(comment.roundoff),
                         name="Close"
                         )
    data.append(trace_close)
    figure4 = go.Figure(data)
    figure4.update_layout(
    title="Pie-Chart",
    template='plotly_dark',
    plot_bgcolor= 'rgba(0, 0, 0, 0)'
    )


    return figure1, figure2, figure3, figure4





if __name__ == "__main__":
    app.run_server(debug = True)
