import colorama
import os
import random

playerBoard = []
AIBoard = []
lettercoords = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
AIDownedShips = 0
PlayerDownedShips = 0
oldPlayerDownedShips = 0
oldAIDownedShips = 0

class EmptyPiece:
	def __init__(self):
		self.Hit = False
		
	def hit(self):
		self.Hit = True
		
	def getIsHit(self):
		return self.Hit
		
	def consoleColorCode(self):
		if (self.Hit):
			return colorama.Back.WHITE
		else:
			return ""
			
	def getPieceType(self):
		return "empty"
		
	def getIsSunk(self):
		return False

class PlayerShipPiece(EmptyPiece):
	def __init__(self, parent):
		EmptyPiece.__init__(self)
		self.parent = parent
	
	def hit(self):
		EmptyPiece.hit(self)
		self.parent.notifyHit()

	def consoleColorCode(self):
		if (self.Hit):
			return colorama.Back.RED
		else:
			return colorama.Back.BLUE
			
	def getPieceType(self):
		return "ship"
		
	def getIsSunk(self):
		return self.parent.isSunk()
	
class AIShipPiece(EmptyPiece):
	def __init__(self, parent):
		EmptyPiece.__init__(self)
		self.parent = parent
	
	def hit(self):
		EmptyPiece.hit(self)
		self.parent.notifyHit()

	def consoleColorCode(self):
		if (self.Hit):
			return colorama.Back.RED
		else:
			return ""
			
	def getPieceType(self):
		return "ship"
		
	def getIsSunk(self):
		return self.parent.isSunk()
	
class PlayerShip:
	def __init__(self, size, orientation, startposx, startposy):
		self.pieces = []
		x = 0
		while(x < size):
			piece = PlayerShipPiece(self)
			if (orientation.lower() == "v"):
				playerBoard[startposx][startposy+x] = piece
			else:
				playerBoard[startposx+x][startposy] = piece
			self.pieces.append(piece)
			x+=1
		self.sunk = False
	
	def notifyHit(self):
		global AIDownedShips
		x = 0
		while(x < len(self.pieces)):
			if (not self.pieces[x].getIsHit()):
				return False
			x+=1
		self.sunk = True
		AIDownedShips+=1
		return True
		
	def isSunk(self):
		return self.sunk

class AIShip:
	def __init__(self, size, orientation, startposx, startposy):
		self.pieces = []
		x = 0
		self.sunk = False
		while(x < size):
			piece = AIShipPiece(self)
			if (orientation.lower() == "v"):
				AIBoard[startposx][startposy+x] = piece
			else:
				AIBoard[startposx+x][startposy] = piece
			self.pieces.append(piece)
			x+=1
	
	def notifyHit(self):
		global PlayerDownedShips
		x = 0
		while(x < len(self.pieces)):
			if (not self.pieces[x].getIsHit()):
				return False
			x+=1
		self.sunk = True
		PlayerDownedShips+=1
		return True
		
	def isSunk(self):
		return self.sunk
	
class AICoord:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y
	
	def getX(self):
		return self.x
		
	def getY(self):
		return self.y
		
	def getIsSunk(self):
		return playerBoard[self.x][self.y].getIsSunk()
		
def clear():
	if (os.name == 'nt'):
		os.system('cls')
	else:
		os.system('clear')
	
def buildBoards():
	x = 0
	while(x < 10):
		y = 0
		playerBoard.append([])
		AIBoard.append([])
		while (y < 10):
			AIBoard[x].append(EmptyPiece())
			playerBoard[x].append(EmptyPiece())
			y+=1
		x+=1
		
def validateCoordinate(input):
	if (len(input) < 2):
		return False
	if (not input.upper()[:1] in lettercoords):
		return False
	try:
		if (not(int(input[1:]) > 0 and int(input[1:]) < 11)):
			return False
	except:
		return False
	return input.upper()
	
def translateX(input):
	input = validateCoordinate(input)
	if (input):
		input = input[:1]
		if (input == "A"):
			return 0
		elif (input == "B"):
			return 1
		elif (input == "C"):
			return 2
		elif (input == "D"):
			return 3
		elif (input == "E"):
			return 4
		elif (input == "F"):
			return 5
		elif (input == "G"):
			return 6
		elif (input == "H"):
			return 7
		elif (input == "I"):
			return 8
		elif (input == "J"):
			return 9
	return -1

def translateY(input):
	input = validateCoordinate(input)
	if (input):
		return int(input[1:])-1
	return -1
	
def displayUserBoard():
	print("    A  B  C  D  E  F  G  H  I  J")
	print("   ------------------------------")
	x = 0
	while (x < 10):
		if (x == 9):
			line = str(x+1)+" "
		else:
			line = str(x+1)+"  "
		y = 0
		while (y < 10):
			if (playerBoard[y][x].getIsSunk()):
				line += "|"+playerBoard[y][x].consoleColorCode()+"X"+colorama.Style.RESET_ALL+"|"
			else:
				line += "|"+playerBoard[y][x].consoleColorCode()+" "+colorama.Style.RESET_ALL+"|"
			y+=1
		print(line)
		print("   ------------------------------")
		x+=1

