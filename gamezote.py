# gamezote
import os
from dotenv import load_dotenv
from dash import Dash, html, dcc
from dash.dependencies import Output, Input
import requests
import json
import requests_cache
from flask import Flask, jsonify, send_from_directory

load_dotenv()
football_api_key = os.getenv('FOOTBALL_API_KEY')

server = Flask(__name__)
app = Dash(__name__,server=server)

############## *** ALL API KEYS *** ##############
# _______________________________________________#

vid_url = "https://all-sport-live-stream.p.rapidapi.com/api/v2/all-live-stream"
fb_url = "https://v3.football.api-sports.io/"

vid_api_headers = {
	"x-rapidapi-key": os.getenv('VIDEO_API_KEY'),
	"x-rapidapi-host": "all-sport-live-stream.p.rapidapi.com"
}

fb_headers = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": os.getenv('FOOTBALL_API_KEY')
}

def list_of_games():
	gamelist = requests.get(vid_url,headers=vid_api_headers).json()
	return gamelist

list_of_games = list_of_games()

def search_team_logo(team_to_search):
	query = dict(search=team_to_search)
	team_info = requests.get(fb_url+"/teams", headers=fb_headers, params=query).json()
	if team_info['response'] != []:
		team_logo = team_info['response'][0]['team']['logo']
	else:
		team_logo = []
	return team_logo

############## *** HTML JAVASCRIPT *** ##############
# __________________________________________________#

@server.route('/widget')
def serve_widget():
	widget_html =f''' 
		<div id="wg-api-football-games"
			data-host="v3.football.api-sports.io"
			data-key="football_api_key"
			data-date=""
			data-league=""
			data-season=""
			data-theme=""
			data-refresh="60"
			data-show-toolbar="true"
			data-show-errors="false"
			data-show-logos="true"
			data-modal-game="false"
			data-modal-standings="false"
			data-modal-show-logos="true">
		</div>
		<script
		    type="module"
		    src="https://widgets.api-sports.io/2.0.3/widgets.js">
		</script>'''
	return widget_html

############## *** APP LAYOUT *** ##############
# _____________________________________________#


app.layout = html.Div([
	dcc.Location(id='url',refresh=False),

	html.Div([
		html.H1('GameZote'),
		# html.A([
		# 	html.I(className='fas fa-twitter')
		# 	], className='button is-link'),
		],className='column p-5',style={'backgroungColor':'#7a4d99','color':'white'}),

	html.Div([
		dcc.Link('Live', className='button m-1 is-small',href='/live'),
		dcc.Link('All Games', className='button m-1 is-small',href='/live'),
		dcc.Link('Football', className='button m-1 is-small', href='/football'),
		html.A(['NBA'], className='button m-1 is-small'),
		html.A(['Cricket'], className='button m-1 is-small'),
		html.A(['Ice Hockey'], className='button m-1 is-small'),
		],className='has-background-success-65'),

	html.Div([
		html.Div([
			html.Div([],className='grid p-2', id='cellbox'),
			], className='columns p-5'),
		],id='body', className='has-background-dark-60'),

	html.Footer(['Footer'], className='has-background-link-80')

], className='has-text-light')

############## *** CALLBACKS *** ##############
#_____________________________________________#

@app.callback(
	Output('cellbox','children'),
	Input('url','pathname')
	)
def available_games(pathname):
	children = []
	if pathname == '/':

		for categories in list_of_games:
			sport_name = categories["sport_name"]
			category_games = categories['data']
			if not category_games:
				continue

			for game in category_games:
				team_one = game['team_one_name']
				team_two = game['team_two_name']
				match_info = game['score']
				team_one_logo = search_team_logo(team_one)
				team_two_logo = search_team_logo(team_two)
				
				game_widget = html.Div([

					html.P([sport_name], className='button is-small',style={'border-radius':'0 0 8px 8px',}),

					html.Div([
						html.Div([
							html.Img(src=f"{team_one_logo}", className='image is-96x96')
							],className='column'),
						html.Div([html.P([match_info])],className='column has-text-center'),
						html.Div([
							html.Img(src=f"{team_two_logo}", className='image is-96x96')
							], className='column'),
						],className='columns')
					],className='column is-one-third')
				children.append(game_widget)
	return children


# @app.callback(
# 	Output('cellbox','children'),
# 	Input('url','pathname')
# )
# def update_output(pathname):
# 	children=[]
# 	if pathname == "/":
# 		for _ in range(10):
# 			# children.append(html.Div(['Body box13'], className='cell box')),
# 			children.append(html.Div([
# 				html.Iframe(src='/widget'),
# 				], className='cell box')),
# 	return children

if __name__ == "__main__":
    app.run_server(debug=True)