import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_event_info(event_num):
    data = pd.DataFrame
    # Specify the URL of the webpage you want to fetch
    url = f"https://www.ufc.com/event/ufc-{event_num}"
    # Send a GET request to the URL
    response = requests.get(url)
    # Get the HTML content from the response
    html_content = response.text
    # Specify the use of lxml parser
    soup = BeautifulSoup(html_content, "lxml")

# What's the difference between the red corner and blue corner in the ufc
def get_fighters(soup):
    elements = soup.find_all(
        class_="c-listing-ticker-fightcard__red_corner_name")
    red_corner_fighter_names = [element.text for element in elements]
    print(red_corner_fighter_names)
    time.sleep(0.5)  # Appease the website

    elements = soup.find_all(
        class_="c-listing-ticker-fightcard__blue_corner_name")
    blue_corner_fighter_names = [element.text for element in elements]
    print(blue_corner_fighter_names)
    time.sleep(0.5)  # Appease the website
    return red_corner_fighter_names, blue_corner_fighter_names

# This function can definitely be cut in half
def get_win_loss(soup):
    red_corner_win_loss = list()
    elements = soup.find_all(class_="c-listing-fight__corner-body--red")
    time.sleep(0.5)  # Appease the website
    for element in elements:
        subclass_element = element.find(
            class_="c-listing-fight__outcome-wrapper")
        if subclass_element:
            # Process the subclass element
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
    time.sleep(0.5)  # Appease the website
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
    print(
        "Red Corner W\\L",
        red_corner_win_loss,
        "\n\n\n\n",
        "Blue Corner W\\L",
        blue_corner_win_loss,
    )

def get_fight_weight_class(soup):
    elements = soup.find_all(class_="c-listing-fight__class-text")
    time.sleep(0.5)  # Appease the website
    weight_classes = [element.text for element in elements]
    print(weight_classes)

# Some outliers where you have a title fight with an unranked opponent, also
#   lots of missing data on the website for this statistic.
# def get_fighters_ranks():
#     elements = soup.find_all(class_="js-listing-fight__corner-rank c-listing-fight__corner-rank")
#     time.sleep(0.5)  # Appease the website
#     # weight_classes = [element.text for element in elements]
#     print(elements)

# def get_fight_odds():
#     red_corner_odds, blue_corner_odds = list()
#     elements = soup.find_all(class_="c-listing-fight__odds-wrapper")
#     time.sleep(0.5)  # Appease the website
#     for element in elements:

#     # weight_classes = [element.text for element in elements]
#     print(elements)

def fighter_nations():
    return None

# Decision (split, unanimous), Submission (round), TKO/KO (round)
def win_method():
    return None 


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

print(get_fighters())

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