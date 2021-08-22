"""CS 61A Presents The Game of Hog."""

from dice import six_sided, four_sided, make_test_dice
from ucb import main, trace, interact
import math
GOAL_SCORE = 100  # The goal of Hog is to score 100 points.
FIRST_101_DIGITS_OF_PI = 31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679

######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    sum = 0
    k = 0
    temp = 0
    pig_out = 1
    while k < num_rolls:
        temp = dice()
        sum += temp
        if temp == 1:
            pig_out = 0
        k += 1
    if pig_out == 1:
        return sum
    else:
        return 1
    # END PROBLEM 1


def free_bacon(score):
    """Return the points scored from rolling 0 dice (Free Bacon).

    score:  The opponent's current score.
    """
    assert score < 100, 'The game should be over.'
    pi = FIRST_101_DIGITS_OF_PI

    # Trim pi to only (score + 1) digit(s)
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    pi = pi // pow(10, 100 - score)
    # END PROBLEM 2

    return pi % 10 + 3


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    if num_rolls == 0:
        return free_bacon(opponent_score)
    else:
        return roll_dice(num_rolls, dice)
    # END PROBLEM 3


def extra_turn(player_score, opponent_score):
    """Return whether the player gets an extra turn."""
    return (pig_pass(player_score, opponent_score) or
            swine_align(player_score, opponent_score))


def swine_align(player_score, opponent_score):
    """Return whether the player gets an extra turn due to Swine Align.

    player_score:   The total score of the current player.
    opponent_score: The total score of the other player.

    >>> swine_align(30, 45)  # The GCD is 15.
    True
    >>> swine_align(35, 45)  # The GCD is 5.
    False
    """
    # BEGIN PROBLEM 4a
    "*** YOUR CODE HERE ***"
    a1, a2 = player_score, opponent_score
    if a1 == 0 or a2 == 0:
        return False

    while a1 != 0:
        a1, a2 = a2 % a1, a1
    if a2 >= 10:
        return True
    else:
        return False
    # END PROBLEM 4a


def pig_pass(player_score, opponent_score):
    """Return whether the player gets an extra turn due to Pig Pass.

    player_score:   The total score of the current player.
    opponent_score: The total score of the other player.

    >>> pig_pass(9, 12)
    False
    >>> pig_pass(10, 12)
    True
    >>> pig_pass(11, 12)
    True
    >>> pig_pass(12, 12)
    False
    >>> pig_pass(13, 12)
    False
    """
    # BEGIN PROBLEM 4b
    "*** YOUR CODE HERE ***"
    if player_score < opponent_score and opponent_score - player_score < 3:
        return True
    else:
        return False
    # END PROBLEM 4b


def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who


def silence(score0, score1):
    """Announce nothing (see Phase 2)."""
    return silence


