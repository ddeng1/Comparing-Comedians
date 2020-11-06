
import re
import string
import pandas as pd
from get_file import *

# Change the values from being list to a string of text
def combine_text(list_of_text):
    """
    Combines a list of text into one large chunk of text
    Args: 
        list_of_text: A list of strings (text) 
    Returns: A string of texts
    """
    combined_text = ' '.join(list_of_text)
    return combined_text

 #Combine evertyhing in a dictionary
data_combined = dict()  # empty dictionary
for key, value in transcript_dict.items():
    data_combined[key] = combine_text(value) 
    
pd.set_option('max_colwidth',100)
data = pd.DataFrame.from_dict(data_combined, orient='index', columns=["Transcripts"])
# print(data)


def clean_text(text):
    """Given text, make it lowercase, remove text in square brackets, remove punctuation and remove words containing numbers.
    """
    new_text = text.lower()
    new_text = re.sub('\[.*?\]', '', new_text)
    new_text = re.sub('[%s]' % re.escape(string.punctuation), '', new_text)
    new_text = re.sub('\w*\d\w*', '', new_text)
    new_text = re.sub('[‘’“”…]', '', new_text) #Remove additional quotation marks in some transcript
    new_text = re.sub('\n', '', new_text) #remove newline text, \n
    return new_text
    
round1 = lambda x: clean_text(x)

data_clean = pd.DataFrame(data.Transcripts.apply(round1))
# print(data_clean)

# Add comedians full names
full_names = ["Trevor Noah", "Dave Chappelle", "Joe Rogan", "John Mulaney", "Maria Bamford"]


data_clean['full_name'] = full_names
data_clean
# print(data_clean)





