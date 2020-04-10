from PIL import Image

class ForecastDay():
    def __init__(self, day_of_the_week, day_of_the_month, month, image, temperature, weather, feels_like, wind, humidity, p_chance, p_ammount, UV, sunrise, sunset):
        self.day_of_the_week = day_of_the_week.upper()
        self.day_of_the_month = day_of_the_month.upper()
        self.month = month.upper()
        self.temperature = temperature.upper()
        self.weather = weather.upper()
        self.feels_like = feels_like.upper()
        self.wind = wind.upper()
        self.humidity = humidity.upper()
        self.p_chance = p_chance.upper()
        self.p_ammount = p_ammount.upper()
        self.UV = UV.upper()
        self.sunrise = sunrise.upper()
        self.sunset = sunset.upper()

        image_data = image.load()
        h, w = image.size
        for i in range(h):
            for j in range(w):
                if (image_data[i, j] == 0):
                    image_data[i, j] = 255
        self.image = image

    def __str__(self):
        return ' '.join([self.day_of_the_week, self.day_of_the_month, self.month, self.temperature, self.weather, self.feels_like, 
                        self.wind, self.humidity, self.p_chance, self.p_ammount, self.UV, self.sunrise, self.sunset])
