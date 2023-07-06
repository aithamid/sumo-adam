import dash
import dash_leaflet as dl
import dash_html_components as html
import json
import requests

from dash.dependencies import Output, Input, State

app = dash.Dash()
app.layout = html.Div([
    dl.Map(dl.TileLayer(), style={'width': '1000px', 'height': '500px'}, id="map"),
    html.Div(id="output1"), html.Div(id="output2"), html.Div(id="output3"),
    html.Button("Download Map", id="download-button")
])


@app.callback(Output("output1", "children"), [Input("map", "zoom")])
def update_output1(viewport):
    return json.dumps(viewport)


@app.callback(Output("output2", "children"), [Input("map", "center")])
def update_output2(viewport):
    return json.dumps(viewport)


@app.callback(Output("output3", "children"), [Input("map", "viewport")])
def update_output3(viewport):
    center_lat, center_lon = viewport['center']
    zoom = viewport['zoom']

    # Calculate the width and height of the viewport in degrees
    viewport_width = 360 / (2 ** zoom)
    viewport_height = 180 / (2 ** zoom)

    # Calculate the north, south, east, and west coordinates
    north = center_lat + (viewport_height / 2)
    south = center_lat - (viewport_height / 2)
    east = center_lon + (viewport_width / 2)
    west = center_lon - (viewport_width / 2)

    print("North:", north)
    print("South:", south)
    print("East:", east)
    print("West:", west)
    return json.dumps(viewport)


@app.callback(Output("download-button", "n_clicks"), [Input("download-button", "n_clicks")], [State("map", "viewport")])
def download_map(n_clicks, viewport):
    if n_clicks:
        response = requests.get("https://www.openstreetmap.org/#map={}/{}/{}".format(
            viewport["zoom"], viewport["center"][0], viewport["center"][1]
        ))
        with open("map.html", "w") as f:
            f.write(response.text)
    return n_clicks


if __name__ == '__main__':
    app.run_server(debug=True)