def play(strategy0, strategy1, score0=0, score1=0, dice=six_sided,
         goal=GOAL_SCORE, say=silence):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    score0:     Starting score for Player 0
    score1:     Starting score for Player 1
    dice:       A function of zero arguments that simulates a dice roll.
    goal:       The game ends and someone wins when this score is reached.
    say:        The commentary function to call at the end of the first turn.
    """
    who = 0  # Who is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    # while score0 < goal and score1 < goal:
    #     turnplus = True
    #     while  turnplus and score0 < goal and score1 < goal:
    #         if who < 1:
    #             score0 += take_turn(strategy0(score0, score1), score1, dice)
    #             turnplus = extra_turn(score0, score1)
    #         else:
    #             score1 += take_turn(strategy1(score1, score0), score0, dice)
    #             turnplus = extra_turn(score1, score0)
    #         say = say(score0, score1)
    #     who = other(who)

    turnplus = True
    while score0 < goal and score1 < goal:
        if who < 1:
            score0 += take_turn(strategy0(score0, score1), score1, dice)
            turnplus = extra_turn(score0, score1)
        else:
            score1 += take_turn(strategy1(score1, score0), score0, dice)
            turnplus = extra_turn(score1, score0)
        say = say(score0, score1)
        if turnplus is False:
            who = other(who)
        # BEGIN PROBLEM 6
        "*** YOUR CODE HERE ***"
        # END PROBLEM 6
    # END PROBLEM 5
    # (note that the indentation for the problem 6 prompt (***YOUR CODE HERE***) might be misleading)

    return score0, score1


#######################
# Phase 2: Commentary #
#######################


def say_scores(score0, score1):
    """A commentary function that announces the score for each player."""
    print("Player 0 now has", score0, "and Player 1 now has", score1)
    return say_scores


def announce_lead_changes(last_leader=None):
    """Return a commentary function that announces lead changes.

    >>> f0 = announce_lead_changes()
    >>> f1 = f0(5, 0)
    Player 0 takes the lead by 5
    >>> f2 = f1(5, 12)
    Player 1 takes the lead by 7
    >>> f3 = f2(8, 12)
    >>> f4 = f3(8, 13)
    >>> f5 = f4(15, 13)
    Player 0 takes the lead by 2
    """
    def say(score0, score1):
        if score0 > score1:
            leader = 0
        elif score1 > score0:
            leader = 1
        else:
            leader = None
        if leader != None and leader != last_leader:
            print('Player', leader, 'takes the lead by', abs(score0 - score1))
        return announce_lead_changes(leader)
    return say


def both(f, g):
    """Return a commentary function that says what f says, then what g says.

    NOTE: the following game is not possible under the rules, it's just
    an example for the sake of the doctest

    >>> h0 = both(say_scores, announce_lead_changes())
    >>> h1 = h0(10, 0)
    Player 0 now has 10 and Player 1 now has 0
    Player 0 takes the lead by 10
    >>> h2 = h1(10, 8)
    Player 0 now has 10 and Player 1 now has 8
    >>> h3 = h2(10, 17)
    Player 0 now has 10 and Player 1 now has 17
    Player 1 takes the lead by 7
    """
    def say(score0, score1):
        return both(f(score0, score1), g(score0, score1))
    return say


def announce_highest(who, last_score=0, running_high=0):
    """Return a commentary function that announces when WHO's score
    increases by more than ever before in the game.

    NOTE: the following game is not possible under the rules, it's just
    an example for the sake of the doctest

    >>> f0 = announce_highest(1) # Only announce Player 1 score gains
    >>> f1 = f0(12, 0)
    >>> f2 = f1(12, 9)
    9 point(s)! The most yet for Player 1
    >>> f3 = f2(20, 9)
    >>> f4 = f3(20, 30)
    21 point(s)! The most yet for Player 1
    >>> f5 = f4(20, 47) # Player 1 gets 17 points; not enough for a new high
    >>> f6 = f5(21, 47)
    >>> f7 = f6(21, 77)
    30 point(s)! The most yet for Player 1
    """
    assert who == 0 or who == 1, 'The who argument should indicate a player.'
    # BEGIN PROBLEM 7
    "*** YOUR CODE HERE ***"
    def say(score0, score1):
        if who <1:
            score_dif = score0 - last_score
            score_last = score0
        else:
            score_dif = score1 - last_score
            score_last = score1

        score_high = running_high
        if score_dif > running_high:
            print(score_dif,'point(s)! The most yet for Player', who)
            score_high = score_dif
        return announce_highest(who, score_last, score_high)
    return say
    # END PROBLEM 7


#######################
# Phase 3: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def make_averaged(original_function, trials_count=1000):
    """Return a function that returns the average value of ORIGINAL_FUNCTION
    when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.0
    """
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    def cal_avg(*args):
        k, sum =0, 0
        while k < trials_count:
            sum += original_function(*args)
            k += 1
        return sum/trials_count
    return cal_avg
    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, trials_count=10000000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over TRIALS_COUNT times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    k, num_dice = 10, 1
    sum, score_record = 0, 0
    while k > 0:
        count, sum = 0, 0
        while count < trials_count:
            sum += roll_dice(k, dice)
            count += 1
        if  sum >= score_record:
            score_record = sum
            num_dice = k
        k -= 1
    return num_dice
    # END PROBLEM 9


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(6)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if False:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if True:  # Change to True to test extra_turn_strategy
        print('extra_turn_strategy win rate:', average_win_rate(extra_turn_strategy))

    if False:  # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"



def bacon_strategy(score, opponent_score, cutoff=8, num_rolls=6):
    """This strategy rolls 0 dice if that gives at least CUTOFF points, and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 10
    if free_bacon(opponent_score) >= cutoff:
        return 0
    else:
        return num_rolls  # Replace this statement
    # END PROBLEM 10


