import time
import requests
import pandas as pd
from typing import Any, cast, Dict, Optional, Tuple, Union
from bs4 import BeautifulSoup
from joblib import Memory
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import InvalidArgumentException
from selenium.common.exceptions import StaleElementReferenceException
from tqdm import tqdm

memory = Memory("cache/", verbose=0)

UFC_START = 'https://www.ufc.com'
TOTAL_UFC_EVENTS = 113 # I think this could be good--it'll phase out the shitty, old UFC events over time?

# Function to get information from a specific even
def get_event_info(url: str) -> dict[str, Any]:
    data = {}
    # Send a GET request to the URL
    response = requests.get(url)
    # Get the HTML content from the response
    html_content = response.text
    # Specify the use of lxml parser
    soup = BeautifulSoup(html_content, "lxml")

    # Get info from helpers
    data["Red Corner"], data["Blue Corner"] = get_fighters(soup)
    data["Red Corner W\L"], data["Blue Corner W\L"] = get_win_loss(soup)
    data["Weight Class"] = get_fight_weight_class(soup)
    data["Red Nation"], data["Blue Nation"] = get_fighter_nations(soup)
    data["Win Method"] = win_method(soup)
    data["Red Corner Odds"], data["Blue Corner Odds"] = get_fight_odds(soup)
    
    return data

# Function to get fighters from a specific event
# What's the difference between the red corner and blue corner in the ufc?
def get_fighters(soup):
    elements = soup.find_all(
        class_="c-listing-ticker-fightcard__red_corner_name")
    red_corner_fighter_names = [element.text for element in elements]

    elements = soup.find_all(
        class_="c-listing-ticker-fightcard__blue_corner_name")
    blue_corner_fighter_names = [element.text for element in elements]
    
    return red_corner_fighter_names, blue_corner_fighter_names

# This function can definitely be cut in half
# This function is also working in the OPPOSITE WAY that I'd like it to be
#   it's considering a loss to be a win and vice versa...
def get_win_loss(soup):
    red_corner_win_loss = list()
    elements = soup.find_all(class_="c-listing-fight__corner-body--red")
    for element in elements:
        subclass_element = element.find(
            class_="c-listing-fight__outcome-wrapper")
        if subclass_element:
            if subclass_element.find(class_="c-listing-fight__outcome--Win"):
                red_corner_win_loss.append("Win")
            # Elif added so that if Win is changed to lowercase or something, we'll see empty
            # entries instead of false "Loss" entries
            elif subclass_element.find(class_="c-listing-fight__outcome--Loss"):
                red_corner_win_loss.append("Loss")
        else:
            print("Subclass element not found.")
    
    blue_corner_win_loss = list()
    elements = soup.find_all(class_="c-listing-fight__corner-body--blue")
    for element in elements:
        subclass_element = element.find(
            class_="c-listing-fight__outcome-wrapper")
        if subclass_element:
            if subclass_element.find(class_="c-listing-fight__outcome--Win"):
                blue_corner_win_loss.append("Win")
            elif subclass_element.find(class_="c-listing-fight__outcome--Loss"):
                blue_corner_win_loss.append("Loss")
        else:
            print("Subclass element not found.")
    return blue_corner_win_loss, red_corner_win_loss

def get_fight_weight_class(soup):
    elements = soup.find_all(class_="c-listing-fight__class-text")
    weight_classes = [element.text for element in elements]
    return weight_classes[::2][::-1] # Remove every 2nd entry (duplicates)

def get_fighter_nations(soup):
    # Elements are ordered in red corner, then blue corner
    elements = soup.find_all(class_="c-listing-fight__country-text")
    all_nations = [element.text for element in elements]
    blue_nations = all_nations[::2]
    red_nations = all_nations[1::2]
    return red_nations, blue_nations

# Decision (split, unanimous), Submission (round), TKO/KO (round)
def win_method(soup):
    elements = soup.find_all(class_="c-listing-fight__result-text method")
    win_method = []
    for element in elements:
        win_method.append(element.text)
    rounds = soup.find_all(class_="c-listing-fight__result-text round")
    times = soup.find_all(class_="c-listing-fight__result-text time")
    for i, (win, round, time) in enumerate(zip(win_method, rounds, times)):
        if not win.startswith('D'):
            win_method[i] = win + ": Round " + round.text + " Time: " + time.text
    return win_method[::2][::-1]

def get_fight_odds(soup):
    all_odds = list()
    elements = soup.find_all(class_="c-listing-fight__odds-amount")
    for element in elements:
        all_odds.append(element.text)
    blue_odds = all_odds[::2][::-1]
    red_odds = all_odds[1::2][::-1]
    return blue_odds, red_odds

###############################
## TODO: 
#       These 3 functions, but then, using selenium driver, need to go in and get
#       the current stats of each of the fighters.
#


