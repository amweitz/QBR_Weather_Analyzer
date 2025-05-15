# --- Import Required Libraries ---
import sys
import psycopg2                  # PostgreSQL adapter for Python
import matplotlib
matplotlib.use('TkAgg')          # Set matplotlib backend to TkAgg for GUI support
import matplotlib.pyplot as plt  # For plotting
import mplcursors                # For interactive annotations on the plot
import tkinter as tk             # GUI toolkit
from tkinter import ttk          # Themed widgets like Combobox

# --- Database Connection ---
# Connect to the PostgreSQL database using the given credentials
conn = psycopg2.connect(
    dbname="qbr",
    user="insert username",
    host="insert host",
    port="insert port"
)
cur = conn.cursor()  # Create a cursor to perform database operations

# --- Fetch Unique Player Names ---
# Query to get a list of unique player names from the QBR data
cur.execute("SELECT DISTINCT first_name, last_name FROM weekly_qbr ORDER BY last_name, first_name;")
all_names = cur.fetchall()  # List of tuples: [(first1, last1), (first2, last2), ...]
name_options = [f"{first} {last}" for first, last in all_names]  # Convert to list of "First Last" strings

# --- GUI: Dropdown Selector ---
selected_name = None    # Placeholder for the selected player
use_everyone = False    # Flag to determine if all players should be used

# Function to run when "OK" button is clicked
def submit_selection():
    global selected_name
    selected_name = combo.get()
    root.destroy()  # Close the GUI window

# Function to run when "Everyone" button is clicked
def submit_everyone():
    global selected_name, use_everyone
    selected_name = None
    use_everyone = True
    root.destroy()  # Close the GUI window

# Function to auto-fill the dropdown based on typed input
def on_search_change(*args):
    typed = search_var.get().lower()
    for name in name_options:
        if typed in name.lower():
            combo.set(name)
            break

# Create GUI window
root = tk.Tk()
root.title("Select Player")

# Search bar label + entry
tk.Label(root, text="Quick Search:").pack(padx=10, pady=(10, 0))
search_var = tk.StringVar()
search_var.trace_add("write", on_search_change)  # Trigger filter as user types
search_entry = tk.Entry(root, textvariable=search_var, width=40)
search_entry.pack(padx=10, pady=(0, 10))

# Dropdown label + Combobox
tk.Label(root, text="Select Player:").pack()
combo = ttk.Combobox(root, values=name_options, width=40)
combo.pack(padx=10, pady=5)

# Frame to hold buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# "OK" and "Everyone" buttons
submit_btn = tk.Button(button_frame, text="OK", command=submit_selection)
submit_btn.pack(side=tk.LEFT, padx=5)

everyone_btn = tk.Button(button_frame, text="Everyone", command=submit_everyone)
everyone_btn.pack(side=tk.LEFT, padx=5)

# Start GUI event loop
root.mainloop()

# --- Parse Selected Name ---
# Split the full name into first and last names if a player was selected
if not use_everyone and selected_name and ' ' in selected_name:
    first_name, last_name = selected_name.split(' ', 1)
    first_name = first_name.capitalize()
    last_name = last_name.capitalize()
else:
    first_name = None
    last_name = None

# --- Query Function ---
# Function to query average QBR grouped by temperature bucket
def get_qbr_data(cur, first_name=None, last_name=None):
    # Build WHERE clause
    conditions = [
        "w.temperature IS NOT NULL",  # Exclude games with missing temperature
        "q.season >= 2013"            # Focus on more recent seasons
    ]
    values = []

    if first_name and last_name:
        conditions.append("q.first_name = %s")
        conditions.append("q.last_name = %s")
        values += [first_name, last_name]

    where_clause = " AND ".join(conditions)

    # SQL query: Join QBR and weather data, group by 10°F temperature buckets
    query = f"""
    SELECT 
      FLOOR(w.temperature / 10) * 10 AS temp_bucket,
      ROUND(AVG(q.qbr_total)::numeric, 2) AS avg_qbr,
      COUNT(*) AS game_count
    FROM weekly_qbr q
    JOIN nfl_weather w
      ON q.season = w.year
     AND q.week_text = w.week
     AND q.team = w.team
    WHERE {where_clause}
    GROUP BY temp_bucket
    ORDER BY temp_bucket;
    """

    cur.execute(query, values)  # Execute query with optional parameters
    return cur.fetchall()       # Return result rows

# --- Query Data ---
res = get_qbr_data(cur, first_name, last_name)  # Run query with selected player or all
cur.close()  # Close cursor
conn.close()  # Close database connection

# --- Parse Query Results ---
temps = [row[0] for row in res]     # List of temperature buckets (e.g. 40, 50, 60)
qbrs = [row[1] for row in res]      # Corresponding average QBRs
counts = [row[2] for row in res]    # Game count in each bucket
sizes = [c * 10 for c in counts]    # Bubble size scaled by number of games

# --- Plotting ---
fig, ax = plt.subplots(figsize=(7, 6))  # Create figure and axis

# Create scatter plot: x = temp bucket, y = QBR, size = game count
sc = ax.scatter(temps, qbrs, s=sizes, alpha=0.7, edgecolors='black')

# Set plot title
title = f'Average QBR vs Temp - {first_name} {last_name}' if first_name and last_name else 'Average QBR vs Temp (All Players)'
ax.set_title(title)
ax.set_xlabel('Temperature Range (°F)')
ax.set_ylabel('QBR Total')
ax.grid(True)
ax.set_ylim(0, 100)  # QBR is scaled from 0 to 100

# Format x-axis with labels like "30-40", "40-50", etc.
bucket_labels = [f"{t}-{t+10}" for t in temps]
ax.set_xticks(temps)
ax.set_xticklabels(bucket_labels)

# Add hover interaction to show number of games per point
cursor = mplcursors.cursor(sc, hover=True)
cursor.connect("add", lambda sel: sel.annotation.set_text(f"Games: {counts[sel.index]}"))

plt.tight_layout()  # Adjust layout to fit well
plt.show()          # Display the plot