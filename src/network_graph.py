import dash
import pandas as pd
from dash import html, dcc, Input, Output
import dash_cytoscape as cyto
import networkx as nx

class NetworkGraph:
    def __init__(self, r_nodes, r_edges):
        # 1. Create the NetworkX graph
        G = nx.Graph()

        # 2. Define your people (Nodes)
        self.n = r_nodes
        self.e = r_edges
        G.add_nodes_from(
            (node['data']['id'], node['data'])
            for node in r_nodes
        )

        G.add_edges_from(self.e)

        # Convert nodes to Cytoscape format
        nodes = r_nodes

        # Convert edges to Cytoscape format
        edges = [
            {'data': {'source': source, 'target': target}}
            for source, target in G.edges()
        ]
        #edges = []

        self.elements = nodes + edges

    def render_app(self):
        # 3. Initialize the Dash app
        app = dash.Dash(__name__)
        app.layout = html.Div([
            html.H1("Reality TV Network Visualization"),
            cyto.Cytoscape(
                id='cytoscape-graph',
                elements=self.elements,
                style={'width': '100%', 'height': '600px'},
                responsive=True,
                # 4. Choose a layout (Cytoscape handles the math for you)
                layout={
                    'name': 'cose',  # 'cose' is similar to NetworkX's spring_layout
                    'animate': True
                },
                # 5. Define the visual style (CSS-like)
                stylesheet=[
                    {
                        'selector': 'node',
                        'style': {
                            'label': 'data(label)',
                            'background-color': 'SkyBlue',
                            'text-wrap': 'wrap',
                            'text-max-width': '80px', # Increased slightly for better readability
                            'font-size': '12px',

                            # CHANGE THIS:
                            # Setting this to a very small number (or 0) allows the text
                            # to disappear as you zoom out, which feels much smoother.
                            'min-zoomed-font-size': '4px',

                            # OPTIONAL: Add this to keep labels from overlapping during zoom
                            'text-events': 'no',
                        }
                    },
                    {
                        'selector': '[type = "contestant"]',
                        'style': {
                            'background-color': '#C9A9A6',  # dusty rose
                            'width': '40px',  # Make them bigger too!
                            'height': '40px'
                        }
                    },
                    {
                        'selector': ':selected',
                        'style': {
                            'background-color': '#FF4136',  # Turn Red
                            'line-color': '#FF4136',
                            'target-arrow-color': '#FF4136',
                            'source-arrow-color': '#FF4136',
                            'border-width': '4px',
                            'border-color': '#FFDC00',  # Golden border
                            'width': '45px',  # Make it slightly bigger
                            'height': '45px',
                            'z-index': 9999  # Bring to front
                        }
                    },
                    {
                        'selector': 'edge',
                        'style': {
                            'width': 1,
                            'line-color': '#888',
                            'curve-style': 'bezier' # Allows for curved edges and arrows
                        }
                    },
                    {
                        'selector': 'edge:selected',
                        'style': {
                            'width': 6,
                            'line-color': '#FF4136',  # Bright Red
                            'target-arrow-color': '#FF4136',
                            'label': 'Relationship Info',  # Optional: Show text on the line itself
                            'font-size': '10px',
                            'color': '#FF4136',
                            'z-index': 9999
                        }
                    }
                ]
            ),
            html.Div([
                html.Label("Filter by Show:"),
                dcc.Dropdown(
                    id='dept-dropdown',
                    options=[
                        {'label': 'Season', 'value': 'all'},
                        {'label': 'Engineering', 'value': 'Engineering'},
                        {'label': 'Design', 'value': 'Design'},
                        {'label': 'Executive', 'value': 'Executive'}
                    ],
                    value='all',
                    clearable=False,
                    style={'width': '300px'}
                ),
            ], style={'marginBottom': '20px'}),
            html.Div(id='node-data-display', style={'marginTop': '20px', 'fontSize': '1.2em', 'color': '#555'})
        ])
        return app



if __name__ == '__main__':
    # traitors_us_s4_2026-02-25
    # df = pd.read_csv('traitors_us_s4_2026-02-25.csv')
    # nd = df['name'].tolist()
    # ed = []
    # for x in nd:
    #     tup = (x, "Traitors_US_S4")
    #     ed.append(tup)
    #
    # ng_traitors_us4 = NetworkGraph(nd, ed)

    # bachelor
    bach_nd = []
    bach_ed = []
    bach_df = pd.read_csv('./data/reality_contestants.csv')


    contestant_list = bach_df['name'].tolist()
    show_list = bach_df['show'].tolist()

    for x in contestant_list:
        dic = {'data': {'id': x, 'label': x, 'type': 'contestant'}}
        bach_nd.append(dic)
    for x in list(set(show_list)):
        dic = {'data': {'id': x, 'label': x, 'type': 'show'}}
        bach_nd.append(dic)

    for index, row in bach_df.iterrows():
        tup = (row['name'], row['show'])
        bach_ed.append(tup)
    bach_ng = NetworkGraph(bach_nd, bach_ed)

    app = bach_ng.render_app()

    app.run()