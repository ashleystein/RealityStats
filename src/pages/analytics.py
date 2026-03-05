import dash
import pandas as pd
from dash import html
import dash_ag_grid as dag

dash.register_page(__name__, path='/')

# Sample Data
df = pd.read_csv('/Users/ashilys/Desktop/RealityStats/data/reality_contestants.csv')
new_df = pd.DataFrame(columns=['Contestant', 'Show', 'Season', 'Instagram Id', 'IG Follower Count'])
new_df[['Contestant', 'Show']] = df[['name', 'show']]


layout = html.Div([
    html.H1("Site Analytics Table"),
    dag.AgGrid(
        id="my-table",
        rowData=new_df.to_dict("records"),      # The data
        columnDefs=[{"field": i} for i in new_df.columns], # The headers
        columnSize="sizeToFit",
        dashGridOptions={"pagination": True}, # Adds page navigation to table
    )
])