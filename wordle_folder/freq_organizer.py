import pandas as pd
import numpy as np

words = pd.read_csv('frequency.csv')
wordles = set(open('wordles.txt', 'r').read().splitlines())

# Remove the first row
words = words.iloc[1:]
words.columns = ['word', 'frequency']

# Only keep the words in the wordles list
cleaned_words = pd.DataFrame(words[words['word'].apply(lambda x: x in wordles)] )

# Get the words not in cleaned_words but in wordles list
other_words = [word for word in wordles if word not in cleaned_words['word'].values]
other_words_df = pd.DataFrame(other_words, columns=['word'])

# Concatenate and fill NaN frequencies with 0
cleaned_words = pd.concat([cleaned_words, other_words_df])
cleaned_words.fillna(0, inplace=True)
cleaned_words['frequency'] = cleaned_words['frequency'].map(lambda x: int(x))

#save the cleaned words to a new CSV file
cleaned_words.to_csv('cleaned_frequency.csv', index=False)
