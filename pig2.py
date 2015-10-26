'''David Vayman
IS211_ASSIGNMENT8'''
import random
import time
import operator
import argparse

random.seed(0)  # set random seed for random.choice


class Player(object):
    """
    constructor: name,
                 current_roll_total = 0
    roll(x): calls random.choice on dice object(x)'s side attribute, updates
             current_roll_total and returns value to main game
    hold(y): updates scoreboard object(y) at end of turn if player chooses
             and resets current_roll_total to 0
    """
    def __init__(self, player_name):
        self.name = player_name
        self.current_roll_total = 0
        self.player_type = 'h'

    def roll(self, dice_name):
        throw = random.choice(dice_name.sides)

        if throw > 1:                       # updates current roll if score > 1
            self.current_roll_total += throw
        else:
            self.current_roll_total = 0     # resets current_roll total

        return throw                        # return current throw to main for evaluation

    def hold(self, scoreboard_name):

        scoreboard_name.scoreboard[self.name] += self.current_roll_total    # updates scoreboard
        self.current_roll_total = 0                                         # resets current total


class ComputerPlayer(Player):     # extends player class -- adds private hold limit method and public decision method

    def __init__(self, player_name):
            super(Player, self).__init__()
            self.name = player_name
            self.current_roll_total = 0
            self.player_type = 'c'

    def __hold_limit(self, player_score):
        """
        private method that calculates the hold score on each roll
        """

        low_limit = 25
        high_limit = 100 - player_score

        return low_limit if (low_limit < high_limit) else high_limit

    def decision(self, player_score):                       # this is called in main function before each roll
        """
        returns True for roll, False for hold
        """
        limit = self.__hold_limit(player_score)

        return 'r' if (self.current_roll_total < limit) else 'h'


class Dice(object):

    """
    constructor: num_sides(default=6),
                list comprehension that creates list with range 1 -> num_sides
    """

    def __init__(self, num_sides=6):
        self.sides = [num_sides for num_sides in range(1, num_sides + 1)]


class Scoreboard(object):               # added a score getter method in version2 to work with Computer Player
    """
    attribute: {} - key= Player name/ value = score(int)
    add_player(): creates a new key/value as:  'player name': 0,
    """
    def __init__(self):
        self.scoreboard = {}

    def add_player(self, player):

        self.scoreboard[player] = 0

    def get_score(self, player):

        return self.scoreboard[player]


