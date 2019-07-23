import colorama
import os
import copy
import random

board = []



def setupBoard():
	x = 0
	while(x < 7):
		board.append([])
		y = 0
		while (y < 6):
			board[x].append("E")
			y+=1
		x+=1

def clear():
	if (os.name == 'nt'):
		os.system('cls')
	else:
		os.system('clear')
		
def displayBoard(message=""):
	clear()
	print("---"*7)
	x = 5
	while(x >= 0):
		y = 0
		str = ""
		while(y < 7):
			if (board[y][x] == "R"):
				str+="|"+colorama.Back.RED+" "+colorama.Style.RESET_ALL+"|"
			elif (board[y][x] == "B"):
				str+="|"+colorama.Back.BLUE+" "+colorama.Style.RESET_ALL+"|"
			else:
				str+="|"+colorama.Back.WHITE+" "+colorama.Style.RESET_ALL+"|"
			y+=1
		print(str)
		x-=1
		print("---"*7)
	print(" 1  2  3  4  5  6  7")
	if (message != ""):
		print()
		print()
		print(colorama.Fore.RED+message+colorama.Style.RESET_ALL)

def gameEnd(result="tie"):
	clear()
	print("---"*7)
	x = 5
	while(x >= 0):
		y = 0
		str = ""
		while(y < 7):
			if (board[y][x] == "R"):
				str+="|"+colorama.Back.RED+" "+colorama.Style.RESET_ALL+"|"
			elif (board[y][x] == "B"):
				str+="|"+colorama.Back.BLUE+" "+colorama.Style.RESET_ALL+"|"
			else:
				str+="|"+colorama.Back.WHITE+" "+colorama.Style.RESET_ALL+"|"
			y+=1
		print(str)
		x-=1
		print("---"*7)
	print(" 1  2  3  4  5  6  7")
	print()
	print()
	if (result == "tie"):
		print(colorama.Fore.YELLOW+"Tie game!"+colorama.Style.RESET_ALL)
	elif (result == "win"):
		print(colorama.Fore.GREEN+"You won!"+colorama.Style.RESET_ALL)
	else:
		print(colorama.Fore.RED+"You lost!"+colorama.Style.RESET_ALL)
	input()
	exit()

def makeMove(color, column):
	acol = column-1
	checkColumn = board[acol]
	x = 0
	row = 0
	valid = False
	while(x < 6):
		if (checkColumn[x] == "E"):
			checkColumn[x] = color
			row = x+1
			valid = True
			break
		x+=1
	if (valid):
		checkWin(column, row, color)
		return True
	else:
		return False
						
def playerMakeMove(error=0):
	if (error == 0):
		displayBoard()
	col = input("Select a column to place a chip:")
	try:
		col = int(col)
	except ValueError:
		displayBoard("Please type a number 1-7")
		return playerMakeMove(1)
	if (col <= 0 or col >= 8):
		displayBoard("Please type a number 1-7")
		return playerMakeMove(1)
	row = makeMove("B", col)
	if (not row):
		displayBoard("This column is full, please choose another")
		return playerMakeMove(1)

def AIMakeMove():
	col = AICheckWinNow()
	if (col == -1):
		col = AICheckPlayerWinNext()
	if (col == -1):
		col = AINextBestMove()
	makeMove("R", col+1)
	
def AINextBestMove():
	bestCol = random.randint(0,6)
	bestColCT = 1
	x = 0
	found = False
	while (x < 7):
		checkBoard = copy.deepcopy(board)
		checkColumn = checkBoard[x]
		y = 0
		test = False
		while(y < 6):
			if (checkColumn[y] == "E"):
				checkColumn[y] = "R"
				test = True
				found = True
				break
			y+=1
		if (test):
			curCT = AIGetBestCountAtColRow(checkBoard, x, y)
			if (curCT > bestColCT):
				bestCol = x
				bestColCT = curCT
		x+=1
	if (found):
		return bestCol
	else:
		return AINextBestMove()
	
def AIGetBestCountAtColRow(boar, col, row):
	bestCount = 0
	#check same row
	count = 1
	x = col-1
	while(x >= 0):
		if (boar[x][row] == "R"):
			count+=1
		else:
			break
		x-=1
	x = col+1
	while(x < 7):
		if (boar[x][row] == "R"):
			count+=1
		else:
			break
		x+=1
	if (count >= bestCount):
		bestCount = count
	
	#check same column
	count = 1
	x = row-1
	while(x >= 0):
		if (boar[col][x] == "R"):
			count+=1
		else:
			break
		x-=1
	x = row+1
	while(x < 6):
		if (boar[col][x] == "R"):
			count+=1
		else:
			break
		x+=1
	if (count >= bestCount):
		bestCount = count
		
	#checkBackSlashDiag
	count = 1
	x = col + 1
	y = row - 1
	while (x < 7 and y >= 0):
		if (boar[x][y] == "R"):
			count+=1
		else:
			break
		x+=1
		y-=1
	x = col - 1
	y = row + 1
	while (x >= 0 and y < 6):
		if (boar[x][y] == "R"):
			count+=1
		else:
			break
		x-=1
		y+=1
	if (count >= bestCount):
		bestCount = count
	#checkSlashDiag
	count = 1
	x = col + 1
	y = row + 1
	while (x < 7 and y < 6):
		if (boar[x][y] == "R"):
			count+=1
		else:
			break
		x+=1
		y+=1
	x = col - 1
	y = row - 1
	while (x >= 0 and y >= 0):
		if (boar[x][y] == "R"):
			count+=1
		else:
			break
		x-=1
		y-=1
	if (count >= bestCount):
		bestCount = count
	return bestCount
		
