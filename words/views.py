from django.shortcuts import render
import string
import re
import urllib.request
import random
import json
from django.http import JsonResponse



# Create your views here.

def letters(request):
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
    return JsonResponse({'letters':letters})


def validate_word(request):
    """
    The function should check that the word is made up
    entirely of letters in the letters list. A letter cannot be used more times than
    it appears in the letters list. If the word is valid, the function should return
    True. If it is not valid, the function should return False.
    """
    
    if request.method == 'POST':
        data_json = json.loads(request.body)
        print(data_json)
        word = data_json['word']
        letters = data_json['letters']



        for letter in word: 
            #the letter must occur equal or less  number  of times in word as in letters 
            # the letter must also be present in letters  
            # no of letter in word > no letter in letters implies letter is entered more times than it is
            # in letters or it is not in letters at all         
            if re.findall(letter,word) > re.findall(letter,str(letters)): 
                return JsonResponse({'msg':False})
            
        return JsonResponse({'msg':True})


def process_word(request,word):
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

    api_key = '55plf37ddd9qvz375jbbm5ft0sklal1uptch9tjoz9762y037'
    url = 'https://api.wordnik.com/v4/word.json/' + word.strip() +\
            '/scrabbleScore?api_key=' + api_key
    try:
        resp = urllib.request.urlopen(url)

        if resp.status == 200: #success
            response = json.load(resp)      
            scrabble_score = response['value']
            

            print()
            print(word.upper() + ' Accepted. ' + str(scrabble_score) + " points awarded." )
            print()
            return JsonResponse({
                'msg':True,
                'data':{
                    'scrabble_score':scrabble_score,
                    }
            })
        elif resp.status == 404: #word not found
            print(word.upper() + 'Not Accepted.')
            return JsonResponse({'msg':False})
    except urllib.error.HTTPError as e:
        print(word.upper() + ' Not Accepted.')
        return JsonResponse({'msg':False})


