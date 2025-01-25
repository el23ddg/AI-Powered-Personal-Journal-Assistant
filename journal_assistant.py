import tkinter as tk
from tkinter import ttk, messagebox
from textblob import TextBlob
import csv
import os
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from tkcalendar import Calendar

# Function to save entry to CSV
def save_entry_to_csv(entry, mood):
    file_exists = os.path.exists("journal.csv")
    with open("journal.csv", "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Entry", "Mood"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d"), entry, mood])

# Function to analyze mood
def analyze_mood(entry):
    blob = TextBlob(entry)
    sentiment = blob.sentiment.polarity
    if sentiment > 0:
        return "Happy"
    elif sentiment == 0:
        return "Neutral"
    else:
        return "Sad"

# Function to visualize mood trends
def visualize_mood_trends():
    if not os.path.exists("journal.csv"):
        messagebox.showerror("Error", "No data available to visualize!")
        return

    moods = []
    with open("journal.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            moods.append(row[2])

    mood_counts = {"Happy": moods.count("Happy"), 
                   "Neutral": moods.count("Neutral"), 
                   "Sad": moods.count("Sad")}

    sns.set_style("whitegrid")
    plt.figure(figsize=(6, 4))
    sns.barplot(x=list(mood_counts.keys()), y=list(mood_counts.values()), palette="pastel")
    plt.title("Mood Trends", fontsize=16)
    plt.ylabel("Number of Entries")
    plt.xlabel("Moods")
    plt.show()

# Function to search journal entries
def search_entries(keyword):
    if not os.path.exists("journal.csv"):
        messagebox.showerror("Error", "No journal entries to search!")
        return []

    results = []
    with open("journal.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if keyword.lower() in row[1].lower():
                results.append(f"Date: {row[0]}\nEntry: {row[1]}\nMood: {row[2]}\n")
    return results

# Save entry function
def save_entry():
    entry = text_box.get("1.0", tk.END).strip()
    if not entry:
        messagebox.showwarning("Warning", "Journal entry cannot be empty!")
        return

    mood = analyze_mood(entry)
    save_entry_to_csv(entry, mood)
    text_box.delete("1.0", tk.END)
    messagebox.showinfo("Success", f"Entry saved! Mood: {mood}")
    show_latest_entry()

# Search journal function
def search_journal():
    keyword = search_box.get().strip()
    if not keyword:
        messagebox.showwarning("Warning", "Search keyword cannot be empty!")
        return

    results = search_entries(keyword)
    if results:
        result_window = tk.Toplevel(root)
        result_window.title("Search Results")
        result_text = tk.Text(result_window, height=20, width=60)
        result_text.pack()
        result_text.insert("1.0", "\n\n".join(results))
        result_text.config(state="disabled")
    else:
        messagebox.showinfo("No Results", "No entries found for the given keyword.")

# Function to toggle dark mode
def toggle_dark_mode():
    if root["bg"] == "white":
        root.config(bg="black")
        label.config(bg="black", fg="white")
        text_box.config(bg="gray", fg="white")
        search_label.config(bg="black", fg="white")
        latest_label.config(bg="black", fg="white")
    else:
        root.config(bg="white")
        label.config(bg="white", fg="black")
        text_box.config(bg="white", fg="black")
        search_label.config(bg="white", fg="black")
        latest_label.config(bg="white", fg="black")

# Function to show the latest entry
def show_latest_entry():
    if os.path.exists("journal.csv"):
        with open("journal.csv", "r") as file:
            reader = list(csv.reader(file))
            if len(reader) > 1:
                latest_entry = reader[-1]
                latest_label.config(text=f"Last Entry: {latest_entry[1]}\nMood: {latest_entry[2]}")
            else:
                latest_label.config(text="No entries yet!")

# Function to show a calendar for selecting dates
def show_calendar():
    cal_window = tk.Toplevel(root)
    cal_window.title("Select a Date")
    cal = Calendar(cal_window, selectmode="day")
    cal.pack()

    def fetch_date():
        selected_date = cal.get_date()
        # Add functionality to display entries for selected_date
        messagebox.showinfo("Selected Date", f"You picked {selected_date}")

    submit_button = tk.Button(cal_window, text="OK", command=fetch_date)
    submit_button.pack()

# Main GUI setup
root = tk.Tk()
root.title("AI-Powered Personal Journal Assistant")
root.geometry("600x500")
root.config(bg="white")

# Header and instructions
label = tk.Label(root, text="Write your journal entry below:", font=("Helvetica", 14), bg="white")
label.pack(pady=10)

# Text box for journal entry
text_box = tk.Text(root, height=10, width=60)
text_box.pack(pady=10)

# Save entry button
save_button = tk.Button(root, text="Save Entry", command=save_entry, bg="#4CAF50", fg="white")
save_button.pack(pady=5)

# Latest entry display
latest_label = tk.Label(root, text="", font=("Helvetica", 12), bg="white")
latest_label.pack(pady=5)
show_latest_entry()

# Visualize mood trends
visualize_button = tk.Button(root, text="Visualize Mood Trends", command=visualize_mood_trends, bg="#2196F3", fg="white")
visualize_button.pack(pady=5)

# Search bar
search_label = tk.Label(root, text="Search Journal Entries:", font=("Helvetica", 12), bg="white")
search_label.pack()
search_box = tk.Entry(root, width=30)
search_box.pack(pady=5)
search_button = tk.Button(root, text="Search", command=search_journal, bg="#FFC107", fg="black")
search_button.pack(pady=5)

# Dark mode toggle
dark_mode_button = tk.Button(root, text="Toggle Dark Mode", command=toggle_dark_mode, bg="#F5F5DC", fg="black")
dark_mode_button.pack(pady=5)

# Calendar button
calendar_button = tk.Button(root, text="Open Calendar", command=show_calendar, bg="#009688", fg="white")
calendar_button.pack(pady=5)

# Run the Tkinter event loop
root.mainloop()
