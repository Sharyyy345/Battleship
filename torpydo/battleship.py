import random
import os
import colorama
import platform

from colorama import Fore, Back, Style
from torpydo.ship import Color, Letter, Position, Ship
from torpydo.game_controller import GameController
from torpydo.telemetryclient import TelemetryClient

DEBUG = True

############# PROGRAM IS BUILDING/STARTING ############
print("Starting...")
#hi

############# INITIALIZE VARIABLES ###############

global enemy_hit_count
global me_hit_count
global turn_count

player_1_turn = 1
player_2_turn = 1
turn_count = 1 

player_1 = False
player_2 = False

#SHIPS AND PLACEMENT (I think that's what is held in these variables)
myFleet = []
enemyFleet = []

#BOARDS
BoardP1 = {'a1':'~','a2':'~','a3':'~','a4':'~','a5':'~', 'a6':'~','a7':'~', 'a8':'~',
         'b1':'~','b2':'~','b3':'~','b4':'~','b5':'~', 'b6':'~','b7':'~', 'b8':'~',
         'c1':'~','c2':'~','c3':'~','c4':'~','c5':'~', 'c6':'~','c7':'~', 'c8':'~',
         'd1':'~','d2':'~','d3':'~','d4':'~','d5':'~', 'd6':'~','d7':'~', 'd8':'~',
         'e1':'~','e2':'~','e3':'~','e4':'~','e5':'~', 'e6':'~','e7':'~', 'e8':'~',
         'f1':'~','f2':'~','f3':'~','f4':'~','f5':'~', 'f6':'~','f7':'~', 'f8':'~',
         'g1':'~','g2':'~','g3':'~','g4':'~','g5':'~', 'g6':'~','g7':'~', 'g8':'~',
         'h1':'~','h2':'~','h3':'~','h4':'~','h5':'~', 'h6':'~','h7':'~', 'h8':'~'}

BoardP2 = {'a1':'~','a2':'~','a3':'~','a4':'~','a5':'~', 'a6':'~','a7':'~', 'a8':'~',
         'b1':'~','b2':'~','b3':'~','b4':'~','b5':'~', 'b6':'~','b7':'~', 'b8':'~',
         'c1':'~','c2':'~','c3':'~','c4':'~','c5':'~', 'c6':'~','c7':'~', 'c8':'~',
         'd1':'~','d2':'~','d3':'~','d4':'~','d5':'~', 'd6':'~','d7':'~', 'd8':'~',
         'e1':'~','e2':'~','e3':'~','e4':'~','e5':'~', 'e6':'~','e7':'~', 'e8':'~',
         'f1':'~','f2':'~','f3':'~','f4':'~','f5':'~', 'f6':'~','f7':'~', 'f8':'~',
         'g1':'~','g2':'~','g3':'~','g4':'~','g5':'~', 'g6':'~','g7':'~', 'g8':'~',
         'h1':'~','h2':'~','h3':'~','h4':'~','h5':'~', 'h6':'~','h7':'~', 'h8':'~'}





############## DEFINE FUNCTIONS #############

def placingships_info(): 
    print("Starting")
    print("You need to place your ships on the board.")
    print("For each ship, choose the starting coordinates and the orientation (H for horizontal, V for vertical).")
    print("Possible steps:")
    print("1. Enter the starting column (0-8).")
    print("2. Enter the starting row (A-H).")

def takingshot_info():
    print("Your turn to take a shot at the enemy's board.")
    print("Possible steps:")
    print("1. Enter the column to target (0-8).")
    print("2. Enter the wo to target (A-H).")
    print("Note: You cannot target the same spot twice.")

def checkingforshots_info():
    print("After taking a shot, the game will notify you if it was a hit or miss.")
    print("If a hit results in sinking a ship, you will be informed through an explosion.")

def gameover_info():
    print("The game will continue until all ships of one player have been sunk.")
    print("The player who sinks all of the opponent's ships first wins.")


