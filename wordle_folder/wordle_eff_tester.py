import Wordle_doer as wd
import random as r
import matplotlib.pyplot as plt



def make_hint(guess, correct_word):
    hint = ['r', 'r', 'r', 'r', 'r']
    temp_correct_word = list(correct_word)

    # Mark greens first
    for i in range(5):
        if guess[i] == correct_word[i]:
            hint[i] = 'g'
            temp_correct_word[i] = None # Consume this letter
    # Mark yellows
    for i in range(5):
        if hint[i] == 'g': # Already processed
            continue
        if guess[i] in temp_correct_word:
            hint[i] = 'y'
            # Consume the first occurrence of this yellow letter, this is done to avoid bugs when duplocates exist
            temp_correct_word[temp_correct_word.index(guess[i])] = None 
    return hint



def eff_tester(num_iter, init_guess):

    #open file
    with open('cleaned_frequency.csv', 'r') as w:
        words = w.read().splitlines()
        words = [tuple(line.split(',')) for line in words]

    #create the variables to hold the statistics
    avg_guesses = 0
    max_guesses = 0
    min_guesses = 100
    failures = 0
    guess_dist = [0] * 7
    filtered_words = [word for (word, freq) in words if freq != '0']
    for i in range(num_iter):
        if i % 10 == 0:
            print(f'Iteration {i} of {num_iter}')
        
        word_list = words.copy()
        correct_word = r.choice(filtered_words)
        
        current_game_guess = init_guess
        guesses = 0

        while True:
            guesses = guesses + 1
            hint = make_hint(current_game_guess, correct_word)

            if wd.correct_word(hint):
                break
            
            if guesses >= 6:
                failures += 1
                print(f'Failed to solve word {correct_word} in 6 guesses')
                break

            word_list = wd.filter_words(word_list, hint, current_game_guess)
            try:
                current_game_guess = wd.next_word(word_list)
            except ValueError:
                failures += 1
                break 
        
        if wd.correct_word(hint):
            guess_dist[guesses] += 1
            avg_guesses += guesses
            if guesses > max_guesses:
                max_guesses = guesses
            if guesses < min_guesses:
                min_guesses = guesses

    successful_solves = num_iter - failures
    avg_guesses_for_success = avg_guesses / successful_solves
   

    print(f'Average guesses: {avg_guesses_for_success}',
          f'Max guesses: {max_guesses}',
          f'Min guesses: {min_guesses}',
          f'Failures: {failures}')
    
    plt.bar(range(1, 7), guess_dist[1:], color='blue', alpha=0.7)
    plt.title(f'Wordle Efficiency Test with {num_iter} iterations, initial guess: {init_guess}')
    plt.xlabel('Number of Guesses')
    plt.ylabel('Number of Games')
    plt.xticks(range(1, 7))
    plt.show()

    
eff_tester(1000, 'salet')

