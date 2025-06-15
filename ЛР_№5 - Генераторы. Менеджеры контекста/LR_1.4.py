def build_country_city_dict(data):
    country_city = {}
    for item in data:
        parts = item.split()
        country = parts[0]
        cities = parts[1:]
        for city in cities:
            country_city[city] = country
    return country_city

def find_countries_for_cities(country_city_dict, cities_to_find):
    for city in cities_to_find:
        country = country_city_dict.get(city, "Error")
        print(f"{city} -- {country}")

# Входные данные
input_data = [
    "Россия Москва Санкт-Петербург Новосибирск",
    "Германия Берлин Мюнхен Гамбург",
    "Франция Париж Лион Марсель"
]

cities_to_search = ["Москва", "Берлин", "Лион", "Киев"]

# Обработка
country_dict = build_country_city_dict(input_data)
find_countries_for_cities(country_dict, cities_to_search)