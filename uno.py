from abc import ABC, abstractmethod
import random

order = []
deck = []
played = []
currentColor = ""
currentType = ""
gameWon = False


class Card(ABC):
	def __init__(self, type, color):
		self.type = type
		self.color = color
		
	def getType(self):
		return self.type
		
	def getColor(self):
		return self.color
		
	def performSpecial(self):
		pass
		
class NumberCard(Card):
	def performSpecial(self):
		global order
		print(order[-1].getName()+" played a "+self.getColor()+" "+self.getType())
			
class SkipCard(Card):
	def __init__(self, color):
		Card.__init__(self, "Skip", color)
	
	def performSpecial(self):
		global order
		print(order[-1].getName()+" skipped "+order[0].getName())
		order.append(order.pop(0))
				
class ReverseCard(Card):
	def __init__(self, color):
		Card.__init__(self, "Reverse", color)
		
	def performSpecial(self):
		global order
		print(order[-1].getName()+" reversed the order")
		order.reverse()
		order.append(order.pop(0))
		
class DrawTwoCard(Card):
	def __init__(self, color):
		Card.__init__(self, "Draw 2", color)
	
	def performSpecial(self):
		global order
		print(order[-1].getName()+" made "+order[0].getName()+" draw 2 cards")
		order[0].drawCard()
		order[0].drawCard()
		order.append(order.pop(0))
		
class ChangeColorCard(Card):
	def __init__(self):
		Card.__init__(self, "Wild Card", "")
		
	def performSpecial(self):
		global order
		order[-1].requestColor()
		print(order[-1].getName()+" changed the color to "+currentColor)
		
class ChangeColorDraw4Card(Card):
	def __init__(self):
		Card.__init__(self, "Wild Card (Draw 4)", "")
		
	def performSpecial(self):
		global order
		order[-1].requestColor()
		print(order[-1].getName()+" changed the color to "+currentColor+" and made "+order[0].getName()+" draw 4 cards")
		order[0].drawCard()
		order[0].drawCard()
		order[0].drawCard()
		order[0].drawCard()
		order.append(order.pop(0))
		
class Player(ABC):
	def __init__(self, name):
		self.hand = []
		self.name = name

	def drawCard(self):
		global deck
		global played
		if (len(deck) > 0):
			self.hand.append(deck.pop())
		else:
			print("Deck out of cards! reshuffling played cards into deck...")
			topCard = played.pop()
			deck = played
			x = 0
			while (x < 1000):
				random.shuffle(deck)
				x+=1
			played = []
			played.append(topCard)
			self.hand.append(deck.pop())
		print(self.name+" drew a card")
	def getName(self):
		return self.name
	
	def requestColor(self):
		pass
		
	def doTurn(self):
		pass
		
class Human(Player):
	def __init__(self):
		Player.__init__(self, "Player")

	def requestColor(self):
		global currentColor
		global currentType
		global deck
		global played
		global order
		
		newcolor = input("What would you like the new color to be?: ").lower()
		while (not (newcolor == "red" or newcolor == "r" or newcolor == "blue" or newcolor == "b" or newcolor == "green" or newcolor == "g" or newcolor == "orange" or newcolor == "o")):
			newcolor = input("Please enter a valid card color (red, green, blue, orange): ").lower()
		currentColor = newcolor.capitalize()
		
	def doTurn(self):
		global currentColor
		global currentType
		global deck
		global played
		global order
		global gameWon
		
		if (currentColor != "" and currentType != ""):
			print("The current top card is a "+currentColor+" "+currentType)
		elif(currentColor == "" and currentType == ""):
			print("Play any card")
		else:
			print("The current color is "+currentColor)
		print()
		print("Your hand:")
		x = 0
		while (x < len(self.hand)):
			print(self.hand[x].getColor()+" "+self.hand[x].getType())
			x+=1
		
		print()
		print()
		whatdo = input("Would you like to Draw a card or place a card?").lower()
		badInput = False
		foundCard = False
		while(True):
			if (whatdo == "draw" or whatdo == "d"):
				self.drawCard()
				order.append(order.pop(0))
				foundCard = True
				break
			x = 0
			if (whatdo == "wild"):
				wildcardlocation = -1
				wilddraw4location = -1
				x = 0
				while (x < len(self.hand)):
					if (self.hand[x].getType() == "Wild Card (Draw 4)"):
						wilddraw4location = x
					elif (self.hand[x].getType() == "Wild Card"):
						wildcardlocation = x
					x+=1
				cardPos = -1
				if (wildcardlocation == -1 and wilddraw4location == -1):
					print("test")
					badInput = True
				elif (wildcardlocation > -1 and wilddraw4location > -1):
					draw4 = input("Use draw 4 card?")
					if (draw4.lower() == "y" or draw4.lower() == "yes"):
						cardPos = wilddraw4location
					else:
						cardPos = wildcardlocation
				elif (wildcardlocation > -1):
					cardPos = wildcardlocation
				else:
					cardPos = wilddraw4location
				
				if (not badInput):
					order.append(order.pop(0))
					played.append(self.hand.pop(cardPos))
					foundCard = True
					currentType = ""
					played[-1].performSpecial()
					break
					
			if (not foundCard and not badInput):
				while (x < len(self.hand)):
					type1 = self.hand[x].getColor()+" "+self.hand[x].getType()
					type2 = self.hand[x].getColor()+self.hand[x].getType()
					type1 = type1.lower()
					type2 = type2.lower()
					if (whatdo == type1 or whatdo == type2):
						if ((currentColor == self.hand[x].getColor() or currentType == self.hand[x].getType()) or currentColor == ""):
							order.append(order.pop(0))
							played.append(self.hand.pop(x))
							currentColor = played[-1].getColor()
							currentType = played[-1].getType()
							played[-1].performSpecial()
							foundCard = True
							break
					x+=1
				if (foundCard):
					break
			whatdo = input("Please enter a valid input (ie. red skip, blue 4, wild)").lower()
		if (len(self.hand) == 1):
			print("You have UNO!")
		elif (len(self.hand) == 0):
			print("You have won!")
			gameWon = True
			
