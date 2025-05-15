import requests
from bs4 import BeautifulSoup
import csv

def scrape_nfl_weather(year, week, writer):
    # Map for special week names
    special_week_names = {
        "wildcard-weekend": "Wild Card",
        "divisional-playoffs": "Divisional Round",
        "conf-championships": "Conference Championship",
        "superbowl": "Super Bowl"
    }

    # Construct the URL and label
    if isinstance(week, int):
        url = f"https://www.nflweather.com/week/{year}/week-{week}"
        week_label = f"Week {week}"
    else:
        url = f"https://www.nflweather.com/week/{year}/{week}"
        week_label = special_week_names.get(week, week)

    # Send HTTP request
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve {url}. Status code: {response.status_code}")
        return

    # Parse HTML
    soup = BeautifulSoup(response.content, "html.parser")
    games = soup.find_all("div", class_="game-box")

    for game in games:
        weather_div = game.find("div", class_="mx-2")
        weather = weather_div.find("span") if weather_div else None
        team1 = game.find("span", class_="fw-bold")
        team2 = game.find("span", class_="fw-bold ms-1")

        if weather and team1 and team2:
            temperature = weather.get_text(strip=True).split(" ")[0]
            team1_name = team1.get_text(strip=True)
            team2_name = team2.get_text(strip=True)
            writer.writerow([year, week_label, team1_name, temperature])
            writer.writerow([year, week_label, team2_name, temperature])

# Open CSV file and write header
with open("nfl_weather.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["year", "week", "team", "temperature"])  # CSV header

    # Loop over all years and weeks
    for y in range(2013, 2023):
        for x in range(1, 17):
            scrape_nfl_weather(y, x, writer)
        scrape_nfl_weather(y, "wildcard-weekend", writer)
        scrape_nfl_weather(y, "divisional-playoffs", writer)
        scrape_nfl_weather(y, "conf-championships", writer)
        scrape_nfl_weather(y, "superbowl", writer)