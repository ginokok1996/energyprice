from twilio.rest import Client
import requests
import psycopg2
import rich
import json
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta

current_date = datetime.now()
#day_before_yesterday_date = current_date - timedelta(days=2)
yesterday_date = current_date - timedelta(days=1)


URL = f"https://api.energyzero.nl/v1/energyprices?fromDate={yesterday_date.strftime('%Y-%m-%d')}T00:00:00.000Z&tillDate={current_date.strftime('%Y-%m-%d')}T00:00:00.000Z&interval=4&usageType=1&inclBtw=true"
page = requests.get(URL)

output_page = page.json()

output = ""

for item in output_page['Prices']:
    output += f"Tijd: {item['readingDate'].split('T')[-1].replace('Z','')[:2]} Prijs: {item['price']}"
    output += "\n"

print(output)
labels = []
values = []

for item in output_page['Prices']:
    labels.append(item['readingDate'].split('T')[-1].replace('Z', '')[:2])
    values.append(item['price'])
    
plt.bar(labels, values)

plt.xlabel('Tijd')
plt.ylabel('Prijs')

plt.title('Prijs per uur')
plt.savefig(f'./images/price_plot_{current_date.strftime("%Y-%m-%d")}.png')
