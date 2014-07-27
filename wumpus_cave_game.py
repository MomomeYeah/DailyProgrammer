#http://www.reddit.com/r/dailyprogrammer/comments/21kqjq/4282014_challenge_154_hard_wumpus_cave_game/

from random import *
from colorama import *
import os

#Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
#Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
#Style: DIM, NORMAL, BRIGHT, RESET_ALL

class hero():
    def __init__(self, xLoc, yLoc):
        self.dead = False
        self.armed = False
        self.points = 0
        self.xLoc = xLoc
        self.yLoc = yLoc

    def __str__(self):
        return (Fore.RED + '@' + Fore.RESET)

    def print_pos(self):
        print str(self.xLoc)+", "+str(self.yLoc)

    def is_at(self, xLoc, yLoc):
        return self.xLoc == xLoc and self.yLoc == yLoc

    def setPos(self, xLoc, yLoc):
        self.xLoc = xLoc
        self.yLoc = yLoc

    def addPoints(self, points):
        self.points += points

class room(object):
    def __init__(self, xLoc, yLoc, explored = False):
        self.explored = explored
        self.xLoc = xLoc
        self.yLoc = yLoc

    def explore(self, hero):
        self.explored = True
        hero.setPos(self.xLoc, self.yLoc)
        hero.addPoints(1)
        return "There's nothing here"

    def __str__(self):
        return (Fore.GREEN + '.' + Fore.RESET) if self.explored else '?'

    def __name__(self):
        return "Empty Room"

class wall(room):
    def __init__(self, xLoc, yLoc):
        room.__init__(self, xLoc, yLoc)

    def explore(self, hero):
        return "This is a wall, you can't explore here!"

    def __str__(self):
        return (Fore.BLUE + '#' + Fore.RESET)

    def __name__(self):
        return 'Wall'

class entrance_room(room):
    def __init__(self, xLoc, yLoc):
        room.__init__(self, xLoc, yLoc)

    def explore(self, hero):
        hero.setPos(self.xLoc, self.yLoc)
        return "You are at the entrance.  Press R to run away!"

    def __str__(self):
        return '^'

    def __name__(self):
        return 'Entrance'

class wumpus_room(room):
    def __init__(self, xLoc, yLoc):
        room.__init__(self, xLoc, yLoc)

    def explore(self, hero):
        self.explored = True
        hero.setPos(self.xLoc, self.yLoc)
        if hero.armed:
            self.explored = True
            hero.addPoints(10)
            return "You slayed a wumpus!"
        else:
            hero.dead = True
            return "You were slain by a wumpus!"

    def __str__(self):
        return room.__str__(self)

    def __name__(self):
        return 'Wumpus Room'

class pit_trap_room(room):
    def __init__(self, xLoc, yLoc):
        room.__init__(self, xLoc, yLoc)

    def explore(self, hero):
        hero.setPos(self.xLoc, self.yLoc)
        hero.dead = True
        return "You died to a pit trap, how unfortunate!"

    def __str__(self):
        return room.__str__(self)

    def __name__(self):
        return 'Pit Trap Room'

class gold_room(room):
    def __init__(self, xLoc, yLoc):
        room.__init__(self, xLoc, yLoc)
        self.loot_taken = False

    def explore(self, hero):
        self.explored = True
        hero.setPos(self.xLoc, self.yLoc)
        return "You found a gold room!  Press L to loot!"

    def loot(self, hero):
        self.loot_taken = True
        hero.addPoints(5)
        return "You picked up some gold!"

    def __str__(self):
        if self.explored:
            return '.' if self.loot_taken else (Fore.YELLOW + '$' + Fore.RESET)
        else:
            return '?'

    def __name__(self):
        return 'Gold Room'

class weapon_room(room):
    def __init__(self, xLoc, yLoc):
        room.__init__(self, xLoc, yLoc)
        self.loot_taken = False

    def explore(self, hero):
        self.explored = True
        hero.setPos(self.xLoc, self.yLoc)
        return "You found a weapon room!  Press L to loot!"

    def loot(self, hero):
        self.loot_taken = True
        hero.armed = True
        hero.addPoints(5)
        return "You picked up a weapon!"

    def __str__(self):
        if self.explored:
            return '.' if self.loot_taken else (Fore.YELLOW + 'W' + Fore.RESET)
        else:
            return '?'

    def __name__(self):
        return 'Weapon Room'