def displayEnemyBoard():
	print("    A  B  C  D  E  F  G  H  I  J")
	print("   ------------------------------")
	x = 0
	while (x < 10):
		if (x == 9):
			line = str(x+1)+" "
		else:
			line = str(x+1)+"  "
		y = 0
		while (y < 10):
			if (AIBoard[y][x].getIsSunk()):
				line += "|"+AIBoard[y][x].consoleColorCode()+"X"+colorama.Style.RESET_ALL+"|"
			else:
				line += "|"+AIBoard[y][x].consoleColorCode()+" "+colorama.Style.RESET_ALL+"|"
			y+=1
		print(line)
		print("   ------------------------------")
		x+=1
		
def hitCoord(input, board):
	if (validateCoordinate(input)):
		x = translateX(input)
		y = translateY(input)
		board[x][y].hit()

def playerPlaceShip(length):
	orientation = input("How would you like your "+str(length)+"-long ship oriented?: ")
	while (not(orientation.upper() == "H" or orientation.upper() == "V")):
		orientation = input("Please choose (H)orizontal or (V)ertical: ")
	startpos = validateCoordinate(input("Where would you like to place your "+str(length)+"-long ship?: "))
	while (not startpos):
		startpos = validateCoordinate(input("Please choose a valid position (eg. F6, H10, D2): "))
	x = translateX(startpos)
	y = translateY(startpos)
	valid = True
	if (orientation.upper() == "H"):
		if (x+length > 10):
			print("Invalid placement")
			playerPlaceShip(length)
			valid = False
	elif (orientation.upper() == "V"):
		if (y+length > 10):
			print("Invalid placement")
			playerPlaceShip(length)
			valid = False
	if (valid):
		if (not checkOccupationConflict(x,y,orientation.upper(), length, playerBoard)):
			PlayerShip(length, orientation.upper(), x, y)
		else:
			print("Invalid placement")
			playerPlaceShip(length)
	
def checkOccupationConflict(startX, startY, orientation, length, board):
	x = 0
	while (x < length):
		if (orientation == "H"):
			if (board[startX+x][startY].getPieceType() == "ship"):
				return True
		elif (orientation == "V"):
			if (board[startX][startY+x].getPieceType() == "ship"):
				return True
		x+=1
	return False

def setupShips():
	clear()
	displayUserBoard()
	playerPlaceShip(5)
	clear()
	displayUserBoard()
	playerPlaceShip(4)
	displayUserBoard()
	clear()
	displayUserBoard()
	playerPlaceShip(3)
	clear()
	displayUserBoard()
	playerPlaceShip(3)
	clear()
	displayUserBoard()
	playerPlaceShip(2)
	AIPlaceShip(5)
	AIPlaceShip(4)
	AIPlaceShip(3)
	AIPlaceShip(3)
	AIPlaceShip(2)
	
def AIPlaceShip(length):
	orientation = ""
	if(random.choice([True, False])):
		orientation = "V"
	else:
		orientation = "H"		
	x = 0
	y = 0
	
	if (orientation == "H"):
		x = random.randint(0, 10-length)
		y = random.randint(0, 9)
	else:
		y = random.randint(0, 10-length)
		x = random.randint(0, 9)
		
	if (checkOccupationConflict(x, y, orientation, length, AIBoard)):
		AIPlaceShip(length)
	else:
		AIShip(length, orientation, x, y)

def playerDoTurn(message=""):
	global AIDownedShips
	global PlayerDownedShips
	global oldAIDownedShips
	global oldPlayerDownedShips
	clear()
	displayEnemyBoard()
	print()
	print()
	displayUserBoard()
	if (message != ""):
		print()
		print(message)
	if (oldPlayerDownedShips != PlayerDownedShips):
		print(colorama.Fore.GREEN+"You sunk an enemy's battleship!"+colorama.Style.RESET_ALL)
		oldPlayerDownedShips = PlayerDownedShips
	if (oldAIDownedShips != AIDownedShips):
		print(colorama.Fore.RED+"The enemy sunk one of your battleships!"+colorama.Style.RESET_ALL)
		oldAIDownedShips = AIDownedShips
		
	move = validateCoordinate(input("which coordinate would you like to shoot at?"))
	while(not move):
		move = validateCoordinate(input("Please enter a valid coordinate (eg. F10, G4, D2): "))
	if (AIBoard[translateX(move)][translateY(move)].getIsHit()):
		playerDoTurn("You have already fired here, please choose a different location")
	else:
		AIBoard[translateX(move)][translateY(move)].hit()
	
