#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 10:37:34 2023

@author: tomvija
"""

from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
import time
import random
from collections import Counter




#inputs the value passed into the function.
def convert_keys(word, driver):
    for char in word:
        time.sleep(.1)
        driver.find_element(By.CSS_SELECTOR, f'button[data-key="{char}"]').click()
    driver.find_element(By.CSS_SELECTOR, 'button[aria-label="enter"]').click()


def update_keys(driver, guess_num):
    hint = [' '] * 5
    # Find all rows
    rows = driver.find_elements(By.CLASS_NAME, 'Row-module_row__pwpBq')
    row = rows[guess_num]
    # Find all tiles in the row
    tiles = row.find_elements(By.CSS_SELECTOR, 'div[data-testid="tile"]')

    #fill in the hint list
    for i in range(5):
        aria_state = tiles[i].get_attribute('data-state')
        if aria_state == 'correct':
            hint[i] = 'g'
        elif aria_state == 'present':
            hint[i] = 'y'
        elif aria_state == 'absent':
            hint[i] = 'r'
    return hint




def filter_words(words, hint, previousWord):

    #filter out the words only from the words list
    newList = set([word for (word, count) in words if word != previousWord])
    letter_counts = Counter()

    # Determine actual counts of hinted letters in the previous word
    for i in range(5):
        if hint[i] in ('g', 'y'):
            letter_counts[previousWord[i]] += 1

    for i in range(5):
        ch = previousWord[i]
        h = hint[i]

        if h == 'g':
            newList = [word for word in newList if word[i] == ch]

        elif h == 'y':
            newList = [word for word in newList if ch in word and word[i] != ch]

        elif h == 'r':
            #if there are no more occurences of the letter in the previous word, remove all words with that letter
            if letter_counts[ch] == 0:
                newList = [word for word in newList if ch not in word]
            else:
                #if there are more occurences of the letter in the previous word, remove all words with the letter in the same position
                newList = [word for word in newList if word[i] != ch]

    #convert the newList to a list of tuples
    words = update_frequency(newList, words)

    return words


def update_frequency(words, freq):
    freq = [(word, count) for (word, count) in freq if word in words]
    return freq

def next_word(words):
    if not words:
        raise ValueError("No words left to choose from.")
    else:
        return words[0][0]

#returns a boolean for if the word is right or not.
def correct_word(hint):
    return ''.join(hint) == "ggggg"


def main():
    
    options = ChromeOptions()
    
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    options.add_argument("--log-level=3") # 0 (all), 1 (info), 2 (warnings), 3 (errors)

    driver = webdriver.Chrome(service=Service(), options=options)
    hint = []
    #open text file with every 5 letter word

    with open('cleaned_frequency.csv', 'r') as w:
        words = w.read().splitlines()
        words = [tuple(line.split(',')) for line in words]


    #get the URL and print the status code
    url = 'https://www.nytimes.com/games/wordle/index.html'
    response = requests.get(url)
    if(response.status_code == 200):
        print('The website has a response code of 200, we are all good.')
    else:
        print(f"Error: The website has a response code of {response.status_code}, halting the program.")
        exit()
    

    #hit the play button
    driver.get(url)
    time.sleep(1)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="Play"]'))).click()

    try:    
        #close the pop up for the rules
        time.sleep(2)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label = "Close"]'))).click()
    except:
        pass
    guess_num = 0
    #type in the first word
    newWord = "salet"
    print(f'The first word will be {newWord}.')
    convert_keys(newWord, driver)
    previousWord = newWord

    while (not correct_word(hint)):
        time.sleep(2)

        hint = update_keys(driver, guess_num)
        guess_num += 1
        if correct_word(hint):
            break
        words = filter_words(words, hint, previousWord)
        newWord = next_word(words)
        print(f'The next word will be {newWord}.')
        convert_keys(newWord, driver)
        previousWord = newWord
    print('The word has been found, Closing in 10 seconds...')
    time.sleep(10)
    driver.close()
    
if __name__ == "__main__":
    main()