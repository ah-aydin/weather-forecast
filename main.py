import scrap_data
import sys

if __name__ == '__main__':
    forcastData = scrap_data.get_forecast_data('Tulcea')
    for day in forcastData:
        print(day)
