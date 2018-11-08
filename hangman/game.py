from .exceptions import *
import random


class GuessAttempt(object):
    
    def __init__(self, char, hit=False, miss=False):
        if not hit and not miss:
            raise InvalidGuessAttempt
        if hit and miss:
            raise InvalidGuessAttempt
        self.hit = hit
        self.miss = miss
    
    def is_miss(self):
        return self.miss
    
    def is_hit(self):
        return self.hit
            


class GuessWord(object):
    
    def __init__(self, word):
        if len(word) == 0:
            raise InvalidWordException
        self.answer = word
        self.masked = '*' * len(word)
    
    def perform_attempt(self, char):
        if len(char) > 1 or len(char) == 0:
            raise InvalidGuessedLetterException
        result = ''
        for i,c in enumerate(self.answer.lower()):
            if char.lower() == c and self.masked[i] == '*':
                result += c
                continue
            result += self.masked[i]
        if result == self.masked:
            a = GuessAttempt(char, miss=True)
        else:
            a = GuessAttempt(char, hit=True)
        self.masked = result
        return a


class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    @classmethod
    def select_random_word(cls, list):
        if len(list) == 0:
            raise InvalidListOfWordsException
        return random.choice(list)
    
    def __init__(self, list=WORD_LIST, number_of_guesses=5):
        self.remaining_misses = number_of_guesses
        self.word = GuessWord(HangmanGame.select_random_word(list))
        self.previous_guesses = []
        self.finished = False
        self.won = False
        self.lost = False
        
    def guess(self, char):
        if self.finished:
            raise GameFinishedException
        a = self.word.perform_attempt(char)
        if a.is_miss():
            self.remaining_misses -= 1
        self.previous_guesses.append(char.lower())
        if self.remaining_misses == 0:
            self.finished = True
            self.lost = True
            raise GameLostException
        if '*' not in self.word.masked:
            self.finished = True
            self.won = True
            raise GameWonException
        return a
    
    def is_finished(self):
        return self.finished
    
    def is_won(self):
        return self.won
    
    def is_lost(self):
        return self.lost
