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
		html.Div(id='available_games_widgets', className='columns is-3 p-5 is-multiline')
		],id='body', className='has-background-dark-60'),

	html.Footer(['Footer'], className='has-background-link-80')

], className='has-text-light')

############## *** CALLBACKS *** ##############
#_____________________________________________#

@app.callback(
	Output('available_games_widgets','children'),
	Input('url','pathname')
	)

def available_games(pathname):
	children = []

	if pathname == '/':

		for categories in list_of_games:
			sport_name = categories['sport_name']
			games = categories['data']
			print(sport_name)

			if games == None:
				continue

			for games in categories['data']:
				team_one_name = games['team_one_name']
				team_two_name = games['team_two_name']
				score = games['score']

				widget = html.Div([
					html.Div([
						html.P(sport_name, className='button is-small' )
						], className='columns is-centered', style={'border-radius':'0 0 8px 8px'}),
					html.Div([
						html.Div([html.P(team_two_name, style={'text-align':'center'})], className='column'),
						html.Div([html.P(score, style={'text-align':'center'})], className='column'),
						html.Div([html.P(team_two_name, style={'text-align':'center'})], className='column')
						], className='columns')
					], className='column box is-3 has-text-center')

				children.append(widget)

	return children


available_games('/')

if __name__ == "__main__":
    app.run_server(debug=True)