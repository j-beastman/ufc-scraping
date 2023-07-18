import pandas as pd
from ufc_scraping import get_event_data


df = get_event_data()


df.to_csv("data/ufc-raw-data.csv", index=False)