############### MAIN METHOD DEF ##############
def main():
    TelemetryClient.init()
    TelemetryClient.trackEvent('ApplicationStarted', {'custom_dimensions': {'Technology': 'Python'}})
    colorama.init()
    print(Fore.YELLOW + r"""
                                    |__
                                    |\/
                                    ---
                                    / | [
                             !      | |||
                           _/|     _/|-++'
                       +  +--|    |--|--|_ |-
                     { /|__|  |/\__|  |--- |||__/
                    +---------------___[}-_===_.'____                 /\
                ____`-' ||___-{]_| _[}-  |     |_[___\==--            \/   _
 __..._____--==/___]_|__|_____________________________[___\==--____,------' .7
|                        Welcome to Battleship                         BB-61/
 \_________________________________________________________________________|""" + Style.RESET_ALL)

    initialize_game()
    start_game()

############# START GAME METHOD (MAIN LOOP FOR GAME EVENTS) #############

def start_game():
    global myFleet, enemyFleet
    enemy_hit_count = 0
    me_hit_count = 0
    # clear the screen
    if not DEBUG:

        if(platform.system().lower()=="windows"):
            cmd='cls'
        else:
            cmd='clear'   
        os.system(cmd)
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + r'''
       ⠀⢠⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣴⣶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢸⣟⣻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠈⠉⠉⠀⠀''' + Fore.LIGHTBLACK_EX + '''⣶⡆⠀⠀⠀⣀⣀⣤⣤⣶⣶⣶⣶⣶⣶⣶⡆⢰⣶⡄⢰⣤⡀⠀''' + Fore.LIGHTRED_EX + '''
⠀⠀⠀⠀⠀⠀⢸⡇⠰⢾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⡇⢸⣿⣿⠀''' + Fore.LIGHTBLACK_EX + '''
⠀⠀⠀⠀⠀⠀⠿⠇⠀⠀⠀⠉⠉⠛⠛⠿⠿⠿⠿⠿⠿⠿⠇⠸⠿⠃⠸⠛⠁⠀''' + Style.RESET_ALL)
    
    #turncount(turn_count)
    menu(turn_count)

    while (enemy_hit_count != 17 or me_hit_count != 17):
        if (enemy_hit_count == 17 or me_hit_count == 17):
            if (enemy_hit_count == 17):
                print("Congrats, you win!")
                break
            elif(me_hit_count == 17):
                print("GAME OVER")
                break
        print()
        print(Fore.RED + "ENEMY BOARD: ")
        printBoard(BoardP2)

        print(Fore.YELLOW + "Player, it's your turn")
        position = input("Enter coordinates for your shot :")
        positionparse = parse_position(position)
        positionChange = position.lower()
        is_hit = GameController.check_is_hit(enemyFleet, positionparse)


        if is_hit:
            enemy_hit_count = enemy_hit_count + 1
            BoardP2[positionChange] = Fore.RED + "*" + Fore.CYAN
            print(Fore.LIGHTBLACK_EX + Style.DIM + r'''
          _ ._  _ , _ ._
        (_ ' ( `  )_  .__)
      ( (  (    ''' + Fore.LIGHTRED_EX + r''')''' + Fore.LIGHTBLACK_EX + r'''   `)  ) _)
     (__ (_   ''' + Fore.LIGHTRED_EX + r'''(_ ''' + Fore.LIGHTYELLOW_EX + r'''.''' + Fore.LIGHTRED_EX + r''' _)''' + Fore.LIGHTBLACK_EX + r''' _) ,__)
         ''' + Fore.LIGHTRED_EX + r'''`~~`\ ''' + Fore.LIGHTYELLOW_EX + r'''' .''' + Fore.LIGHTRED_EX + r''' /`~~`
              ;   ;
              ''' + Fore.YELLOW + r'''/   \
''' + Style.RESET_ALL + Fore.BLUE + r'''_____________''' + Fore.YELLOW + r'''/_ __ \ ''' + Fore.BLUE + r'''____________''' + '\n')
            print(Style.RESET_ALL + Fore.LIGHTRED_EX + "Yeah! Nice hit!")

        else:
            BoardP2[positionChange] = Fore.WHITE + "*" + Fore.CYAN
            print(Fore.BLUE + "Miss")
        TelemetryClient.trackEvent('Player_ShootPosition', {'custom_dimensions': {'Position': str(position), 'IsHit': is_hit}})

        position = get_random_position()
        is_hit = GameController.check_is_hit(myFleet, position)
        print()
        print(Fore.YELLOW + f"Computer shoot in {str(position)} and {Fore.RED + 'hit your ship!' if is_hit else Fore.BLUE + 'miss'}")
        TelemetryClient.trackEvent('Computer_ShootPosition', {'custom_dimensions': {'Position': str(position), 'IsHit': is_hit}})
        if is_hit:
           me_hit_count = me_hit_count + 1
           print(Fore.LIGHTBLACK_EX + Style.DIM + r'''
          _ ._  _ , _ ._
        (_ ' ( `  )_  .__)
      ( (  (    ''' + Fore.LIGHTRED_EX + r''')''' + Fore.LIGHTBLACK_EX + r'''   `)  ) _)
     (__ (_   ''' + Fore.LIGHTRED_EX + r'''(_ ''' + Fore.LIGHTYELLOW_EX + r'''.''' + Fore.LIGHTRED_EX + r''' _)''' + Fore.LIGHTBLACK_EX + r''' _) ,__)
         ''' + Fore.LIGHTRED_EX + r'''`~~`\ ''' + Fore.LIGHTYELLOW_EX + r'''' .''' + Fore.LIGHTRED_EX + r''' /`~~`
              ;   ;
              ''' + Fore.YELLOW + r'''/   \
''' + Style.RESET_ALL + Fore.BLUE + r'''_____________''' + Fore.YELLOW + r'''/_ __ \ ''' + Fore.BLUE + r'''____________''' + '\n')
           
    




