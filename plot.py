import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from db import Data

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
data = Data(db_name="time-logs", collection_name="logs-data")
dates = ["03-07-2021","04-07-2021","05-07-2021"]
username = "Salman"
timelogs = [data.load_time_logs()[date] for date in dates]
for timelog in timelogs:
    del timelog["id"]
    del timelog["date"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

df = pd.DataFrame({
    "Activity": list(timelogs[0].keys()) +list(timelogs[1].keys()) + list(timelogs[2].keys()),
    "Time Spent (mins)": [value["duration"] for value in timelogs[0].values()] + [value["duration"] for value in timelogs[1].values()] + [value["duration"] for value in timelogs[2].values()],
})
df["Time Spent (mins)"] = df["Time Spent (mins)"].astype(int)
df = df[df["Time Spent (mins)"]>0]
fig = px.bar(df, x="Activity", y="Time Spent (mins)", color="Activity")

app.layout = html.Div([
    html.H3('AutoTimer',style={'textAlign': 'center'}),
    html.Div('An automation solution to track screen activities',style={'textAlign': 'center'}),
    html.Div(f'User: {username}',style={'color': '#FFA500'}),
    html.Div(f'Date: {dates[0]} to  {dates[2]}',style={'color': '#FFA500'}),
    dcc.Graph(
        id='activity-logs',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)