class AIOpponent(Player):
	def requestColor(self):
		global currentColor
		global currentType
		global deck
		global played
		global order
		orange = 0
		blue = 0
		green = 0
		red = 0
		
		x = 0
		while (x < len(self.hand)):
			if (self.hand[x].getColor() == "Red"):
				red+=1
			elif(self.hand[x].getColor() == "Green"):
				green+=1
			elif(self.hand[x].getColor() == "Blue"):
				blue+=1
			elif(self.hand[x].getColor() == "Orange"):
				orange+=1
			x+=1
		choice = max(orange, green, blue, red)
		if (orange == choice):
			currentColor = "Orange"
		elif (green == choice):
			currentColor = "Green"
		elif (red == choice):
			currentColor = "Red"
		else:
			currentColor = "Blue"
	
	def doTurn(self):
		#matching color?
		global currentColor
		global currentType
		global deck
		global played
		global order
		global gameWon
		
		cardChosen = False
		x = 0
		while (x < len(self.hand)):
			if (self.hand[x].getColor() == currentColor):
				order.append(order.pop(0))
				played.append(self.hand.pop(x))
				currentType = played[-1].getType()
				played[-1].performSpecial()
				cardChosen = True
				break
			x+=1
			
		#matching number?
		if (not cardChosen):
			if (currentType != ""):
				x = 0
				while (x < len(self.hand)):
					if (self.hand[x].getType() == currentType):
						order.append(order.pop(0))
						played.append(self.hand.pop(x))
						currentType = played[-1].getType()
						currentColor = played[-1].getColor()
						played[-1].performSpecial()
						cardChosen = True
						break
					x+=1
					
		#wildcard?
		if (not cardChosen):
			count = 0
			draw4pos = -1
			regpos = -1
			x = 0
			while (x < len(self.hand)):
				if (self.hand[x].getType() == "Wild Card (Draw 4)"):
					count+=1
					draw4pos = x
				elif (self.hand[x].getType() == "Wild Card"):
					count+=1
					regpos = x
				x+=1
			if (count == 0):
				self.drawCard()
				order.append(order.pop(0))
			else:
				order.append(order.pop(0))
				played.append(self.hand.pop(max(draw4pos, regpos)))
				currentType = ""
				played[-1].performSpecial()
				
		if (len(self.hand) == 1):
			print(self.name+" has UNO!")
		elif (len(self.hand) == 0):
			print(self.name+" has won!")
			gameWon = True
			
def setupDeck():
	x = 0
	while (x <= 9):
		deck.append(NumberCard(str(x), "Green"))
		deck.append(NumberCard(str(x), "Blue"))
		deck.append(NumberCard(str(x), "Red"))
		deck.append(NumberCard(str(x), "Orange"))
		x+=1
		
	x = 1
	while (x <= 9):
		deck.append(NumberCard(str(x), "Green"))
		deck.append(NumberCard(str(x), "Blue"))
		deck.append(NumberCard(str(x), "Red"))
		deck.append(NumberCard(str(x), "Orange"))
		x+=1
		
	x = 0
	while(x < 2):
		deck.append(SkipCard("Green"))
		deck.append(SkipCard("Blue"))
		deck.append(SkipCard("Red"))
		deck.append(SkipCard("Orange"))
		
		deck.append(ReverseCard("Green"))
		deck.append(ReverseCard("Blue"))
		deck.append(ReverseCard("Red"))
		deck.append(ReverseCard("Orange"))
		
		deck.append(DrawTwoCard("Green"))
		deck.append(DrawTwoCard("Blue"))
		deck.append(DrawTwoCard("Red"))
		deck.append(DrawTwoCard("Orange"))
		x+=1
	
	deck.append(ChangeColorCard())
	deck.append(ChangeColorCard())
	deck.append(ChangeColorCard())
	deck.append(ChangeColorCard())
		
	deck.append(ChangeColorDraw4Card())
	deck.append(ChangeColorDraw4Card())
	deck.append(ChangeColorDraw4Card())
	deck.append(ChangeColorDraw4Card())
	
	x = 0
	while (x < 1000):
		random.shuffle(deck)
		x+=1
		
def setupGame():
	setupDeck()
	order.append(Human())
	order.append(AIOpponent("Opponent 1"))
	order.append(AIOpponent("Opponent 2"))
	order.append(AIOpponent("Opponent 3"))
	
	x = 0
	while (x < 7):
		order[0].drawCard()
		order[1].drawCard()
		order[2].drawCard()
		order[3].drawCard()
		x+=1
		
def beginGame():
	setupGame()
	print()
	print()
	while(not gameWon):
		print(order[0].getName()+"'s turn:")
		order[0].doTurn()
	input()
	
beginGame()