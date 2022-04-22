# Dungeon Egg Hunt Using object-oriented programming principles,
#  create an egg hunt game. Your objective is to go through the dungeon to collect the basket and the eggs. 
# Once you've retrieved all of the items, exit through the door.

# RULES:

# 1. Player, Monster, Door, Basket and the 3 Eggs must all start at a random locations on a 5x5 grid.

# 2. Player must collect the Basket first before collecting the 3 Eggs. 
# Player will not be able to collect any Eggs until it first has collected the Basket.

# 3. Once Player collects the Basket, then and only then will it be able to collect any Eggs.

# 4. When Player collects the Basket and the 3 Eggs, Player will need to head toward the Door.

# 5. The entire time the Player is searching for the Eggs, Basket and the Door, 
# there will be a Monster trying to eat the Player.

# 6. If the Monster lands on the same space as the Player, or the Player lands on 
# the same space as the Monster, the game ends and the game will prompt the user to play again.

# 7. If Player reaches the Door before the Monster catches them, you win the game 
# and the game will prompt the user to play again.

# 8. The Player does not know where any of the other tokens are, so all of the 
# tokens with the exception of the Player will be hidden.

# 9. (Optional) If a player lands on a Trap Door then they loose all their items 
# and enter a new floor with all new items/monsters

# Note: For debugging purposes, you can create tokens for each of the other tokens. For example:

# Player (P) Monster (M) Eggs (O) Basket (U) Door (D)

import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Game:
    def __init__(self, moves=0):
        self.number_of_moves=moves
        self.player = Player(self.number_of_moves)
        self.monster = Monster(self.player)
        self.basket = Basket(self.player)
        self.egg1 = Egg(self.player)
        self.egg2 = Egg(self.player)
        self.egg3 = Egg(self.player)
        self.door = Door(self.player)
        self.trapdoor = TrapDoor(self.player)
        self.obj_on_map = [self.basket, self.egg1, self.egg2, self.egg3, self.trapdoor, self.door, self.monster]
        self.check_monster_pos()

    def check_monster_pos(self):
        if self.player.y == self.monster.y and self.player.x == self.monster.x:
            self.monster=Monster(self.player)
            self.check_monster_pos()

    def draw_map(self):
        j=0 #xval
        k=0 #yval 

        mapstring=''
        for i in range(25):
            if(j>4):
                mapstring +=' \n'
                j=0
                k +=1
            # draw the player on the map
            if k==self.player.y and j == self.player.x:
                mapstring+='[P]'
                # for obj in self.obj_on_map:
                #     print(f"{obj.name} x: {obj.y} y:{obj.x}")
                # print(f"player x:{self.player.y} y: {self.player.x}")
            else:
                mapstring+='[ ]'
            j+=1
        print(mapstring)
        print(f"Moves: {self.player.number_of_moves}")
        invstring=''
        for item in set(self.player.items):
            invstring+=f"{item} x {self.player.items.count(item)}"
        print(f"You inventory: {invstring}")

    def init_game(self):
        while not self.player.game_over:
            self.draw_map()


            self.player.move()
            self.player.look_in_room(self.obj_on_map)
            self.monster.move()
        again=input("Do you want to play again? Y/N").capitalize()
        if again == "Y":
            #start a new game
            Game.play_game()

    @classmethod
    def play_game(cls, moves=0):
        game=Game(moves)
        game.init_game()


class Token:

    def __init__(self, player):
        import random
        self.y = random.randint(0,4)
        self.x = random.randint(0,4)
        self.player = player


class Player(Token):

    def __init__(self, number_of_moves, player=None):
        super().__init__(player)
        self.items = []
        self.game_over = False
        self.number_of_moves = number_of_moves

    def move(self):
        s = input("Which was to you want to go? N, S, E, W?").capitalize()
        clear_screen()
        if s=="N":
            if self.y-1 < 0:
                print("You hit a wall, move again")
            else:
                self.y -= 1
        elif s=="E":
            if self.x+1 > 4:
                print("You hit a wall, move again")
            else:
                self.x += 1
        elif s=="S":
            if self.y+1 > 4:
                print("You hit a wall, move again")
            else:
                self.y += 1
        elif s=="W":
            if self.x-1 < 0:
                print("You hit a wall, move again")
            else:
                self.x -= 1
        self.number_of_moves+=1

    def look_in_room(self, obj_on_map):
        for obj in obj_on_map:
            if obj.y == self.y and obj.x == self.x:
                obj.found()


class Monster(Token):
    def __init__(self, player):
        super().__init__(player)
        self.name="Monster"
    
    def move(self):
        import random
        newy = self.y
        newx = self.x
        newy += random.randint(-1,1)
        newx += random.randint(-1,1)
        if newy >4 or newx >4 or newy<0 or newx <0:
            self.move()
        else:
            self.y=newy
            self.x=newx

    def found(self):
        print("You have been eaten by the Monster")
        self.player.game_over=True


class Egg(Token):
    def __init__(self, player):
        super().__init__(player)
        self.name = "Egg"
        self.picked_up = False
    
    def found(self):
        if not self.picked_up:
            print("You found an Egg")
            if "Basket" in self.player.items:
                self.player.items.append("Egg")
                print("You put the egg in your basket")
                self.picked_up = True
            else:
                print("You need a basket ot pick up an egg")

class Basket(Token):
    def __init__(self, player):
        super().__init__(player)
        self.name="Basket"
        self.picked_up = False

    def found(self):
        if not self.picked_up:
            print("You found the basket")
            self.player.items.append("Basket")
            self.picked_up = True

class Door(Token):
    def __init__(self, player):
        super().__init__(player)
        self.name="Door"
    
    def found(self):
        print("You found a Door")
        if self.player.items.count("Egg") == 3:
            print("You made it out Alive!")
            self.player.game_over = True


class TrapDoor(Token):
    def __init__(self, player):
        super().__init__(player)
        self.name = "Trap Door"

    def found(self):
        print("Oh No! You fell through a Trap Door \n You lost ALL you items in the fall \n You are now on a different floor")
        Game.play_game(self.player.number_of_moves) 

#Driver Code
if __name__ == '__main__':
    Game.play_game()