# Some outliers where you have a title fight with an unranked opponent, also
#   lots of missing data on the website for this statistic.
# def get_fighters_ranks():
#     elements = soup.find_all(class_="js-listing-fight__corner-rank c-listing-fight__corner-rank")
#     time.sleep(0.5)  # Appease the website
#     # weight_classes = [element.text for element in elements]
#     print(elements)


# ## Pickle snippet
# import pickle
# import os
# file_to_store_results = "cache/embeddings.pcl"
# if os.path.exists(file_to_store_results):
#     with open(file_to_store_results, "rb") as f:
#         encodings = pickle.load(f)
# else:
#     # Embed the titles
#     box_office_encoded = model.encode(
#         (box_office["Release"] + " - Official Trailer").str.lower()
#     )
#     # Pickle--to save to disk
#     videos_encoded = model.encode(video_data["title"].str.lower())
#     encodings = (box_office_encoded, videos_encoded)  # Some big calculations
#     with open(file_to_store_results, "wb") as f:
#         pickle.dump(encodings, f)

#################################################
## DEPRECATED AND SEEMINGLY UNUSEFUL FUNCTIONS ##
#################################################
# Finding the class of the element (helper function)
def _find_html_classes_of_data(soup, input: str):
    input_found = soup.find_all(string=input)
    if input_found is None:
        print("Input not found")
        return None
    input_classes = [input.parent.get("class") for input in input_found]
    # Make it so that this is an option
    input_parents = [input.parent for input in input_found]
    print(input_parents)
    # It ("get()") returns a list, but there's only 1 element in it (usually)
    return input_classes


# Need to address the complexity of this function--It's pretty crazy honestly
# This function basically just creates 
@memory.cache  # Cache not tested, but if shit is cached this should run very quick.
def get_event_data(future=False) -> pd.DataFrame:
    # Loop through years
    time.sleep(0.5)
    # Open the webpage; this line might cause issues if webdriver isn't set up, not sure how well
    # it'll transfer over GitHub, might be an accessibility issue for others trying to run this module.

    options = Options()
    options.headless = False  # Set to False if you want to see the browser in action
    driver = webdriver.Firefox(options=options)
    driver.get("https://www.ufc.com/events")

    if future == False:
        # element = soup.find('a', href='#events-list-past')
        element = driver.find_element('css selector', 'a[href="#events-list-past"]')
        element.click()

    def _find_and_click_next(index: int = 0, length: int = 3):
        target_elements = driver.find_elements('xpath', '//a[contains(@class, "button")]'
                                                    '[contains(@title, "Load more items")]'
                                                    '[contains(text(), "Load More")]')
        time.sleep(length) # Let webpage load
        driver.execute_script("arguments[0].style.visibility = 'visible';", target_elements[index])
        driver.execute_script("arguments[0].click();", target_elements[index])

    target_elements = driver.find_elements('xpath', '//a[contains(@class, "button")]'
                                                  '[contains(@title, "Load more items")]'
                                                  '[contains(text(), "Load More")]')
    
    # try: This try, except seems unuseful, it should only be run once a week to get an updated piece of content?
    #     # Open the HTML file and read its content
    #     with open('data/page_state.html', 'r', encoding='utf-8') as file:
    #         html_content = file.read()
    #     # Create a BeautifulSoup object from the HTML content
    #     soup = BeautifulSoup(html_content, 'html.parser')
    # except:
    i = 0
    while target_elements is not None and (i < TOTAL_UFC_EVENTS):
        try: 
            _find_and_click_next()
        except StaleElementReferenceException:
            try:
                _find_and_click_next(length=4) # Give it more time now.
            except StaleElementReferenceException:
                if len(target_elements) > 1:
                    # print(target_elements[1].is_enabled(), "#2 Is clickable")
                    try:
                        _find_and_click_next(index=1)
                    except StaleElementReferenceException:
                        print("Something has gone terribly wrong")
                        exit()
        i += 1
    # Save the current state of the page to a file
    with open('data/page_state.html', 'w', encoding='utf-8') as file:
        file.write(driver.page_source)
    # Now that all of the fights have been loaded on to 1 page, create soup object
    soup = BeautifulSoup(driver.page_source, "lxml")

    elements = soup.find_all(class_="c-card-event--result__headline")
    event_titles = [element.text for element in elements]
    links = pd.DataFrame(columns=["EventTitle", "URL"])
    links["EventTitle"] = event_titles

    for i, element in tqdm(enumerate(elements), total=len(elements)):
        link = element.find('a')['href']  # Get the href attribute value of the link
        full_link = UFC_START + link
        links["URL"][i] = full_link
    links.to_csv("data/links_to_events.csv", index=False)
    driver.quit()  # Couldn't find a way to do it without quitting the driver each time