class ForecastDay():
    def __init__(self, day_of_the_week, day_of_the_month, month, image, temperature, weather, feels_like, wind, humidity, p_chance, p_ammount, UV, sunrise, sunset):
        self.day_of_the_week = day_of_the_week[0].upper() + day_of_the_week[1:]
        self.day_of_the_month = day_of_the_month
        self.month = month
        self.image = image
        self.temperature = temperature
        self.weather = ' ' + weather
        self.feels_like = feels_like
        self.wind = wind
        self.humidity = humidity
        self.p_chance = p_chance
        self.p_ammount = p_ammount
        self.UV = UV
        self.sunrise = sunrise
        self.sunset = sunset
    
    def __str__(self):
        return ' '.join([self.day_of_the_week, self.day_of_the_month, self.month, self.temperature, self.weather, self.feels_like, 
                        self.wind, self.humidity, self.p_chance, self.p_ammount, self.UV, self.sunrise, self.sunset])
