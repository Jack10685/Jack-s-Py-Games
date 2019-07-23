import os
import statistics

position = [" ", " ", " ", " ", " ", " ", " ", " ", " "]

def clear():
	if (os.name == 'nt'):
		os.system('cls')
	else
		os.system('clear')

def disp():
    clear()
    print("     |   |")
    print("   "+position[6]+" | "+position[7]+" | "+position[8]+" ")
    print("     |   |")
    print(" -------------")
    print("     |   |")
    print("   "+position[3]+" | "+position[4]+" | "+position[5]+" ")
    print("     |   |")
    print(" -------------")
    print("     |   |")
    print("   "+position[0]+" | "+position[1]+" | "+position[2]+" ")
    print("     |   |")
    print()
    print()

def checkWin(letter):
    if (position[6] == letter and position[7] == letter and position[8] == letter):
        print("1")
        return True
    elif (position[3] == letter and position[4] == letter and position[5] == letter):
        print("2")
        return True
    elif (position[0] == letter and position[1] == letter and position[2] == letter):
        print("3")
        return True
    elif (position[6] == letter and position[3] == letter and position[0] == letter):
        print("4")
        return True
    elif (position[7] == letter and position[4] == letter and position[1] == letter):
        print("5")
        return True
    elif (position[8] == letter and position[5] == letter and position[2] == letter):
        print("6")
        return True
    elif (position[6] == letter and position[4] == letter and position[2] == letter):
        print("7")
        return True
    elif (position[8] == letter and position[4] == letter and position[0] == letter):
        print("8")
        return True
    else:
        return False

def gameWon(letter):
    disp()
    print(letter+"'s have won!")

def getAINextPosOffensiveInitial():
    i = 0
    while (i < 9):
        if (position[i] == "O" and position[i+1] == "O" and position[i+2] == " "):
            return i+2
        elif (position[i] == "O" and position[i+2] == "O" and position[i+1] == " "):
            return i+1
        elif (position[i+1] == "O" and position[i+2] == "O" and position[i] == " "):
            return i
        i+=3
    i = 6
    while (i < 9):
        if (position[i] == "O" and position[i-3] == "O" and position[i-6] == " "):
            return i-6
        elif (position[i] == "O" and position[i-6] == "O" and position[i-3] == " "):
            return i-3
        elif (position[i-3] == "O" and position[i-6] == "O" and position[i] == " "):
            return i
        i+=1
    if (position[6] == "O" and position[4] == "O" and position[2] == " "):
        return 2
    elif (position[6] == "O" and position[2] == "O" and position[4] == " "):
        return 4
    elif (position[4] == "O" and position[2] == "O" and position[6] == " "):
        return 6
    elif (position[0] == "O" and position[4] == "O" and position[8] == " "):
        return 8
    elif (position[0] == "O" and position[8] == "O" and position[4] == " "):
        return 4
    elif (position[4] == "O" and position[8] == "O" and position[0] == " "):
        return 0
    else:
        return -1;

def getAINextPosDefensive():
    i = 0
    while (i < 9):
        if (position[i] == "X" and position[i+1] == "X" and position[i+2] == " "):
            return i+2
        elif (position[i] == "X" and position[i+2] == "X" and position[i+1] == " "):
            return i+1
        elif (position[i+1] == "X" and position[i+2] == "X" and position[i] == " "):
            return i
        i+=3
    i = 6
    while (i < 9):
        if (position[i] == "X" and position[i-3] == "X" and position[i-6] == " "):
            return i-6
        elif (position[i] == "X" and position[i-6] == "X" and position[i-3] == " "):
            return i-3
        elif (position[i-3] == "X" and position[i-6] == "X" and position[i] == " "):
            return i
        i+=1
    if (position[6] == "X" and position[4] == "X" and position[2] == " "):
        return 2
    elif (position[6] == "X" and position[2] == "X" and position[4] == " "):
        return 4
    elif (position[4] == "X" and position[2] == "X" and position[6] == " "):
        return 6
    elif (position[0] == "X" and position[4] == "X" and position[8] == " "):
        return 8
    elif (position[0] == "X" and position[8] == "X" and position[4] == " "):
        return 4
    elif (position[4] == "X" and position[8] == "X" and position[0] == " "):
        return 0
    else:
        return -1

