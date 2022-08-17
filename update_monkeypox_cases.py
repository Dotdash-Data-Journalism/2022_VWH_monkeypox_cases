import requests
import pandas as pd
import numpy as np
from datetime import datetime, date
import time
from datawrapper import Datawrapper
import os

ACCESS_TOKEN = os.getenv('DW_API_KEY')

dw = Datawrapper(access_token=ACCESS_TOKEN)

### Function to get the covid json as a dataframe and the latest update date as a datetime
def getMonkeypoxJSON(url):
    try:
        df = pd.read_csv(filepath_or_buffer=url,
        index_col=False, header=0, sep=",", dtype={"Location":str, "Cases":int, "Case Range":str, "AsOf": str})
    except urllib.error.HTTPError as errh:
        print(f"Http Error:{errh}")
    except urllib.error.URLError as err:
        print(f"Other error:{err}")

    df['AsOf'] = df['AsOf'].str.replace(r'Data as of ', '')
    
    updateDate = datetime.strptime(df['AsOf'][0], "%d %b %Y %I:%M %p %Z").date()

    return(df, updateDate)

### Function to update datawrapper charts
def updateChart(dw_chart_id, dataSet, updateDate, dw_api_key):
    dw.add_data(
    chart_id=dw_chart_id,
    data=dataSet
    )

    time.sleep(2)

    headers = {
    "Accept": "*/*",
    "Content-Type": "application/json",
    "Authorization": "Bearer " + dw_api_key
    }

    response = requests.request(method="PATCH", 
                                url="https://api.datawrapper.de/v3/charts/" + dw_chart_id, 
                                json={"metadata": {
                                        "annotate": {
                                            "notes": "Updated " + str(updateDate.strftime('%B %d, %Y'))
                                    }
                                }},
                                headers=headers)

    response.raise_for_status()

    time.sleep(2)

    dw.publish_chart(chart_id=dw_chart_id)

cdc_monkeypox_full = getMonkeypoxJSON("https://www.cdc.gov/wcms/vizdata/poxvirus/monkeypox/data/USmap_counts.csv")

cdc_monkeypox_latest = cdc_monkeypox_full[0]
cdc_monkeypox_latest_date = cdc_monkeypox_full[1]

cdc_monkeypox_latest['AsOf'] = cdc_monkeypox_latest_date

cdc_monkeypox = pd.read_csv(filepath_or_buffer="./visualizations/cdc_monkeypox_cases.csv", 
                            index_col= False,
                            header=0,
                            sep=",",
                            dtype={"Location":str, "Cases":int, "Case Range":str},
                            parse_dates=['AsOf'])

cdc_monkeypox['AsOf'] = cdc_monkeypox['AsOf'].dt.date

cdc_monkeypox_date = max(cdc_monkeypox['AsOf'])

if cdc_monkeypox_latest_date > cdc_monkeypox_date:
    full_cdc_monkeypox = pd.concat([cdc_monkeypox_latest, cdc_monkeypox])

    full_cdc_monkeypox.to_csv("./visualizations/cdc_monkeypox_cases.csv", index=False)

    # Only select rows and columns we want
    vizDF = cdc_monkeypox_latest.loc[~(cdc_monkeypox_latest['Location'].isin(["Non-US Resident", "Puerto Rico", "Total"])), ['Location', 'Cases', 'Case Range', 'AsOf']].reset_index(drop=True)

    updateChart('4SHvi', vizDF, cdc_monkeypox_latest_date, ACCESS_TOKEN)
