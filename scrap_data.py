import requests as req
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from forecast_day import ForecastDay

def get_forecast_data(city_name):

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763'}

    main_page = req.get('https://www.timeanddate.com/weather/results.html?query='+city_name, headers=headers)
    s_main_page = BeautifulSoup(main_page.text, features='html.parser')
    href_forecast_page = s_main_page.find('td', {'class': 'sep-thick'}).find('a')['href']
    del main_page, s_main_page


    forecast_page = req.get('https://www.timeanddate.com'+href_forecast_page+'/ext', headers=headers)
    s_forecast_page = BeautifulSoup(forecast_page.text, features='html.parser')
    forecast_table = s_forecast_page.find('table', {'id': 'wt-ext'}).find('tbody').find_all('tr')
    del forecast_page, s_forecast_page

    forecastDays = []
    for day in forecast_table:

        # Get the day of the week, day of the month and the month
        date = day.find('th').text
        day_of_the_week = ''
        day_of_the_month = ''
        month = date.split(' ')[-1]
        for i in range(len(date)):
            if date[i].isdecimal() == False:
                day_of_the_week += date[i]
            elif date[i].isdecimal() == True:
                day_of_the_month += date[i]
            if date[i] == ' ':
                break
        
        # Get the image
        image_src = day.find('img')['src']
        image_location = req.get('http:'+image_src, headers=headers)
        image = Image.open(BytesIO(image_location.content))
        
        # Get the remaining data
        data = day.find_all('td')[1:] # The first 'td' will have the image in it which has allready been stored
        temperature = data[0].text
        weather = data[1].text
        feels_like = data[2].text
        wind = data[3].text
        humidity = data[5].text
        p_chance = data[6].text
        p_ammount = data[7].text
        UV = data[8].text
        sunrise = data[9].text
        sunset = data[10].text
        forecastDay = ForecastDay(day_of_the_week, day_of_the_month, month, image, temperature, weather, feels_like, wind, humidity, p_chance, p_ammount, UV, sunrise, sunset)
        forecastDays.append(forecastDay)

    del forecast_table

    return forecastDays