from sklearn.feature_extraction.text import CountVectorizer
from cleaning import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from textblob import TextBlob

vectorizer = CountVectorizer(stop_words='english')
# fit count vectorizor to the clean transcipt data
data_vector = vectorizer.fit_transform(data_clean.Transcripts)

# Convert it to an array and label all the columns
data_tokenized = pd.DataFrame(data_vector.toarray(),
                              columns=vectorizer.get_feature_names())
data_tokenized.index = data_clean.index

data_df = data_tokenized.transpose()

# Number of unique Words used by each Comedian

unique_list = []
for comedian in data_df.columns:
    uniques = data_df[comedian].to_numpy().nonzero()[0].size
    unique_list.append(uniques)

# Create a new dataframe that contains this unique word count
data_words = pd.DataFrame(list(zip(full_names, unique_list)),
                          columns=['comedian', 'unique_words'])
data_words_sort = data_words.sort_values(by='unique_words')


def analyze_unique_words():
    # Calculate the words per minute of each comedian
    # Find the total number of words that a comedian uses
    total_word_list = []
    for comedian in data_df.columns:
        totals = sum(data_df[comedian])
        total_word_list.append(totals)

    # Comedy special run times from IMDB (in minutes)
    run_times = [63, 65, 63, 65, 74]

    # add additional columns to the dataframe
    data_words['total_words'] = total_word_list
    data_words['run_times(min)'] = run_times
    data_words['words_per_minute'] = data_words['total_words'] / data_words['run_times(min)']

    # Sort the dataframe by words per minute to see who talks the slowest and fastest
    data_wpm_sort = data_words.sort_values(by='words_per_minute')
    # Returns evenly spaced values within a given interval. Stop at len(data_words)
    y_pos = np.arange(len(data_words))
    plt.subplot(1, 2, 1)  # plt.subplot (nrows, ncols, index)
    plt.barh(y_pos, data_words_sort.unique_words, align='center')
    plt.yticks(y_pos, data_words_sort.comedian)
    plt.title('No. of Unique Words', fontsize=15)

    plt.subplot(1, 2, 2)
    plt.barh(y_pos, data_wpm_sort.words_per_minute, align='center', color='green')
    plt.yticks(y_pos, data_wpm_sort.comedian)
    plt.title('No. of Words Per Minute', fontsize=15)

    plt.tight_layout()
    plt.savefig('comparing_words')
    return data_wpm_sort


def analyze_sentiments():
    # Performing a sentiment analysis of their comedy transcripts
    polar = lambda x: TextBlob(x).sentiment.polarity
    subj = lambda x: TextBlob(x).sentiment.subjectivity

    # Apply a function along an axis of the DataFrame.
    data_clean['polarity'] = data_clean['Transcripts'].apply(polar)
    data_clean['subjectivity'] = data_clean['Transcripts'].apply(subj)
    data_final = data_clean

    plt.rcParams['figure.figsize'] = [10, 8]  # Set width to 10 inches and height to 8 inches

    for index, comedian in enumerate(data.index):
        x = data_clean.polarity.loc[comedian]
        y = data_clean.subjectivity.loc[comedian]
        plt.scatter(x, y, color='red')
        # set measurements so that dot and label do not overlap
        plt.text(x + .001, y + .001, data_clean['full_name'][index], fontsize=12)
        plt.xlim(-.015, .15)

    plt.title('Sentiment Analysis', fontsize=20)
    plt.xlabel('<-- Negative . . . . . . . . . . . . . . . Positive -->', fontsize=15)
    plt.ylabel('<-- Facts . . . . . . . . . . . . . . . Opinions -->', fontsize=15)

    plt.savefig('sentiment_analysis')