class Game(object):     # game engine functions / helpers encapsulated in a class

    def __init__(self):
        self.game_time = 0
        self.old_time_stamp = 0
        self.current_time_stamp = 0

    def __update_time(self):
        """
        private method that updates the game_time attribute
        """
        time = self.current_time_stamp - self.old_time_stamp
        self.old_time_stamp = self.current_time_stamp
        self.game_time += time  # increments game time in seconds

    # def proxy_out(self):        # sends time out Proxy
    #     return True if self.game_time < 60 else False

    def __pause(self, seconds):     # private pause method
        return time.sleep(seconds)

    @classmethod                    # class method used to call without object instantiation
    def setup(cls, player1, player2, scoreboard):
        """
        Gets user input for player1 and player2 as string 'h' or 'c'
        Names each player (either ask player or choose from list)
        Creates either human or cpu player using factory
        appends to player list and scoreboard
        returns player_list to main
        """
        factory = Factory()     # initialize factory, player list and robot names
        player_list = []
        robot_names = ['Vasya Petrovich', 'Einstein', 'Louie', 'Ya dalbak']

        player_str_input = player1, player2

        for i in range(len(player_str_input)):

            if player_str_input[i] == 'h':
                prompt = 'Player ' + str(i + 1) + ' What is your name?: '
                user_name = str(raw_input(prompt))

                new_player = factory.spawn(user_name, player_str_input[i])
                player_list.append(new_player)
                scoreboard.add_player(new_player.name)

            elif player_str_input[i] == 'c':
                user_name = random.choice(robot_names)
                robot_names.remove(user_name)           # need to remove robot from list

                new_player = factory.spawn(user_name, player_str_input[i])
                player_list.append(new_player)
                scoreboard.add_player(new_player.name)

        return player_list

    def game_engine(self, player_list, scoreboard, game_dice):
        """
        main game sequence...   outer while loop - continues cycling players until someone wins (return True)
                                for loop - moves through the players in the player list
                                inner while loop - game algorithm -- returns True to main when there is a winner
        In order for it to work with proxy it cannot be an infinite loop. The loop needs to exist outside of the
        game method.
        time init performed by proxy
        """

        for player in player_list:

            while player:

                self.current_time_stamp = time.time()
                self.__update_time()                        # HERE's where Proxy needs to read game time

                print player.name.upper() + ' Its Your turn!'
                self.__pause(.5)

                # BRANCH HERE if human or CPU player
                if player.player_type == 'h':
                    user_input = str(raw_input(player.name +
                                     ', What would your like to do ? roll or hold? Please enter "(r)" or "(h)": ')).lower()
                else:
                    user_input = player.decision(scoreboard.scoreboard[player.name])

                if user_input == 'r':

                    roll = player.roll(game_dice)
                    print player.name.upper() + ' rolled a ' + str(roll) + ' !!'
                    self.__pause(.5)
                    print ''

                    if roll > 1:

                        shadow_total = player.current_roll_total + scoreboard.scoreboard[player.name]

                        if shadow_total >= 100:
                            print player.name.upper() + 's total for this roll = ' + str(player.current_roll_total)
                            print player.name.upper() + 's GRAND TOTAL: ' + str(shadow_total)
                            print ''

                            return True      # EXITS function here on WINNER, returns False to main to break game loop
                        else:
                            print player.name.upper() + 's total for this roll = ' + str(player.current_roll_total)
                            self.__pause(.5)
                            print player.name.upper() + 's GRAND TOTAL: ' + str(shadow_total)
                            print ''

                    else:
                        print 'You Suck' + player.name + ' You lost all your points HAHAHAHAHA!!'

                        print ''
                        print '______________'
                        print '<><><><><><><>'
                        print 'CURRENT SCORES: ' + str(scoreboard.scoreboard)
                        print '<><><><><><><>'
                        print '______________'
                        break       # breaks out of inner loop and goes to next player

                elif user_input == 'h':
                    player.hold(scoreboard)    # calls hold method then breaks out of loop
                    print player.name + ': Decides to hold'

                    print ''
                    print '______________'
                    print '<><><><><><><>'
                    print 'CURRENT SCORES: ' + str(scoreboard.scoreboard)
                    print '<><><><><><><>'
                    print '______________'
                    break       # breaks out of inner loop and goes to next player

                else:
                    print 'Invalid input, try again '
                    print ''


class TimedGameProxy(object):   # timed proxy for game class

    def set_intial_timestamp(self, game):
        game.old_time_stamp = time.time()

    def work(self, game, player_list, scoreboard, dice):
        """
        main proxy method... gets called in loop in main script
        checks if game is over 1 minute on each iteration
        returns True only if winner = False/None to keep outer loop going
        """

        if game.game_time < 60:
            winner = game.game_engine(player_list, scoreboard, dice)
            print "Current Time:: " + str(game.game_time)

            return True if not winner else False

        else:
            print "GAME OVER!!! YOU RAN OUT OF TIME!!"
            return False


class Factory(object):  # can spawn a Player class or ComputerPlayer class depending on input

    def spawn(self, name, player_type):
        return Player(name) if (player_type == "h") else ComputerPlayer(name)


def main():     # main script that takes user input and calls appropriate classes

    parser = argparse.ArgumentParser()
    parser.add_argument("--player1", help=" h for human, c for computer")
    parser.add_argument("--player2", help=" h for human, c for computer")
    parser.add_argument("--timed", help=" y or n for timed game")
    args = parser.parse_args()

    try:

        p1 = args.player1
        p2 = args.player2
        timed = args.timed

        # check input -- if wrong raise Exception
        if (p1 != 'h' and p1 != 'c') or (p2 != 'h' and p2 != 'c') or \
                (timed != 'y' and timed != 'n'):
            raise Exception

        s = Scoreboard()
        player_list = Game.setup(p1, p2, s)

        d = Dice()
        g = Game()

        if timed == 'y':
            t = TimedGameProxy()             # This works for the proxy method
            t.set_intial_timestamp(g)
            while True:
                result = t.work(g, player_list, s, d)
                if not result:
                    break
        else:
            while True:                       # This works for non proxy
                winner = g.game_engine(player_list, s, d)
                if winner:
                    break

        winner = max(s.scoreboard.iteritems(), key=operator.itemgetter(1))[0]
        print ''
        print winner
        print ''
        print '***********************************'
        print 'YOU ARE THE 2015 WORLD CHAMPION!!!!'
        print '___________________________________'

    except Exception:
        print "Please enter the correct information to begin the game. --player1 (h,c) --player2(h,c) and --timed(y,n)\n" \


if __name__ == "__main__":
    main()
