import random

pool = []
playerHand = []
playerBooks = []
AIHand = []
AIBooks = []

AIPlayerPrevTurns = []
AIAIPrevTurns = []

class Card:
	def __init__(self, number, suite):
		self.number = number
		self.suite = suite
		
	def getNumber(self):
		return self.number
		
	def getSuite(self):
		return self.suite
		
def setupGame():
	x = 2
	while (x <= 10):
		pool.append(Card(str(x), "Clubs"))
		pool.append(Card(str(x), "Diamonds"))
		pool.append(Card(str(x), "Spades"))
		pool.append(Card(str(x), "Hearts"))
		x+=1
		
	pool.append(Card("J", "Clubs"))
	pool.append(Card("J", "Diamonds"))
	pool.append(Card("J", "Spades"))
	pool.append(Card("J", "Hearts"))
		
	pool.append(Card("Q", "Clubs"))
	pool.append(Card("Q", "Diamonds"))
	pool.append(Card("Q", "Spades"))
	pool.append(Card("Q", "Hearts"))
		
	pool.append(Card("K", "Clubs"))
	pool.append(Card("K", "Diamonds"))
	pool.append(Card("K", "Spades"))
	pool.append(Card("K", "Hearts"))
		
	pool.append(Card("A", "Clubs"))
	pool.append(Card("A", "Diamonds"))
	pool.append(Card("A", "Spades"))
	pool.append(Card("A", "Hearts"))
	
	x = 0
	gotil = int(random.random()*1000)
	while (x < gotil):
		random.shuffle(pool)
		x+=1
	
def dealInitialCards():
	x = 0
	while (x < 7):
		playerHand.append(pool.pop())
		AIHand.append(pool.pop())
		x+=1
	checkPlayerInitialBooks()
	checkAIInitialBooks()

def checkPlayerInitialBooks():
	x = 0
	while (x < len(playerHand)-1):
		y = x+1
		while(y < len(playerHand)):
			if (playerHand[x].getNumber() == playerHand[y].getNumber()):
				playerBooks.append(playerHand[x].getNumber())
				print("Started with book of "+playerHand[x].getNumber()+"s!")
				playerHand.pop(y)
				playerHand.pop(x)
				checkPlayerInitialBooks()
				break
			y+=1
		x+=1
	
def checkAIInitialBooks():
	x = 0
	while (x < len(AIHand)-1):
		y = x+1
		while(y < len(AIHand)):
			if (AIHand[x].getNumber() == AIHand[y].getNumber()):
				AIBooks.append(AIHand[x].getNumber())
				AIHand.pop(y)
				AIHand.pop(x)
				checkAIInitialBooks()
				break
			y+=1
		x+=1
		
def dealCard():
	if (len(pool) > 0):
		return pool.pop()
	return False
		
def playerPrintTurnMessage(message):
	print()
	print()
	print()
	
	if (message):
		print(message)
		print()
		
	if (len(pool) > 32):
		print("pool is mostly full")
	elif(len(pool) > 23):
		print("pool is about 3/4 full")
	elif(len(pool) > 16):
		print("pool is about half full")
	elif(len(pool) > 6):
		print("pool is about 1/4 full")
	else:
		print("pool is nearly empty")
	
	print()
	print("Your hand:")
	x = 0
	string = ""
	while (x < len(playerHand)):
		string+=playerHand[x].getNumber()+" of "+playerHand[x].getSuite()
		if (x != len(playerHand)-1):
			string+=", "
		x+=1
	print(string)
	print()
	if (len(playerBooks) > 0):
		string = "Your books: "
		x = 0
		while (x < len(playerBooks)):
			string+=playerBooks[x]+"s"
			if (x != len(playerBooks)-1):
				string+=", "
			x+=1
		print(string)
	if (len(AIBooks) > 0):
		x = 0
		string = "Opponent's books: "
		while (x < len(AIBooks)):
			string+=AIBooks[x]+"s"
			if (x != len(AIBooks)-1):
				string+=", "
			x+=1
		print(string)
	print()
	print()
		
def handContains(hand, number):
	x = 0
	while (x < len(hand)):
		if (hand[x].getNumber() == number):
			return hand.pop(x)
		x +=1
	return False

def validatePick(pick):
	if (pick == "K" or pick == "Q" or pick == "J" or pick == "A"):
		return True
	else:
		try:
			tpick = int(pick)
			if (tpick <= 10 and tpick >= 2):
				return True
		except ValueError:
			return False
		return False
	
