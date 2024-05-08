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
		if pos in excel:
			currPos = pd.read_excel(f"./positionData/{excel}")
			readPositions.append(currPos)
	
	combinedData = pd.concat(readPositions)
	
	# for i in range(2):
		# print(combinedDataLst[i]["Unnamed: 1"][i])
  
	with open("./teams.json", 'r') as teamJSON:
			teamKeys = json.load(teamJSON)

	allPlayers = {}

	combinedDataLst = combinedData.values.tolist()
	combinedDataLst = combinedDataLst[1:]
	for i in range(1, len(combinedDataLst) // 200):
		print(combinedDataLst[i*200])
		combinedDataLst.pop(i*200)
		print(combinedDataLst[i*200])

	for i in range(len(combinedDataLst)):
		playerDict = {}
		print(i)
		print(combinedDataLst[i])
		teamName = combinedDataLst[i][9]
		oppName = combinedDataLst[i][11]
		fullScore = combinedDataLst[i][11]
		hyphen = fullScore.find("-")
		playerDict.update({
			"week": combinedDataLst[i][6],
			"team": teamKeys[teamName],
			"opp": teamKeys[oppName],
			"teamScore": fullScore[2:hyphen],
			"oppScore": fullScore[hyphen:],
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
		allPlayers.update({combinedDataLst[i][1]: playerDict})
	with open("./playerDict.json", "w") as f:
		json.dump(allPlayers, f)



main()