def parse_position(input: str):
    letter = Letter[input.upper()[:1]]
    number = int(input[1:])
    position = Position(letter, number)

    return Position(letter, number)


def get_random_position():
    rows = 8
    lines = 8

    letter = Letter(random.randint(1, lines))
    number = random.randint(1, rows)
    position = Position(letter, number)

    return position



def initialize_game():
    initialize_myFleet()
    initialize_enemyFleet()


############ PRINTING THE GAME BOARD METHOD ############
def printBoard(board):
    print(Fore.LIGHTMAGENTA_EX + '  1 2 3 4 5 6 7 8')
    
    print(Fore.LIGHTMAGENTA_EX + 'A'+ ' ' + Style.RESET_ALL + Fore.CYAN + board['a1'] + ' ' + board['a2'] + ' ' + board['a3'] + ' ' + board['a4'] + ' ' + board['a5'] + ' ' + board['a6'] + ' ' + board['a7'] + ' ' + board['a8'])
    
    print(Fore.LIGHTMAGENTA_EX + 'B'+ ' ' + Style.RESET_ALL + Fore.CYAN + board['b1'] + ' ' + board['b2'] + ' ' + board['b3'] + ' ' + board['b4'] + ' ' + board['b5'] + ' ' + board['b6'] + ' ' + board['b7'] + ' ' + board['b8'])

    print(Fore.LIGHTMAGENTA_EX + 'C'+ ' ' + Style.RESET_ALL + Fore.CYAN + board['c1'] + ' ' + board['c2'] + ' ' + board['c3'] + ' ' + board['c4'] + ' ' + board['c5'] + ' ' + board['c6'] + ' ' + board['c7'] + ' ' + board['c8'])

    print(Fore.LIGHTMAGENTA_EX + 'D'+ ' ' + Style.RESET_ALL + Fore.CYAN + board['d1'] + ' ' + board['d2'] + ' ' + board['d3'] + ' ' + board['d4'] + ' ' + board['d5'] + ' ' + board['d6'] + ' ' + board['d7'] + ' ' + board['d8'])

    print(Fore.LIGHTMAGENTA_EX + 'E'+ ' ' + Style.RESET_ALL + Fore.CYAN + board['e1'] + ' ' + board['e2'] + ' ' + board['e3'] + ' ' + board['e4'] + ' ' + board['e5'] + ' ' + board['e6'] + ' ' + board['e7'] + ' ' + board['e8'])

    print(Fore.LIGHTMAGENTA_EX + 'F'+ ' ' + Style.RESET_ALL + Fore.CYAN + board['f1'] + ' ' + board['f2'] + ' ' + board['f3'] + ' ' + board['f4'] + ' ' + board['f5'] + ' ' + board['f6'] + ' ' + board['f7'] + ' ' + board['f8'])

    print(Fore.LIGHTMAGENTA_EX + 'G'+ ' ' + Style.RESET_ALL + Fore.CYAN + board['g1'] + ' ' + board['g2'] + ' ' + board['g3'] + ' ' + board['g4'] + ' ' + board['g5'] + ' ' + board['g6'] + ' ' + board['g7'] + ' ' + board['g8'])

    print(Fore.LIGHTMAGENTA_EX + 'H'+ ' ' + Style.RESET_ALL + Fore.CYAN + board['h1'] + ' ' + board['h2'] + ' ' + board['h3'] + ' ' + board['h4'] + ' ' + board['h5'] + ' ' + board['h6'] + ' ' + board['h7'] + ' ' + board['h8'])
    print('\n')