def extra_turn_strategy(score, opponent_score, cutoff=8, num_rolls=6):
    """This strategy rolls 0 dice when it triggers an extra turn. It also
    rolls 0 dice if it gives at least CUTOFF points and does not give an extra turn.
    Otherwise, it rolls NUM_ROLLS.
    """
    # BEGIN PROBLEM 11
    if free_bacon(opponent_score) >= cutoff or extra_turn(score + free_bacon(opponent_score), opponent_score):
        return 0
    else:
        return num_rolls  # Replace this statement
    # END PROBLEM 11

# def achieve_d(d):
#     k, num_dice = 10, 6
#     d_record = 1
#     num_run = 100000
#     if d > 54:
#         return 10
#
#     while k > 0:
#         count, sum = 0, 0
#         while count < num_run:
#             if roll_dice(k, six_sided) >= d:
#                 sum += 1
#             count += 1
#         if  sum >= d_record:
#             d_record = sum
#             num_dice = k
#         k -= 1
#     # print(d_record/num_run*100, '%')
#     return num_dice
def achieve_d(d):
    if d > 32:
        return 10
    elif d > 28:
        return 9
    elif d > 25:
        return 8
    elif d > 21:
        return 7
    elif d > 17:
        return 6
    elif d > 13:
        return 5
    elif d > 10:
        return 4
    elif d > 6:
        return 3
    else:
        return 0

def equal_d(d):
    assert d <= 60, 'd should be less than 61.'
    k, num_dice = 10, 6
    d_record = 1
    num_run = 100000
    if d > 54:
        return 10

    while k > 0:
        count, sum = 0, 0
        while count < num_run:
            if roll_dice(k, six_sided) == d:
                sum += 1
            count += 1
        if  sum >= d_record:
            d_record = sum
            num_dice = k
        k -= 1
    return num_dice, d_record/num_run*100


# shishi = 1
# while shishi <= 54:
#     print(shishi, equal_d(shishi))
#     shishi += 1


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 12
    d_score = GOAL_SCORE - score
    d_opponent = opponent_score - score
    if d_score <= free_bacon(opponent_score) or extra_turn(score + free_bacon(opponent_score), opponent_score):
        return 0
    if GOAL_SCORE - opponent_score <= 10:
        return achieve_d(d_score)
    if d_score < 10:
        return 3
    if extra_turn(score + 1, opponent_score) or d_opponent > 32:
        return 10
    # free_try = 2
    # while free_try <= 10:
    #     if extra_turn(score + free_try, opponent_score):
    #         if free_try < 7:
    #             return 1
    #         else:
    #             return 2
    #     free_try += 1

    # elif d_opponent > 0:
    #     return achieve_d(d_opponent)
    return extra_turn_strategy(score, opponent_score, 8, 6)  # Replace this statement
    # END PROBLEM 12

##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()

# debug
# always_three = make_test_dice(3)
# always = always_roll
# s0, s1 = play(always(5), always(5), goal=25, dice=always_three)
# print(s0, s1)
# i = 0
# frequency = dict()
# while i < GOAL_SCORE:
#     frequency[str(free_bacon(i))] = frequency.get(str(free_bacon(i)), 0) + 1
#     i += 1
# lst = list(frequency.keys())
# lst.sort()
# print(lst)
# for key in lst:
#     print(key, frequency[key])
# print(frequency)
# print(sorted(frequency.items(), key = lambda kv:(kv[1], kv[0])))
