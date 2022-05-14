"""Typing test implementation"""

from cmath import sin
from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.

    ps = ['short', 'really long', 'tiny']
    s = lambda p: len(p) <= 5
    choose(ps, s, 0) # 'short'
    """
    # BEGIN PROBLEM 1
    p = [i for i in paragraphs if select(i)]
    if k>len(p)-1:
        return ''
    else:
        return p[k]
    
    # END PROBLEM 1

import utils
def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    def s(_p):
        _p = remove_punctuation(_p).lower().split(' ')
        if len([i for i in topic if i in _p])==0:
            return False
        else:
            return True
    return s
    # END PROBLEM 2
    # dogs = about(['dogs', 'hounds'])
    # dogs('A paragraph about cats.')


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    if len(typed_words) ==0 or len(reference_words) ==0:
        return 0.0
    elif len(typed_words) <= len(reference_words) :
        correct = len([i for _,i in enumerate(typed_words) if i == reference_words[_]])
    elif len(typed_words) > len(reference_words):
        correct = len([i for _,i in enumerate(reference_words) if i == typed_words[_]])
    return correct/len(typed_words) * 100
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    return len(typed)/5*(60/elapsed)
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    if isinstance(valid_words,str):
        if diff_function(user_word,valid_words,limit) > limit:
            return user_word
        else:
            return valid_words
    
    elif isinstance(valid_words,list):
        if user_word in valid_words:
            return user_word
        else:
            d_list = []
            for i in valid_words:
                d_list.append(diff_function(user_word,i,limit))
            if min(d_list) > limit:
                return user_word
            else:
                _ = min([_ for _,i in enumerate(d_list) if i == min(d_list)])
                return valid_words[_]
    # END PROBLEM 5


def shifty_shifts(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    if goal =='' or start =='':
        return 0
    if limit == -1:
        return 0

    else:
        l = min(len(start),len(goal))
        # change = shifty_shifts(start[1:l], goal[1:l],limit) + abs(len(goal)-len(start),limit)
        if start[0] != goal[0]:
            return 1 + shifty_shifts(start[1:l], goal[1:l],limit-1) + abs(len(goal)-len(start))
        else:
            return shifty_shifts(start[1:l], goal[1:l],limit) + abs(len(goal)-len(start))
            
        
#     # cats --> scat
#     # match - plus 0
#     # skip/non-match - plus 1
#     #   * c a t s
#     # * 0 0 0 0 0
#     # s 1 1 1 1 0
#     # c 2 1 2 2 1 
#     # a 3 2 1 2 2
#     # t 4 3 2 1 2

#     # *cats
#     # scat*

def editDistance_approxi(x, y, returnD=False):
    # Create distance matrix
    D = []
    for i in range(len(x)+1):
        D.append([0]*(len(y)+1))
    # Initialize first row and column of matrix
    for i in range(len(x)+1):
        D[i][0] = i  # first col
    for i in range(len(y)+1):
        D[0][i] = i  # first row
    # Fill in the rest of the matrix
    for i in range(1, len(x)+1):
        for j in range(1, len(y)+1):
            distHor = D[i][j-1] + 1  # skip from horizonal plus 1 (skip from p or x)
            distVer = D[i-1][j] + 1  # skip from vertical plus 1 (skip from t or y)
            if x[i-1] == y[j-1]:
                distDiag = D[i-1][j-1]   # match then plus 0
            else:
                distDiag = D[i-1][j-1] + 1
            D[i][j] = min(distHor, distVer, distDiag)  # not match then plus 1
    # Edit distance is the value in the bottom right corner of the matrix
    if returnD:
        return D, min(D[-1])
    else:
        return min(D[-1])

    
def pawssible_patches(start, goal, limit):
    # a recursion version of editDistance_approxi
    # https://bdebo.medium.com/edit-distance-643a4bcfaa09

    if len(start) ==0 or len(goal) ==0:
        return len(start) + len(goal)
    
    if limit == -1:
        return 0
    
    if start[0] == goal[0]:
        return pawssible_patches(start[1:],goal[1:],limit)

    else:
        # place     add: rplace     remove: lace       replace: rlace
        # rest8          rest8              rest8               rest8
        add1 = pawssible_patches(start,goal[1:],limit-1)
        rm1 =  pawssible_patches(start[1:],goal,limit-1)
        rp1 =  pawssible_patches(start[1:],goal[1:],limit-1)
        return 1+ min(add1,rm1,rp1)
    


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'

# small_words_list = ["spell", "nest", "test", "pest", "best", "bird", "wired",
#                   "abstraction", "abstract", "wire", "peeling", "gestate",
#                   "west", "spelling", "bastion"]

###########
# Phase 3 #
###########


def report_progress(typed, prompt, user_id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    if len(typed) ==0:
        progress = 0.0
    else:
        if typed == prompt[0:len(typed)]:
            progress = (len(typed))/len(prompt)
        else:
            i = min([ind for ind in range(len(typed)) if typed[ind] != prompt[ind]])
            progress = (i)/len(prompt)
                
    send({'id':user_id, 'progress':progress})
    return progress
    # END PROBLEM 8


def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.
    """
    # BEGIN PROBLEM 9
    # times_per_player = [[1, 3, 5], [2, 5, 6]]
    times = []
    for player in times_per_player:
        # [1,3,5] --> [3-1,5-3]
        time = []
        for i in range(len(player)-1):
            time.append(player[i+1]-player[i])
        times.append(time)
    return game(words,times)
    # END PROBLEM 9


def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.
    Returns:
        a list of lists containing which words each player typed fastest
    """
    # w  ['a','b','c']
    # t  [[1,1,2],[2,1,3]]
    # p0 [1,1,2]
    # p1 [2,1,3]
    # return [['a','b','c'],[]]
    player_indices = range(len(all_times(game)))  # contains an *index* for each player
    word_indices = range(len(all_words(game)))    # contains an *index* for each word
    # BEGIN PROBLEM 10
    words,times = all_words(game),all_times(game)
    # There's no necessary to use this 
    # why does it have to be wrapped in an object

    out_list = [[] for i in player_indices]
    for w_ind in word_indices:
        mm = min([times[i][w_ind] for i in player_indices])
        p = min([i for i in player_indices if times[i][w_ind] == mm])
        out_list[p].append(words[w_ind])
    return out_list
    # END PROBLEM 10


def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])

enable_multiplayer = False  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)