############ PLACING PLAYER 1 SHIPS #############
def initialize_myFleet():
    global myFleet

    turn_count = 1

    menu(turn_count)

    myFleet = GameController.initialize_ships()
    usedSpaces = []
    print(Fore.GREEN + "Please position your fleet:")
    printBoard(BoardP1)

    for ship in myFleet:
        print()
        print(f"Please enter the position for the {ship.name} (size: {ship.size})")
        for i in range(ship.size):
            position_input = validateShipPlace(usedSpaces, i, ship.size)
            ship.add_position(position_input)
            usedSpaces.append(position_input)
            position_input = position_input.lower()
            BoardP1[position_input] = Fore.GREEN + '0' + Fore.CYAN
            TelemetryClient.trackEvent('Player_PlaceShipPosition', {'custom_dimensions': {'Position': position_input, 'Ship': ship.name, 'PositionInShip': i}})
        printBoard(BoardP1)

def validateShipPlace(usedSpaces, iter, shipSize):
    while True:
        valposin = []
        position_input = input(f"Enter position {iter} of {shipSize} (i.e A3):")
        #orientation = input(f"Enter orientation of {ship} (i.e. h for horizontal, v for vertical):")
        #orientation = orientation.lower()
        valposin.extend(position_input)
    #VALIDATE POSITION EXISTS AT ALL ON GRID
        if valposin[0].lower() not in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'] or int(valposin[1]) not in range(1,9) or len(valposin) >= 3:
            print("That is not a valid ship placement. Please enter another space.")


    #VALIDATE THERE'S NO OTHER SHIP THERE
        elif position_input in usedSpaces: 
            print("You have already placed a ship there. You must pick a different spot.")

        else:
            return position_input #, orientation
    #VALIDATE THAT IS AN ACCEPTABLE ORIENTATION FOR THAT SHIP
    #except orientation != 'h' or orientation != 'v':
        #print("That is not an acceptable orientation. You must enter H or V.")
        #validateShipPlace()



################## PLACING PLAYER 2 OR COMPUTER SHIPS ################ (can implement the 2 player later)
def initialize_enemyFleet():
    global enemyFleet

    turn_count = 1
    menu(turn_count)

    enemyFleet = GameController.initialize_ships()
    
    pos = random.choice(possiblePos)

    if DEBUG:
        print(pos)

    k = 0
    x = 0

    for i in range(0,5,1):
        if i == 0:
            x = 4
            if DEBUG:
                print("Carrier Adding...\n")
        elif i == 1:
            x = 3
            if DEBUG:
                print("Battleship Adding...\n")
        elif i == 2:
            x = 2
            if DEBUG:
                print("Submarine Adding...\n")
        elif i == 3:
            x = 2
            if DEBUG:
                print("Destroyer Adding...\n")
        elif i == 4:
            x = 1
            if DEBUG:
                print("Patrol Adding...\n")
        for j in range(0,x+1,1):
            enemyFleet[i].positions.append(pos[k])
            k += 1
        if DEBUG:
                print("Added\n")
    
    #Possible Game Boards For Enemy Computer
