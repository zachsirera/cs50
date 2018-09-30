# This is a program to rank FBS football teams
# Zach Sirera
# 9/14/2018 to 9/20/2018

# This program is designed to rank football teams based on score outcomes only. 
# No other metrics are taken into account. 
# This poll does not take into account pre-season rankings.
# This poll is recursive as it will re-evalute the value of wins throughout the season. 
# Teams are awarded points for wins over better teams, however, if these teams' relative rankings reverse, 
# 	the poll will be adjusted to reflect that, and the winning team will no longer benefit from a win over a 
# 	team now determined to be worse. 
# Teams are ranked in order of number of points ammassed throughout the season. 
# Rankings will be recompiled after every week of football and finalized at the end of the regular season. 


from lxml import html
import arrow
import requests
import sys
import numpy as np
import pandas as pd 
import helpers
import settings
from flask import Flask, render_template
import matplotlib.pyplot as plt


app = Flask(__name__) 


@app.route("/", methods=["GET", "POST"])
def rankings():

	# Get score data for all games of P5 schools using html from lxml 
	page  = requests.get('https://www.masseyratings.com/scores.php?s=300937&sub=11604&all=1')
	scores = html.fromstring(page.content)
	games = scores.xpath('//pre/text()')
	games_list = "--".join(games)

	# Put data in a readable list 
	games_rows = games_list.split('\n')

	# Delete last 4 lines from games_rows which do not represent any game data
	# This is the list that this program will iterate over to award points
	games_rows = games_rows[:-4]

	# Get today's date 
	today = arrow.now().format('YYYY-MM-DD')

	# Create an empty list to store team's data
	team_data = []
	team_columns = ['Team', 'Conference', 'Tier', 'Wins', 'Losses', 'Points', 'Rank']

	for teams in settings.fbs_teams:
		
		# All teams start 0-0 with 0 points, 0 SOR, 0 Total, and tied for rank 1
		teamdata = [teams, helpers.conf(teams), helpers.tier(helpers.conf(teams)), 0, 0, 0, 1]
		team_data.append(teamdata)

	global team_df
	team_df = pd.DataFrame(team_data, columns=team_columns)

	# Create an empty list to store game data
	game_data = []


	for index, rows in enumerate(games_rows):
		# Extract game data from rows
		date = rows[0:10]
		location = rows[10:12]
		team1 = rows[12:37].rstrip()
		score1 = int(rows[37:39])
		team2 = rows[41:66].rstrip()
		score2 = int(rows[66:68])
		team1conf = helpers.conf(team1)
		team2conf = helpers.conf(team2)
		team1tier = helpers.tier(team1conf)
		team2tier = helpers.tier(team2conf)


		# Get team data
		if team1tier == "Lower":
			# team1points = 0
			team1wins = 0
		else:
			# team1points = team_df.iloc[settings.fbs_teams.index(team1)]['Points']
			team1wins = team_df.iloc[settings.fbs_teams.index(team1)]['Wins']
		if team2tier == "Lower":
			# team2points = 0
			team2losses = 0
		else:
			# team2points = team_df.iloc[settings.fbs_teams.index(team2)]['Points']
			team2losses = team_df.iloc[settings.fbs_teams.index(team2)]['Losses']

		team1points = 0
		team2points = 0

		######################################
		# Point stucture is as follows:

		# Points for winning the game: 

		# Win game 						10 pts


		# Points for how a team played:
		# These can be won by either team, provided neither team is in the 'Lower' tier

		# Score 40 or more				1  pts
		# Score 50 or more 				1  pts
		# Hold them to 20 or less 		1  pts
		# Hold them to 10 or less 		1  pts
		# Shut them out 				3  pts
		# Win by 20 					1  pts
		# Win by 30 					1  pts
		# Win by 40 					1  pts

		# The only criteria that results in a loss of points: 

		# Lose to lower 'level' team   -5  pts

		# College football games cannot end in a tie.

		######################################

		

		# Points for each game are the summation of all point-awarding criteria. 
		# Teams can also earn points in a loss.

		########## Assign points ##########

		# Initialize "points"
		# By default, team1 is always the winner of the game.
		team1points += 10
		team1wins += 1
		team2losses += 1 

		# As stated above, these style points can only be earned in wins over G5 or P5 teams:
		if not helpers.tier(team2conf) == 'Lower':
			if helpers.winby20(score1, score2):
				team1points += 1

			if helpers.winby30(score1, score2):
				team1points += 1

			if helpers.winby40(score1, score2):
				team1points += 1

			if helpers.score40(score1):
				team1points += 1

			if helpers.score40(score2):
				team2points += 1

			if helpers.score50(score1):
				team1points += 1

			if helpers.score50(score2):
				team2points += 1

			if helpers.hold20(score1):
				team2points += 1

			if helpers.hold10(score1):
				team2points += 1

			if helpers.hold20(score2):
				team1points += 1

			if helpers.hold10(score2):
				team1points += 1

		# These points can be won by teams at any tier
		if helpers.shutout(score2):
			team1points += 3

		if helpers.roadwin(location):
			team1points += 2

		game_columns = ['Date', 'Winning Team', '1 Score', '1 Points', '1 SOR', '1 Total', 'Losing Team', '2 Score', '2 Points', '2 SOR', '2 Total']
		gamedata = [date, team1, score1, team1points, 0, 0, team2, score2, team2points, 0, 0]
		game_data.append(gamedata)	

		# Update DataFrame with game data
		if team1tier != 'Lower':
			team1index = settings.fbs_teams.index(team1)
			team_df.loc[team1index, 'Wins'] = team1wins
			team_df.loc[team1index, 'Points'] = team1points

		if team2tier != 'Lower':
			team2index = settings.fbs_teams.index(team2)
			team_df.loc[team2index, 'Losses'] = team2losses
			team_df.loc[team2index, 'Points'] = team2points

	# Compile game_data into Data Frame
	global game_df
	game_df = pd.DataFrame(game_data, columns = game_columns)

	# Evaluate ranks of all teams in FBS based on the number of points they have at this time
	team_df['Rank'] = team_df['Points'].rank(ascending = False)

	# Determing SOR
	for index, rows in enumerate(games_rows):
		# Extract game data from rows
		# By default team1 is the winning team
		team1 = rows[12:37].rstrip()
		team2 = rows[41:66].rstrip()
		team1conf = helpers.conf(team1)
		team2conf = helpers.conf(team2)
		team1tier = helpers.tier(team1conf)
		team2tier = helpers.tier(team2conf)
		if team1tier == 'Lower':
			team1rank = 129
		else:
			team1rank = team_df.iloc[settings.fbs_teams.index(team1)]['Rank']
		if team2tier == 'Lower':
			team2rank = 129
		else:
			team2rank = team_df.iloc[settings.fbs_teams.index(team2)]['Rank']

		# Determine the Strength of Record for each performance
		if team2tier == 'G5':
			# A team gets 0.5 for beating a G5 school
			team1SOR = 1.5
			# A team will get additional points for beating a team that is in the top 25 and/or is higher ranked
			if helpers.beattop25(team2rank):
				team1SOR += 0.5
			if helpers.beathigherranked(team1rank, team2rank):
				team1SOR += 0.5
		elif team2tier == 'P5':
			# A team gets 1 for beating a P5 school
			team1SOR = 2
			if helpers.beattop25(team2rank):
				team1SOR += 0.5
			if helpers.beathigherranked(team1rank, team2rank):
				team1SOR += 0.5
		else:
			# If a team beats a Lower tier school the multiplier is limited to 1. 
			team1SOR = 1

		# Same thing goes for team2, however, by definition they are the losers, so the 'beat' functions are not executed. 
		if team1tier == 'G5':
			team2SOR = 1.5
		elif team1tier == 'P5':
			team2SOR = 2
		else: 
			team1SOR = 1

		# Append the game DataFrame with SOR data and calculate Total for this game 
		game_df.loc[index, '1 SOR'] = team1SOR
		game_df.loc[index, '2 SOR'] = team2SOR

		# Get points from previous iterations
		team1points = game_df.loc[index, '1 Points']
		team2points = game_df.loc[index, '2 Points']

		# Calculate totals 
		team1gametotal = team1SOR * team1points
		team2gametotal = team2SOR * team2points

		# Update game_df with totals
		game_df.loc[index, '1 Total'] = team1gametotal
		game_df.loc[index, '2 Total'] = team2gametotal

		# Update totals in team_df DataFrame
		if team1tier == 'Lower':
			team1total = 0
		else:
			team1index = settings.fbs_teams.index(team1)
			team1total = team_df.loc[team1index, 'Points']

		team1total += team1gametotal

		if team2tier == 'Lower':
			team2total = 0
		else: 
			team2index = settings.fbs_teams.index(team2)
			team2total = team_df.loc[team2index, 'Points']

		team2total += team2gametotal

		team_df.loc[team1index, 'Points'] = team1total
		team_df.loc[team2index, 'Points'] = team2total

		# Update rankings
		team_df['Rank'] = team_df['Points'].rank(ascending = False)

	# Get just top 25
	global top_25 
	top_25 = pd.DataFrame(team_df[team_df.Rank < 26]).sort_values(by = ['Rank'])

	global top_25list
	top_25list = top_25.values.tolist()

	# Render template in Flask
	return render_template("index.html", rankings = top_25, updated = today)

# This route will display a table of all 128 FBS teams and their records, ranks, and scores. 
@app.route('/teams', methods=['GET', 'POST'])
def all_teams():

	# Get today's date 
	today = arrow.now().format('YYYY-MM-DD')
	
	return render_template("teams.html", rankings = team_df, updated = today)

# This route will display all game data up until this point in the season that the code is executed. 
@app.route('/games', methods=['GET', 'POST'])
def all_games():

	# Get today's date 
	today = arrow.now().format('YYYY-MM-DD')

	return render_template("games.html", games = game_df, updated = today)

# This route will generate a bar graph to visually depict the score breakdown of the top 25
@app.route('/chart', methods=['GET', 'POST'])
def chart():

	#plot = top_25.plot.barh(x='Team', y='Points')
	#fig.savefig("plot.png")

	return render_template("chart.html")

# This route will display the poll methodology document
@app.route('/method', methods=['GET', 'POST'])
def method():

	return render_template("method.html")














