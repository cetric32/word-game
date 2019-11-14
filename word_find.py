"""
CLI program that allows the user to play a word game.
If the user scores high enough in the game, some data about the game in
a text file.
"""

import random
import json
import re
import urllib.request
import string


# store the user’s score.
score = 0
# store the words that the user has entered.
used_words = []

def select_letters():
    """ 
    The function randomly selects 9 letters and returns them 
    as a list of 9 strings. The same letter can appear multiple times,
    and the selection process uses the frequency of letters in Scrabble
    when choosing letters.
    """
    # store the letters selected for this game.
    letters = []
    # This tuple contains 26 numbers, representing the frequency of each letter of the alphabet in Scrabble.
    letter_weights = (9, 2, 2, 4, 12, 2, 3, 2, 9, 1, 1, 4, 2, 6, 8, 2, 1, 6, 4, 6, 4, 2, 2, 1, 2, 1)
    # The letter_weights tuple is used in this call to the "random.choices()" function, along with
    # the pre-defined "string.ascii_uppercase" variable which contains the letters A to Z.
    letters = random.choices(string.ascii_uppercase, weights=letter_weights, k=9)
    return letters



def display_letters(letters):
    """
    function should
    print the letters in a 3x3 grid
    """
    print()
    print('          ',letters[0],'|',letters[1],'|',letters[2])
    print('          ----------------')
    print('          ',letters[3],'|',letters[4],'|',letters[5])
    print('          ----------------')
    print('          ',letters[6],'|',letters[7],'|',letters[8])
    print()

def validate_word(word,letters):
    """
    The function should check that the word is made up
    entirely of letters in the letters list. A letter cannot be used more times than
    it appears in the letters list. If the word is valid, the function should return
    True. If it is not valid, the function should return False.
    """
    
    for letter in word: 
        #the letter must occur equal or less  number  of times in word as in letters 
        # the letter must also be present in letters  
        # no of letter in word > no letter in letters implies letter is entered more times than it is
        # in letters or it is not in letters at all         
        if re.findall(letter,word) > re.findall(letter,str(letters)):   
            return False
    return True

def select_mode():
    """
    In easy mode, entering an invalid word does not end
    the game. In hard mode, an invalid word ends the game.
    """
    
    #the mode of the game
    hard_mode = False

    
    while True:
        mode = str(input('Do you wish to play [e]asy mode or [h]ard mode? ')).strip()
        if mode.lower() == 'h':
                hard_mode = True  # play in hard mode
                print('Hard Mode selected.Entering an Invalid word will end the game.\n')
                return hard_mode
        elif mode.lower() == 'e':
                print('Easy mode Selected.\n')
                return hard_mode
        else: # case of invalid input
            print('Invalid input,please select a mode\n')

def process_word(word):
    """
    check if the user’s input is a recognised English word and
    obtain its Scrabble score. This will be done by sending a request to an
    online service named “Wordnik”. If the word is recognised, print a “word
    accepted” message that tells the user how many points it is worth, and
    add the points to their score, and append the word to the used_words
    list.
    If the word is not recognised, print an appropriate message. If
    hard_mode is True, print “Game over!” and end the loop to end the
    game.
    """
    global score
    global used_words

    api_key = '55plf37ddd9qvz375jbbm5ft0sklal1uptch9tjoz9762y037'
    url = 'https://api.wordnik.com/v4/word.json/' + word.strip() +\
            '/scrabbleScore?api_key=' + api_key
    try:
        resp = urllib.request.urlopen(url)

        if resp.status == 200: #success
            response = json.load(resp)      
            scrabble_score = response['value']
            #appending to the lists
            score += int(scrabble_score) 
            used_words.append(word.upper())

            print()
            print(word.upper() + ' Accepted. ' + str(scrabble_score) + " points awarded. Your score is now " +str( score) )
            print()
            return True
        elif resp.status == 404: #word not found
            print(word.upper() + 'Not Accepted.')
            return False
    except urllib.error.HTTPError as e:
        print(word.upper() + ' Not Accepted.')
        return False

def log_game(letters):
    """
    logs the game data. 
    This will involve first opening a text file in read mode to read existing log data,
    appending a log of the game to the data, and then writing the entire data to
    the file.
    """
    global used_words
    global score
    letters = letters

    log_list = []
    log_dict = {}

    #storing the data to the dictionary
    log_dict['letters'] = letters
    log_dict['words'] = used_words
    log_dict['score'] = score

    #opening the file for reading and writing
    try:
        fh = open('logs.txt')
        #if file exists continue
        new_log_list = json.load(fh)
        new_log_list.append(log_dict)
        fh.close()
        fh = open('logs.txt','w')
        json.dump(new_log_list,fh)
        fh.close()

    except FileNotFoundError:
        #open the file in write mode and add data
        fh = open('logs.txt','w')
        log_list.append(log_dict)
        json.dump(log_list,fh)
        fh.close()
    except Exception as e:
        print(e)



def end_game(letters):
    """
    ends the game (by choice or due to an invalid word in hard mode).
    print their final score. If their score is 50 or more, congratulate them and record a
    log of the game.This will involve first opening a text file in read mode to read existing log data,
    appending a log of the game to the data, and then writing the entire data to
    the file.
    """
    letters = letters
    print('Your final score was ',score)
    if score >= 50:
        print('Congradulations! You have played well.')
        #logging the game data
        log_game(letters)
    print('Thank you for playing!')
    exit(0)

def main():
    """
    The main program function
    """
    global used_words
    global score

    print('Welcome to Word Find Game')
    #select letters
    hard_mode = select_mode()
    letters = select_letters()

    while True:
        print('Score: ',score," Your letters are: ")
        display_letters(letters)
        print()
        choice = input("Enter a word, [s]huffle letters, [l]ist words, or [e]nd game): ").upper()
        
        if choice == 'S': # shuffle the letters
            random.shuffle(letters)
        elif choice == 'E':
            print('Ending game...')
            break
        elif choice == 'L':
            if len(used_words) == 0:
                print('You have not entered any words yet!\n')
            else:
                used_words.sort()
                print('Previously entered words:')
                for word in used_words:
                    print('- ',word)
                print()
        else: # a word entered
            if len(choice) < 3: #input is less than 3 characters long
                print('word should not be less than 3 characters long!')
                if hard_mode:
                    print('Game over')
                    break
                else:
                    continue
            if choice in used_words: #input is in the used_words list
                print('You have aready used the word before!')
                if hard_mode:
                    print('Game over')
                    break
                else:
                    continue
            if not validate_word(choice,letters):  #user’s input is not valid
                print('Invalid character(s) used!')
                if hard_mode:
                    print('Game over')
                    break
                else:
                    continue


            #no errors in the word
            if process_word(choice.lower()):
                    pass
            else:
                    if hard_mode:
                        print('Game over')
                        break

    
    #end the game
    end_game(letters)     
        

if __name__ == '__main__':
    main()