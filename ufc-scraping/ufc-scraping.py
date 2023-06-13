import requests
from bs4 import BeautifulSoup
import time

# Specify the URL of the webpage you want to fetch
url = "https://www.ufc.com/event/ufc-288"

# Send a GET request to the URL
response = requests.get(url)
# time.sleep(0.5) # Sleep for 0.5 seconds

# Get the HTML content from the response
html_content = response.text

# Specify the use of lxml parser
soup = BeautifulSoup(html_content, 'lxml')

# Finding the class of the element I want: Fighter names
def find_classes(input):
    input_found = soup.find_all(string=input)
    if input_found is None:
        print("Input not found")
        return None
    input_classes = [input.parent.get('class') for input in input_found]
    # Make it so that this is an option
    input_parents = [input.parent for input in input_found]
    print(input_parents)
    # It ("get()") returns a list, but there's only 1 element in it (usually)
    return input_classes

# What's the difference between the red corner and blue corner in the ufc
def get_fighters():
    elements = (soup.find_all(class_="c-listing-ticker-fightcard__red_corner_name"))
    red_corner_fighter_names = [element.text for element in elements]
    print(red_corner_fighter_names)
    time.sleep(0.5) # Appease the website

    elements = (soup.find_all(class_="c-listing-ticker-fightcard__blue_corner_name"))
    blue_corner_fighter_names = [element.text for element in elements]
    print(blue_corner_fighter_names)
    time.sleep(0.5) # Appease the website

def get_win_loss():
    red_corner_win_loss = list()
    elements = (soup.find_all(class_="c-listing-fight__corner-body--red"))
    for element in elements:
        subclass_element = element.find(class_="c-listing-fight__outcome-wrapper")
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
    elements = (soup.find_all(class_="c-listing-fight__corner-body--blue"))
    for element in elements:
        subclass_element = element.find(class_="c-listing-fight__outcome-wrapper")
        print(subclass_element, "end of subclass element")
        if subclass_element:
            if subclass_element.find(class_="c-listing-fight__outcome--Win"):
                blue_corner_win_loss.append("Win")
            elif subclass_element.find(class_="c-listing-fight__outcome--Loss"):
                blue_corner_win_loss.append("Loss")
        else:
            print("Subclass element not found.")
    print("Red Corner W\L", red_corner_win_loss, "\n\n\n\n", "Blue Corner W\L", blue_corner_win_loss)
    
def get_fight_class():
    elements = (soup.find_all(class_="c-listing-fight__class-text"))
    print(elements)
# Some outliers where you have a title fight with an unranked opponent (coming up from different weight class)
def get_fighters_ranks():
    elements = (soup.find_all(class_="c-listing-fight__class-text"))
    print(elements)

get_fight_class()

# def print_parents(child):
#     print(child.parent, "\n")
#     print_parents(child.parent)

# print_parents(phrase)