AIWorkingOnShip = False
AIWorkDirection = 0
AILastQuadrant = random.randint(1,4)
AIHitPiecesNotSunk = []
AIOriginalX = 0
AIOriginalY = 0
AIAxis = False
	
def AIDoTurn():
	global AILastQuadrant
	global AIWorkDirection
	global AIWorkingOnShip
	global AIHitPiecesNotSunk
	global AIOriginalX
	global AIOriginalY
	global AIAxis
	
	x = len(AIHitPiecesNotSunk)-1
	while (x>=0):
		if (AIHitPiecesNotSunk[x].getIsSunk()):
			AIHitPiecesNotSunk.pop(x)
		x-=1
	
	if (not AIWorkingOnShip):
		
		if (len(AIHitPiecesNotSunk) > 0):
			AIOriginalX = AIHitPiecesNotSunk[0].getX
			AIOriginalY = AIHitPiecesNotSunk[0].getY
			AIWorkDirection = random.randint(1,4)
			AIWorkingOnShip = True
			AIDoTurn()
		else:
			x = 0
			y = 0
			if (AILastQuadrant == 1):
				AILastQuadrant = 2
				x = random.randint(0, 4)
				y = random.randint(0, 4)
			elif(AILastQuadrant == 2):
				AILastQuadrant = 3
				x = random.randint(0, 4)
				y = random.randint(5, 9)
			elif(AILastQuadrant == 3):
				AILastQuadrant = 4
				x = random.randint(5, 9)
				y = random.randint(5, 9)
			else:
				AILastQuadrant = 1
				x = random.randint(5, 9)
				y = random.randint(0, 4)
			if(playerBoard[x][y].getIsHit()):
				AIDoTurn()
			else:
				playerBoard[x][y].hit()
				if (playerBoard[x][y].getPieceType() == "ship"):
					AIWorkDirection = random.randint(1,4)
					AIWorkingOnShip = True
					AIOriginalX = x
					AIOriginalY = y
					AIHitPiecesNotSunk.append(AICoord(x, y))
	else:
		chosen = False
		chosePos = None
		piece = None
		while (not chosen):
			x = 1
			while (True):
				if (AIWorkDirection == 1):
					if (AIOriginalX-x < 0):
						AIWorkDirection = ((AIWorkDirection) % 4)+1
						break
					piece = playerBoard[AIOriginalX-x][AIOriginalY]
					chosePos = AICoord(AIOriginalX-x, AIOriginalY)
				elif (AIWorkDirection == 2):
					if (AIOriginalX+x > 9):
						AIWorkDirection = ((AIWorkDirection) % 4)+1
						break
					piece = playerBoard[AIOriginalX+x][AIOriginalY]
					chosePos = AICoord(AIOriginalX+x, AIOriginalY)
				elif (AIWorkDirection == 3):
					if (AIOriginalY-x < 0):
						AIWorkDirection = ((AIWorkDirection) % 4)+1
						break
					piece = playerBoard[AIOriginalX][AIOriginalY-x]
					chosePos = AICoord(AIOriginalX, AIOriginalY-x)
				else:
					if (AIOriginalY+x > 9):
						AIWorkDirection = ((AIWorkDirection) % 4)+1
						break
					piece = playerBoard[AIOriginalX][AIOriginalY+x]
					chosePos = AICoord(AIOriginalX, AIOriginalY+x)
				x+=1
				
				if (piece.getIsHit() and piece.getPieceType() == "ship"):
					continue
				elif (not piece.getIsHit()):
					chosen = True
					break
				else:
					AIWorkDirection = ((AIWorkDirection) % 4)+1
					break
			if (chosen):
				piece.hit()
				if (piece.getIsSunk()):
					AIWorkingOnShip = False
					AIAxis = False
				elif (piece.getPieceType() == "empty"):
					if (AIAxis):
						if (AIWorkDirection == 1):
							AIWorkDirection = 2
						elif (AIWorkDirection == 2):
							AIWorkDirection = 1
						elif (AIWorkDirection == 3):
							AIWorkDirection = 4
						elif (AIWorkDirection == 4):
							AIWorkDirection = 3
						AIAxis = False
					else:
						AIWorkDirection = ((AIWorkDirection) % 4)+1
				else:
					AIHitPiecesNotSunk.append(chosePos)
					AIAxis = True
	
def checkWin():
	global AIDownedShips
	global PlayerDownedShips
	
	if (AIDownedShips == 5):
		clear()
		displayEnemyBoard()
		print()
		print()
		displayUserBoard()
		print()
		print(colorama.Fore.RED + "You lose!")
		input()
		exit()
	elif(PlayerDownedShips == 5):
		clear()
		displayEnemyBoard()
		print()
		print()
		displayUserBoard()
		print()
		print(colorama.Fore.GREEN + "You win!")
		input()
		exit()
	
	
	
	
colorama.init()
buildBoards()
setupShips()
while 1:
	playerDoTurn()
	checkWin()
	AIDoTurn()
	checkWin()