possiblePos = [[Position(Letter.B, 4),
                Position(Letter.B, 5),
                Position(Letter.B, 6),
                Position(Letter.B, 7),
                Position(Letter.B, 8),

                Position(Letter.C, 5),
                Position(Letter.C, 6),
                Position(Letter.C, 7),
                Position(Letter.C, 8),

                Position(Letter.A, 3),
                Position(Letter.B, 3),
                Position(Letter.C, 3),

                Position(Letter.F, 8),
                Position(Letter.G, 8),
                Position(Letter.H, 8),

                Position(Letter.E, 5),
                Position(Letter.E, 6)],
                
                
                [Position(Letter.C, 4),
                Position(Letter.C, 5),
                Position(Letter.C, 6),
                Position(Letter.C, 7),
                Position(Letter.C, 8),

                Position(Letter.G, 4),
                Position(Letter.G, 5),
                Position(Letter.G, 6),
                Position(Letter.G, 7),

                Position(Letter.B, 4),
                Position(Letter.C, 4),
                Position(Letter.D, 4),

                Position(Letter.F, 2),
                Position(Letter.G, 2),
                Position(Letter.H, 2),

                Position(Letter.F, 8),
                Position(Letter.G, 8)],
                
                [Position(Letter.B, 4),
                Position(Letter.B, 5),
                Position(Letter.B, 6),
                Position(Letter.B, 7),
                Position(Letter.B, 8),

                Position(Letter.E, 5),
                Position(Letter.E, 6),
                Position(Letter.E, 7),
                Position(Letter.E, 8),

                Position(Letter.B, 3),
                Position(Letter.C, 3),
                Position(Letter.D, 3),

                Position(Letter.F, 8),
                Position(Letter.G, 8),
                Position(Letter.H, 8),

                Position(Letter.C, 7),
                Position(Letter.C, 8)],
                
                [Position(Letter.B, 4),
                Position(Letter.B, 5),
                Position(Letter.B, 6),
                Position(Letter.B, 7),
                Position(Letter.B, 8),

                Position(Letter.E, 5),
                Position(Letter.E, 6),
                Position(Letter.E, 7),
                Position(Letter.E, 8),

                Position(Letter.B, 3),
                Position(Letter.C, 3),
                Position(Letter.D, 3),

                Position(Letter.F, 7),
                Position(Letter.G, 7),
                Position(Letter.H, 7),

                Position(Letter.C, 8),
                Position(Letter.C, 9)]]

################ CREATING GAME MENUS ##############
def menu(turn_count):
    turnStr = Fore.BLUE + "***TURN {}***".format(turn_count)
    optStr = Fore.BLUE + "Here are your options:"
    space = " "
    initStr = Fore.GREEN + "Initialize your Fleet!"
    shootStr = Fore.RED + "Try to shoot your enemy!"
    print(Fore.BLUE + "*----------------------------------------*")
    print(Fore.BLUE + "*", space.center(38, ' '), Fore.BLUE + "*")
    print(Fore.BLUE + "*", turnStr.center(43, ' '), Fore.BLUE + "*")
    print(Fore.BLUE + "*", optStr.center(43, ' '), Fore.BLUE + "*")
    print(Fore.BLUE + "*", space.center(36), ' ', Fore.BLUE + "*")
    if (turn_count == 1):
        print(Fore.BLUE + "*", initStr.center(41), ' ', Fore.BLUE + "*")
    if (turn_count > 1):
        print(Fore.BLUE + "*", shootStr.center(36), ' ', Fore.BLUE + "*")
        
    print(Fore.BLUE + "*", space.center(36), ' ', Fore.BLUE + "*") 
    print(Fore.BLUE + "*----------------------------------------*")
    return turn_count + 1

#def turncount(turn_count):
    #return turn_count + 1


################### ACTUAL PROGRAM STARTS HERE ####################

##################### ENTRY POINT FOR MAIN ##########################
if __name__ == '__main__':
    main()
