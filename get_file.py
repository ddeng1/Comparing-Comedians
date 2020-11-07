# Web scraping the transcripts of 5 commedians from scrapsfromtheloft.com
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pathlib

urls = ["https://scrapsfromtheloft.com/2018/11/21/trevor-noah-son-of-patricia-transcript/",
        "https://scrapsfromtheloft.com/2019/08/26/dave-chappelle-sticks-stones-transcript/",
        "https://scrapsfromtheloft.com/2017/08/19/joe-rogan-triggered-2016-full-transcript/",
        "https://scrapsfromtheloft.com/2018/05/05/john-mulaney-kid-gorgeous-at-radio-city-full-transcript/",
        "https://scrapsfromtheloft.com/2020/05/01/maria-bamford-weakness-is-the-brand-transcript/"]


def url_transcript(url):
    """
    Scrapes webpages from scrapsfromtheloft.com containing stand up comedy transcripts
    Args:
        url: A string representing the webpage url of the transcript
    returns:
        A string representing the the required transcript text
    """
    page_content = requests.get(url)
    if page_content.status_code == 200:
        soup = BeautifulSoup(page_content.text, "html.parser")
        paragraphs = soup.find_all("div", {"class": "elementor-widget-container"})
        transcript = max(paragraphs, key=len)
        text = transcript.text
        return text
    else:
        raise Exception("Invalid input")


def check_file_exist(comedian, url):
    """
    Check whether the file exists in the form comedian_name.text given the comedian name and url
    Args:
        comedian: A string representing the name of the comedian
        url: A string representing the webpage url of the transcript
    Returns: A string representing the the required transcript text
    """
    path = pathlib.Path(f"transcripts/{comedian}.txt")
    if path.exists():
        with open("transcripts/" + comedian + ".txt", "r") as infile:
            return infile.readlines()
    else:
        transcript_text = url_transcript(url)
        # create a folder for each comedian and write transcripts
        with open("transcripts/" + comedian + ".txt", "w") as outfile:
            outfile.write(transcript_text)
        return transcript_text


comedian_names = ["Trevor", "Dave", "Joe", "John", "Maria"]

transcript_dict = {}
for comedian, url in zip(comedian_names, urls):
    transcript_dict[comedian] = check_file_exist(comedian, url)