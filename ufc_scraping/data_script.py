import pandas as pd
from ufc_scraping import get_event_data

links = pd.read_csv('data/links_to_events.csv')

for link in links:
    df = get_event_data()


df.to_csv("data/ufc-raw-data.csv", index=False)