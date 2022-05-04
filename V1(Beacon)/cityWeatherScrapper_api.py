# -*- coding: utf-8 -*-

import requests
# base URL
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
CITY = "Andover,US"
API_KEY = "7a7adfc0a5635b1627c72eccab71a8e9"
URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY
response = requests.get(URL)

# checking the status code of the request
if response.status_code == 200:

   data = response.json()

   main = data['main']
   temperature = round(main['temp']-273, 2) #n celcius
   humidity = main['humidity']
   pressure = main['pressure']
   
   
   # weather report
   report = data['weather']
   print(f"{CITY:-^30}")
   print("Temperature:", temperature)
   print("Humidity:", humidity)
   print("Pressure:", pressure)
   print("Weather Report:",report[0]['description'])
else:
   # showing the error message
   print("Error in the HTTP request")
