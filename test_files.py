import pytest
import get_file
from cleaning import combine_text, clean_text
import analysis


combine_cases = [(["This is my code", "John is great"],
                  "This is my code John is great"),
                 (["This is one", "This is two", "This is three"],
                  "This is one This is two This is three"),
                 (["Dave is funny"], "Dave is funny"),
                 ([" ", " "])]  # Check empty list returns empty string

# Check that it changes text into lower case
clean_cases = [("CHANGE ALL TO LOWERCASE", "change all to lowercase"),
               # Check that punctuations are omitted
               ("This is one sentence. Is this another?",
                "this is one sentence is this another"),
               # Check that text in brackets are omitted
               ("[Everyone, put your hands together.]Thank you for having me tonight",
                "thank you for having me tonight"),
               # Check that newline \n symbols is removed
               ("\nBeginning of new line. Some n8ght words have no meaning.",
                "beginning of new line some  words have no meaning")]


@pytest.mark.parametrize("list_of_text, combined_text", combine_cases)
def test_combine_text(list_of_text, combined_text):
   assert combine_text(list_of_text) == combined_text


@pytest.mark.parametrize("text, new_text", clean_cases)
def test_clean_text(text, new_text):
   assert clean_text(text) == new_text