class cave():
    def __init__(self, game_size):
        self.rooms = []
        number_of_rooms = game_size ** 2

        top_wall = []
        for i in range(game_size + 2):
            w = wall(0, i)
            top_wall.append(w)
        self.rooms.append(top_wall)

        for i in range(1, game_size + 1):
            room_row = []
            w = wall(i, 0)
            room_row.append(w)
            for j in range(1, game_size + 1):
                r = room(i, j)
                room_row.append(r)
            w = wall(i, game_size + 1)
            room_row.append(w)
            self.rooms.append(room_row)

        rooms_assigned = 0
        while(rooms_assigned < 1):
            x = randint(1, game_size)
            y = randint(1, game_size)
            if self.rooms[x][y].__name__() == 'Empty Room':
                er = entrance_room(x, y)
                self.rooms[x][y] = er
                self.hero = hero(x, y)
                rooms_assigned += 1

        rooms_assigned = 0
        while(rooms_assigned < int(number_of_rooms * 15 / 100)):
            x = randint(1, game_size)
            y = randint(1, game_size)
            if self.rooms[x][y].__name__() == 'Empty Room':
                wr = wumpus_room(x,y)
                self.rooms[x][y] = wr
                rooms_assigned += 1

        rooms_assigned = 0
        while(rooms_assigned < int(number_of_rooms * 5 / 100)):
            x = randint(1, game_size)
            y = randint(1, game_size)
            if self.rooms[x][y].__name__() == 'Empty Room':
                ptr = pit_trap_room(x,y)
                self.rooms[x][y] = ptr
                rooms_assigned += 1

        rooms_assigned = 0
        while(rooms_assigned < int(number_of_rooms * 15 / 100)):
            x = randint(1, game_size)
            y = randint(1, game_size)
            if self.rooms[x][y].__name__() == 'Empty Room':
                gr = gold_room(x,y)
                self.rooms[x][y] = gr
                rooms_assigned += 1

        rooms_assigned = 0
        while(rooms_assigned < int(number_of_rooms * 15 / 100)):
            x = randint(1, game_size)
            y = randint(1, game_size)
            if self.rooms[x][y].__name__() == 'Empty Room':
                wr = weapon_room(x,y)
                self.rooms[x][y] = wr
                rooms_assigned += 1

        bottom_wall = []
        for i in range(game_size + 2):
            w = wall(game_size + 1, i)
            bottom_wall.append(w)
        self.rooms.append(bottom_wall)

    def explore_room(self, xLoc, yLoc):
        output = self.rooms[xLoc][yLoc].explore(self.hero)
        if self.rooms[xLoc][yLoc].__name__() == 'Wumpus Room' and not self.hero.dead:
            self.rooms[xLoc][yLoc] = room(xLoc, yLoc, True)
        return output

    def loot_room(self, xLoc, yLoc):
        r = self.rooms[xLoc][yLoc]
        if r.__name__() == 'Gold Room':
             message = r.loot(self.hero)
             self.rooms[xLoc][yLoc] = room(xLoc, yLoc, True)
             return message
        elif r.__name__() == 'Weapon Room':
            message = r.loot(self.hero)
            self.rooms[xLoc][yLoc] = room(xLoc, yLoc, True)
            for i in range(1, len(self.rooms)):
                for j in range(1, len(self.rooms)):
                    if self.rooms[i][j].__name__() == 'Weapon Room' and not self.rooms[i][j].explored:
                        self.rooms[i][j] = gold_room(i,j)
            return message
        else:
            return 'There is nothing to loot!'

    def pos_next_to_room(self, xLoc, yLoc, room_type):
        nr = self.rooms[xLoc - 1][yLoc]
        sr = self.rooms[xLoc + 1][yLoc]
        er = self.rooms[xLoc][yLoc + 1]
        wr = self.rooms[xLoc][yLoc - 1]
        return nr.__name__() == room_type or sr.__name__() == room_type or er.__name__() == room_type or wr.__name__() == room_type

    def __str__(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        output = ""
        for i in range(len(self.rooms)):
            row_str = "\n"
            for j in range(len(self.rooms)):
                row_str += " "+str(self.hero)+" " if self.hero.is_at(i, j) else " "+str(self.rooms[i][j])+" "
            output += row_str+'\n'
        return output

    def print_warnings(self):
        if self.pos_next_to_room(self.hero.xLoc, self.hero.yLoc, 'Wumpus Room'):
            print 'A foul stench fills the air\n'

        if self.pos_next_to_room(self.hero.xLoc, self.hero.yLoc, 'Pit Trap Room'):
            print 'You hear the sound of rushing winds\n'

    def print_status(self):
        print '['+str(self.hero.points)+' points earned] ' + 'You are armed\n' if self.hero.armed else 'You are weaponless\n'

def main():
    game_size = int(raw_input("\nPlease enter game size (10 - 20): "))
    if game_size < 10 or game_size > 20:
        print "Game size must be between 10 and 20!"
        return

    # init colorama
    init()

    c = cave(game_size)

    print c
    c.print_warnings()
    c.print_status()

    command = raw_input("Enter Command (? for help): ")
    last_message = ""
    while(True):
        if command == 'X':
            print
            break
        elif command == 'R':
            if c.rooms[c.hero.xLoc][c.hero.yLoc].__name__() == 'Entrance':
                print '\nYou have made it out alive!\n'
                break
            else:
                last_message = 'You must get to the entrance before you can run away!'
        elif command == 'L':
            last_message = c.loot_room(c.hero.xLoc, c.hero.yLoc)
        elif command == 'N':
            _xLoc = c.hero.xLoc - 1
            _yLoc = c.hero.yLoc
            last_message = c.explore_room(_xLoc, _yLoc)
        elif command == 'S':
            _xLoc = c.hero.xLoc + 1
            _yLoc = c.hero.yLoc
            last_message = c.explore_room(_xLoc, _yLoc)
        elif command == 'E':
            _xLoc = c.hero.xLoc
            _yLoc = c.hero.yLoc + 1
            last_message = c.explore_room(_xLoc, _yLoc)
        elif command == 'W':
            _xLoc = c.hero.xLoc
            _yLoc = c.hero.yLoc - 1
            last_message = c.explore_room(_xLoc, _yLoc)
        elif command == '?':
            last_message = "Press N, S, E or W to go North, South, East or West.  Press X to quit."
        elif command == 'NAME':
            last_message = c.rooms[c.hero.xLoc][c.hero.yLoc].__name__()
        elif command == 'POS':
            last_message = str(c.hero.xLoc)+", "+str(c.hero.yLoc)
        
        print c
        print last_message + '\n'

        if c.hero.dead:
            break
        else:
            c.print_warnings()
            c.print_status()
            command = raw_input("Enter Command (? for help): ")
            

    print "Game Over!  You scored "+str(c.hero.points)+" points!"

main()