def getAINextPosOffensiveFinal():
    goodNextMoves = []
    if (position[4] == " "):
        return 4
    else:
        i = 0
        while (i < 9):
            if (position[i] == " "):
                if (i%3 == 0):
                    #left side
                    if (position[i+1] == "O" or position[i+2] == "O"):
                        goodNextMoves.append(i)
                elif (i%3 == 1):
                    #vertical middle
                    if (position[i-1] == "O" or position[i+1] == "O"):
                        goodNextMoves.append(i)

                else:
                    #right side
                    if (position[i-1] == "O" or position[i-2] == "O"):
                        goodNextMoves.append(i)

                if (i < 3):
                    #bottom
                    if (position[i+3] == "O" or position[i+6] == "O"):
                        goodNextMoves.append(i)
                elif (i < 6):
                    #horiontal middle
                    if (position[i+3] == "O" or position[i-3] == "O"):
                        goodNextMoves.append(i)
                else:
                    #top
                    if (position[i-6] == "O" or position[i-3] == "O"):
                        goodNextMoves.append(i)
            i+=1
        if (goodNextMoves):
            return recurseThroughMoveList(goodNextMoves)
        else:
            i = 0
            while(i < 9):
                if (position[i] == " "):
                    return i
                i+=1

def recurseThroughMoveList(goodNextMoves):
    try:
        return statistics.mode(goodNextMoves)
    except statistics.StatisticsError:
        goodNextMoves.pop(len(goodNextMoves)-1)
        return recurseThroughMoveList(goodNextMoves)

def getAINextPos():
    move = getAINextPosOffensiveInitial()
    if (move == -1):
        move = getAINextPosDefensive()
    if (move == -1):
        move = getAINextPosOffensiveFinal()
    return move

def checkTie():
    if (checkWin("X") or checkWin("O")):
        return False
    i = 0
    while (i < 9):
        if (position[i] == " "):
            return False
        i+=1
    return True

def gameTie():
    disp()
    print("Tie game!")

def status(letter):
    if (checkWin(letter)):
        gameWon(letter)
        input()
        return True
    elif (checkTie()):
        gameTie()
        input()
        return True
    else:
        return False

def validateInput(inp):
    try:
        num = int(inp)
        if (num > 9 or num < 1):
            return -1
        else:
            return num
    except ValueError:
        return -1

def vsAI():
	while (True):
		disp()
		nextpos = -1
		nextpos = validateInput(input("Choose a position (using numpad): "))
		while (nextpos == -1 or not position[int(nextpos)-1] == " "):
			disp()
			nextpos = validateInput(input("Invalid choice! Choose a position (using numpad): "))
		position[int(nextpos)-1] = "X"
		if (status("X")):
			break
		position[getAINextPos()] = "O"
		if (status("O")):
			break

def vsPlayer():
	while (True):
		disp()
		nextpos = -1
		nextpos = validateInput(input("Player 1: Choose a position (using numpad): "))
		while (nextpos == -1 or not position[int(nextpos)-1] == " "):
			disp()
			nextpos = validateInput(input("Player 1: Invalid choice! Choose a position (using numpad): "))
		position[int(nextpos)-1] = "X"
		if (status("X")):
			break
		disp()
		nextpos = -1
		nextpos = validateInput(input("Player 2: Choose a position (using numpad): "))
		while (nextpos == -1 or not position[int(nextpos)-1] == " "):
			disp()
			nextpos = validateInput(input("Player 2: Invalid choice! Choose a position (using numpad): "))
		position[int(nextpos)-1] = "O"
		if (status("O")):
			break    	

def help():
	clear()
	print("This screen is to show you how to use this file, if you don't know how to play tic tac toe, google exists, use it.\n")
	print("to make a move, press they number corresponding on your keypad and press enter\n")
	print("if that confuses you or you don't have a keypad, these are the corresponding keys:\n")
	print("     |   |")
	print("   7 | 8 | 9 ")
	print("     |   |")
	print(" -------------")
	print("     |   |")
	print("   4 | 5 | 6 ")
	print("     |   |")
	print(" -------------")
	print("     |   |")
	print("   1 | 2 | 3 ")
	print("     |   |\n\n")
	print("If there are two of you who wish to play against each other, use the option \"Player vs. Player\" \n")
	print("If you are lonely and have no friends, or just don't like people but still want to play, use the option \"Player vs. AI\"\n")
	input("Press enter to be returned to the main screen")
	os.system('cls')
	main()

def main():
	print("Welcome to Tic-Tac-Toe! Please type an option and press enter to get started.\n")
	print("1. Player vs. Player")
	print("2. Player vs. AI")
	print("3. Help")
	option = input()
	while (not (option == "1" or option == "2" or option == "3")):
		option = input()
	if (option == "1"):
		vsPlayer()
	elif (option == "2"):
		vsAI()
	elif (option == "3"):
		help()

main()