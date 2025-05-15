# QBR vs Temperature Analysis

**Note:** This project uses NFL weekly QBR statistics from **2013 through 2023**, including only games where the QBR rating was finalized.

This project visualizes the relationship between NFL quarterback performance (measured by QBR) and outdoor game temperatures.  
It uses data from two main sources: weekly QBR statistics and weather conditions during NFL games.

## 📊 Features

- Interactive **Tkinter GUI** to select a specific quarterback or analyze all players.  
- Automatically filters and queries data from a **PostgreSQL** database.  
- Plots a **scatter chart** using `matplotlib` where:  
  - **X-axis** shows temperature buckets (e.g., 40–50°F).  
  - **Y-axis** shows average QBR in that range.  
  - **Bubble size** reflects the number of games in each temperature bucket.  
  - **Hover tooltip** displays exact game counts (via `mplcursors`).

## 🏈 What is QBR?

ESPN’s Total Quarterback Rating (Total QBR) incorporates all of a quarterback’s contributions to winning, including how he impacts the game on passes, rushes, turnovers, and penalties. Since QBR is built from the play level, it accounts for a team’s success or failure on every play to provide proper context and then allocates credit to the quarterback and teammates to produce a clearer measure of quarterback efficiency. — *ESPN*

In our project, we used QBR to assess how quarterback performance changes with outdoor temperature. By averaging QBR scores across 10-degree temperature buckets, we visualized trends—identifying whether certain quarterbacks excel or struggle in cold or hot conditions based on their Total QBR.

## 🏈 Data Sources

- **QBR Data**: Taken from the [`qbr-nfl-weekly.csv`](https://github.com/nflverse/espnscrapeR-data/blob/master/data/qbr-nfl-weekly.csv) file provided by the [`espnscrapeR-data`](https://github.com/nflverse/espnscrapeR-data/tree/master/data) project by [nflverse](https://github.com/nflverse).  
- **Weather Data**: Scraped from [nflweather.com](http://www.nflweather.com) using a custom Python scraper.

## 🛠️ Requirements

- Python 3.7+  
- PostgreSQL (with populated `weekly_qbr` and `nfl_weather` tables)  
- Python packages:  
  - `psycopg2`  
  - `matplotlib`  
  - `mplcursors`  
  - `tkinter`
