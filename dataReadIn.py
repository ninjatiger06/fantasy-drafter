import numpy as np
import pandas as pd
import os, os.path

def main():
	year = input("Year: ")
	pos = input("Position: ")
	fantasyData = pd.read_excel(f"./fantasyData/{year}.xlsx")

	positions = os.listdir("./positionData")
	readPositions = []
	for excel in positions:
		if pos in excel:
			readPositions.append(excel)
			currPos = pd.read_excel(f"./positionData/{excel}")
	print(readPositions)



main()