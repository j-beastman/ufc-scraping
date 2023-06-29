import pandas as pd
from ufc_scraping import get_event_info


# get_event
df = pd.DataFrame(get_event_info(288))
print(df.head())

df.to_csv("data/ufc-raw-data.csv", index=False)