def playerTurn(message):
	playerPrintTurnMessage(message)
	if (len(AIHand) > 0):
		print(approxAICards())
		pick = input("Select a card number/letter to take from the opponent's hand: ").upper()
		while (not validatePick(pick)):
			pick = input("Please select a valid number/letter (2-10, J, Q, K, A): ").upper()
		AIPreviousPlayerIncTurns(pick)
		retreivedCard = handContains(AIHand, pick)
		if (not retreivedCard):
			print("Go Fish!")
			retreivedCard = dealCard()
			if (retreivedCard):
				print("Card from pool: "+retreivedCard.getNumber()+" of "+retreivedCard.getSuite())
			else:
				print("pool empty!")
		else:
			print("Received "+retreivedCard.getNumber()+" of "+retreivedCard.getSuite()+" from Opponent")
	else:
		print("Opponent hand is empty.")
		retreivedCard = dealCard()
		if (retreivedCard):
			print("Card from pool: "+retreivedCard.getNumber()+" of "+retreivedCard.getSuite())
		else:
			print("pool is empty")
	x = 0
	madeBook = False
	if (retreivedCard):
		while (x < len(playerHand)):
			if (playerHand[x].getNumber() == retreivedCard.getNumber()):
				AIPlayerRecentBook(playerHand[x].getNumber())
				print("Made a book of "+retreivedCard.getNumber()+"s!")
				playerBooks.append(retreivedCard.getNumber())
				playerHand.pop(x)
				madeBook = True
				break
			x+=1
		if (not madeBook):
			playerHand.append(retreivedCard)
			
	if (len(pool) == 0 and len(playerHand) == 0):
		gameWin()
	else:
		AITurn()

def approxAICards():
	if (len(AIHand) == 1):
		return "Opponent has 1 card."
	elif (len(AIHand) < 6):
		return "Opponent has "+str(len(AIHand))+" cards."
	elif (len(AIHand) < 10):
		return "Opponent has less than 10 cards, but more than 5."
	elif (len(AIHand) < 20):
		return "Opponent has less than 20 cards, but more than 10."
	else:
		return "Opponent has very many cards."

def gameWin():
	print("Your books: "+str(len(playerBooks)))
	print("Opponent's books: "+str(len(AIBooks)))
	print()
	if (len(playerBooks) == len(AIBooks)):
		print("Tie game!")
	elif(len(playerBooks) > len(AIBooks)):
		print("You win!")
	else:
		print("Opponent won!")
	input()
	
def AIPreviousPlayerIncTurns(number):
	if (len(AIPlayerPrevTurns) > 5):
		AIPlayerPrevTurns.pop(0)
	AIPlayerPrevTurns.append(number)
	
def AIPlayerRecentBook(number):
	removeNumberFromPPT(number)

def removeNumberFromPPT(number):
	newList = []
	global AIPlayerPrevTurns
	for item in AIPlayerPrevTurns:
		if (item != number):
			newList.append(item)
	AIPlayerPrevTurns = newList	

def addAIAIPrevTurns(number):
	if (len(AIAIPrevTurns) > 5):
		AIAIPrevTurns.pop(0)
	AIAIPrevTurns.append(number)
	
def AITurn():
	print()
	print()
	print()
	
	message = ""
	if (len(playerHand) > 0):
		chosenCard = ""
		if (len(AIHand) > 0):
			x = 0
			while (x < len(AIHand)):
				y = len(AIPlayerPrevTurns) - 1
				while (y >= 0):
					if (AIHand[x].getNumber() == AIPlayerPrevTurns[y]):
						chosenCard = AIHand[x].getNumber()
						break
					y-=1
				if (chosenCard != ""):
					break
				x+=1
			
			if (chosenCard == ""):
				while (x < len(AIHand)):
					useCard = True
					y = len(AIAIPrevTurns) - 1
					while (y >= 0):
						if (AIHand[x].getNumber() == AIAIPrevTurns[y]):
							useCard = False
							break
						y-=1
					if (useCard):
						chosenCard = AIHand[x].getNumber()
						break
					x+=1
					
			if (chosenCard == ""):
				chosenCard = random.choice(AIHand).getNumber()
		else:
			rlist = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "K", "Q", "A"]*2
			for k in playerBooks:
				rlist.remove(k)
			for k in AIBooks:
				rlist.remove(k)
			chosenCard = random.choice(rlist)
		
		print ("Opponent wants "+chosenCard+"s.")
		addAIAIPrevTurns(chosenCard)
		returned = handContains(playerHand, chosenCard)
		if (not returned):
			returned = dealCard()
			message = "Go Fish! Opponent drew card from pool."
		else:
			message = "Opponent took your "+returned.getNumber()+"s."
			
		madeBook = False
		if (returned):
			x = 0
			while (x < len(AIHand)):
				if (AIHand[x].getNumber() == returned.getNumber()):
					message = message+"\n\nOpponent made a book of "+returned.getNumber()+"s!"
					AIBooks.append(returned.getNumber())
					AIHand.pop(x)
					madeBook = True
					break
				x+=1
			if (not madeBook):
				AIHand.append(returned)
	else:
		returned = dealCard()
		if (returned):
			message = "Opponent drew card from pool."
			madeBook = False
			x = 0
			while (x < len(AIHand)):
				if (AIHand[x].getNumber() == returned.getNumber()):
					print("Opponent made a book of "+returned.getNumber()+"s!")
					AIBooks.append(returned.getNumber())
					AIHand.pop(x)
					madeBook = True
					break
				x+=1
			if (not madeBook):
				AIHand.append(returned)
		else:
			message = "Your hand and the pool are empty. A logic error was made because this should not have run."
			
	if (len(pool) == 0 and len(AIHand) == 0):
		gameWin()
	else:
		playerTurn(message)
			
			
setupGame()
dealInitialCards()
playerTurn("")