import numpy as np
import pandas as pd
import json
import os, os.path

def main():
	year = input("Year: ")
	pos = input("Position: ")
	fantasyData = pd.read_excel(f"./fantasyData/{year}.xlsx")

	positions = os.listdir("./positionData")
	readPositions = []
	for excel in positions:
		if pos in excel and year in excel:
			currPos = pd.read_excel(f"./positionData/{excel}")
			readPositions.append(currPos)
	
	combinedData = pd.concat(readPositions)
	
	# for i in range(2):
		# print(combinedDataLst[i]["Unnamed: 1"][i])
  
	with open("./teams.json", 'r') as teamJSON:
			teamKeys = json.load(teamJSON)

	combinedDataLst = combinedData.values.tolist()
	combinedDataLst = combinedDataLst[1:]
	for i in range(1, len(combinedDataLst)-1):
		try:
			if combinedDataLst[i][0] == 'Rk':
				print(f"\n + {i}")
				print(combinedDataLst[i-1])
				print(combinedDataLst[i])
				print(combinedDataLst[i+1])
				combinedDataLst.pop(i)
		except IndexError:
			pass
	
	try:
		f = open("playerDict.json", "r")
		try:
			allPlayers = json.load(f)
		except json.decoder.JSONDecodeError:
			allPlayers = {}
	except FileNotFoundError:
		allPlayers = {}
		f = open("playerDict.json", "w")

	for i in range(len(combinedDataLst)):
		playerName = combinedDataLst[i][1]
		playerDict = {}
		teamName = combinedDataLst[i][9]
		oppName = combinedDataLst[i][11]
		fullScore = combinedDataLst[i][12]
		hyphen = fullScore.find("-")
		# week = ((int(year)-2020) * 17) + combinedDataLst[i][6]
		playerDict.update({
			# "week": None,
			"season": year,
			"week": combinedDataLst[i][6],
			"team": teamKeys[teamName],
			"opp": teamKeys[oppName],
			"teamScore": fullScore[2:hyphen],
			"oppScore": fullScore[hyphen+1:],
			"cmpPass": combinedDataLst[i][13],
			"att": combinedDataLst[i][14],
			"inc": combinedDataLst[i][15],
			"cmpPerc": combinedDataLst[i][16],
			"yds": combinedDataLst[i][17],
			"td": combinedDataLst[i][18],
			"intThrown": combinedDataLst[i][19],
			"pick6": combinedDataLst[i][20],
			"tdPerc": combinedDataLst[i][21],
			"intPerc": combinedDataLst[i][22],
			"rate": combinedDataLst[i][23],
			"sk": combinedDataLst[i][24],
			"skYds": combinedDataLst[i][25],
			"skPerc": combinedDataLst[i][26],
			"yA": combinedDataLst[i][27],
			"ayA": combinedDataLst[i][28],
			"anyA": combinedDataLst[i][29],
			"yC": combinedDataLst[i][30],
			"succPerc": combinedDataLst[i][31]
		})
		try:
			newPlayerDict = allPlayers[playerName]
			# print(newPlayerDict)
			# lastWk = newPlayerDict[len(newPlayerDict)-1]["week"]
			# print(lastWk, combinedDataLst[i][6], lastWk + combinedDataLst[i][6])
			# playerDict.update({"week": lastWk + 1})
			newPlayerDict.append(playerDict)
			allPlayers.update({playerName: newPlayerDict})
		except KeyError:
			# playerDict.update({"week": combinedDataLst[i][6]})
			allPlayers.update({playerName: [playerDict]})
			
	f.close()
	f = open("playerDict.json", "w")
	json.dump(allPlayers, f, indent=2)
	f.close()



main()