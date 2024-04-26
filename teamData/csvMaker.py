def main():
	# r = True
	# while r == True:
	# 	filename = input("File name: ") + ".csv"
	# 	content = input("Content: ")
	# 	with open(filename) as myFile:
	# 		myFile.write(content)
	# 	if input("Continue? (y/n): ") == "n":
	# 		r = False
	teams = ["cardinals", "falcons", "ravens", "bills", "panthers", "bears", "bengals", "browns", "cowboys", "broncos", "lions", "packers", "texans", "colts", "jaguars", "chiefs", "raiders", "chargers", "rams", "dolphins", "vikings", "patriots", "saints" "giants", "jets", "eagles", "steelers", "49ers", "seahawks", "buccaneers", "titans", "commanders"]
	sections = ["passing", "rushingAndReceiving", "kickAndPunt", "kicking", "punting", "defense", "scoring"]

	for team in teams:
		for section in sections:
			filename = team + "_" + section + ".csv"
			f = open(filename, "w")
			f.close()



main()