def AICheckWinNow():
	x = 0
	while (x < 7):
		checkBoard = copy.deepcopy(board)
		checkColumn = checkBoard[x]
		y = 0
		test = False
		while(y < 6):
			if (checkColumn[y] == "E"):
				checkColumn[y] = "R"
				test = True
				break
			y+=1
		if (test):
			if (AICheckWin(checkBoard, x, y, "R")):
				return x
		x+=1
	return -1
	
def AICheckPlayerWinNext():
	x = 0
	while (x < 7):
		checkBoard = copy.deepcopy(board)
		checkColumn = checkBoard[x]
		y = 0
		test = False
		while(y < 6):
			if (checkColumn[y] == "E"):
				checkColumn[y] = "B"
				test = True
				break
			y+=1
		if (test):
			if (AICheckWin(checkBoard, x, y, "B")):
				return x
		x+=1
	return -1
			
def AICheckWin(boar, col, row, color):
	#check same row
	count = 1
	x = col-1
	while(x >= 0):
		if (boar[x][row] == color):
			count+=1
		else:
			break
		x-=1
	x = col+1
	while(x < 7):
		if (boar[x][row] == color):
			count+=1
		else:
			break
		x+=1
	if (count >= 4):
		return True
	
	#check same column
	count = 1
	x = row-1
	while(x >= 0):
		if (boar[col][x] == color):
			count+=1
		else:
			break
		x-=1
	x = row+1
	while(x < 6):
		if (boar[col][x] == color):
			count+=1
		else:
			break
		x+=1
	if (count >= 4):
		return True
		
	#checkBackSlashDiag
	count = 1
	x = col + 1
	y = row - 1
	while (x < 7 and y >= 0):
		if (boar[x][y] == color):
			count+=1
		else:
			break
		x+=1
		y-=1
	x = col - 1
	y = row + 1
	while (y < 6 and x >= 0):
		if (boar[x][y] == color):
			count+=1
		else:
			break
		x-=1
		y+=1
	if (count >= 4):
		return True
	#checkSlashDiag
	count = 1
	x = col + 1
	y = row + 1
	while (x < 7 and y < 6):
		if (boar[x][y] == color):
			count+=1
		else:
			break
		x+=1
		y+=1
	x = col - 1
	y = row - 1
	while (x >= 0 and y >= 0):
		if (boar[x][y] == color):
			count+=1
		else:
			break
		x-=1
		y-=1
	if (count >= 4):
		return True
	return False
	
def checkWin(col, row, color):
	#check board full
	col = col - 1
	row = row - 1
	x = 0
	emptySpace = False
	while (x < 7):
		y = 0
		while (y < 6):
			if (board[y][x] == "E"):
				emptySpace = True
				break
			y+=1
		if (emptySpace):
			break
		x+=1
	if (not emptySpace):
		gameEnd()
	else:
		#check same row
		count = 1
		x = col-1
		while(x >= 0):
			if (board[x][row] == color):
				count+=1
			else:
				break
			x-=1
		x = col+1
		while(x < 7):
			if (board[x][row] == color):
				count+=1
			else:
				break
			x+=1
		if (count >= 4 and color == "B"):
			gameEnd("win")
		elif(count >= 4 and color == "R"):
			gameEnd("loss")
		
		#check same column
		count = 1
		x = row-1
		while(x >= 0):
			if (board[col][x] == color):
				count+=1
			else:
				break
			x-=1
		x = row+1
		while(x < 6):
			if (board[col][x] == color):
				count+=1
			else:
				break
			x+=1
		if (count >= 4 and color == "B"):
			gameEnd("win")
		elif(count >= 4 and color == "R"):
			gameEnd("loss")
			
		#checkBackSlashDiag
		count = 1
		x = col + 1
		y = row - 1
		while (x < 7 and y >= 0):
			if (board[x][y] == color):
				count+=1
			else:
				break
			x+=1
			y-=1
		x = col - 1
		y = row + 1
		while (y < 6 and x >= 0):
			if (board[x][y] == color):
				count+=1
			else:
				break
			x-=1
			y+=1
		if (count >= 4 and color == "B"):
			gameEnd("win")
		elif(count >= 4 and color == "R"):
			gameEnd("loss")
		#checkSlashDiag
		count = 1
		x = col + 1
		y = row + 1
		while (x < 7 and y < 6):
			if (board[x][y] == color):
				count+=1
			else:
				break
			x+=1
			y+=1
		x = col - 1
		y = row - 1
		while (x >= 0 and y >= 0):
			if (board[x][y] == color):
				count+=1
			else:
				break
			x-=1
			y-=1
		if (count >= 4 and color == "B"):
			gameEnd("win")
		elif(count >= 4 and color == "R"):
			gameEnd("loss")


colorama.init()
setupBoard()
displayBoard()

while(True):
	playerMakeMove()
	AIMakeMove()