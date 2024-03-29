"""CSC111 Winter 2024 Project 2

Module Description
==================
This module contains the code to display the form for the recipe recommender.

Copyright and Usage Information
===============================
This file is Copyright (c) 2024 Akanksha Anand Iyengar, Leilia Ho, Diana Akhmedova, Herena Li
"""

import tkinter
import tree
import gui
from tkinter import ttk
from tkinter import *

def clear_form():
    difficulty_combo_box.set('')
    time_combo_box.set('')
    # calories_spinbox.delete(0, tkinter.END)
    calories_combo_box.set('')
    allergy_status_var.set('No')
    allergies_text.delete("1.0", tkinter.END)
    diet_listbox.selection_clear(0, tkinter.END)
    cuisine_listbox.selection_clear(0, tkinter.END)
    # food_text.delete("1.0", tkinter.END)
    food_combo_box.set('')
    other_text.delete("1.0", tkinter.END)

def enter_data():
    difficulty = difficulty_combo_box.get()
    time = time_combo_box.get()
    # calories = int(calories_spinbox.get())
    calories = calories_combo_box.get()
    allergy = allergy_status_var.get()
    list_allergies = allergies_text.get("1.0", tkinter.END).strip()
    diet_selection = [diet_listbox.get(idx) for idx in diet_listbox.curselection()]
    cuisine_selection = [cuisine_listbox.get(idx) for idx in cuisine_listbox.curselection()]
    # food = food_text.get("1.0", tkinter.END).strip()
    food = food_combo_box.get()
    other = other_text.get("1.0", tkinter.END).strip()

    decision_tree = tree.build_decision_tree("filtered_merged.csv")
    answers = [food, difficulty, time, calories]
    recipes = decision_tree.check_equality(answers)
    # TODO: filter data
    recipes = recipes[:5]  # take the first five recipes

    # calculate cal_range
    max_calories = max([recipe.calories for recipe in recipes])
    min_calories = min([recipe.calories for recipe in recipes])
    for recipe in recipes:
        recipe.cal_range = (min_calories, max_calories)

    # open the tabview
    gui.TabWindow(recipes)

    # print("Difficulty:", difficulty)
    # print("Time:", time)
    # print("Calories:", calories)
    # print("Allergy:", allergy)
    # print("List Allergies:", list_allergies)
    # print("Diet:", diet_selection)
    # print("Cuisine:", cuisine_selection)
    # print("Food:", food)
    # print("Other:", other)
    # print("---------------------------------")

    clear_form()

window = tkinter.Tk()
window.title("Questionnaire")

frame = tkinter.Frame(window)
frame.pack()

# Saving Basic Info
basic_info_frame = tkinter.LabelFrame(frame, text="Basic Information")
basic_info_frame.grid(row=0, column=0, sticky="news", padx=20, pady=10)

# Difficulty
difficulty_label = tkinter.Label(basic_info_frame, text="Difficulty")
difficulty_combo_box = ttk.Combobox(basic_info_frame, values=["Beginner", "Novice", "Intermediate", "Advanced", "Expert"])
difficulty_label.grid(row=0, column=0)
difficulty_combo_box.grid(row=1, column=0)

# Time Taken
time_label = tkinter.Label(basic_info_frame, text="Max Time Taken")
time_combo_box = ttk.Combobox(basic_info_frame, values=["0-29 Minutes", "30-79 Minutes", "80-159 Minutes", "160-239 Minutes", "240+ Minutes"])
time_label.grid(row=0, column=1)
time_combo_box.grid(row=1, column=1)

# Calories
# calories_label = tkinter.Label(basic_info_frame, text="Max Calories")
# calories_spinbox = tkinter.Spinbox(basic_info_frame, from_=0, to=5000) # TODO: Whats the max?
# calories_label.grid(row=0, column=2)
# calories_spinbox.grid(row=1, column=2)
calories_label = tkinter.Label(basic_info_frame, text="Calories")
calories_combo_box = ttk.Combobox(basic_info_frame, values=['Less than 500 calories', '500-999 calories', '1000-1499 calories', '1500-1999 calories', '2000 or more calories'])
calories_label.grid(row=0, column=2)
calories_combo_box.grid(row=1, column=2)

# Allergy
allergy_label = tkinter.Label(basic_info_frame, text="Have Allergies?")
allergy_status_var = tkinter.StringVar(value="No")
allergy_check = tkinter.Checkbutton(basic_info_frame, text="Yes", variable=allergy_status_var, onvalue="Yes", offvalue="No")
allergy_label.grid(row=2, column=0)
allergy_check.grid(row=3, column=0)

# List Allergies
allergies_label = tkinter.Label(basic_info_frame, text="List Allergies (separate by commas)")
allergies_text = tkinter.Text(basic_info_frame, width=5, height=2)
allergies_label.grid(row=2, column=1)
allergies_text.grid(row=3, column=1, sticky="ew", padx=5)

for widget in basic_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=10)

# Saving Preferences
preferences_frame = tkinter.LabelFrame(frame, text="Preferences")
preferences_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

# Diet
diet_label = tkinter.Label(preferences_frame, text="Diet")
diet_label.grid(row=0, column=0)
diet_frame = tkinter.Frame(preferences_frame)
diet_frame.grid(row=1, column=0)

diet_scrollbar = tkinter.Scrollbar(diet_frame, orient=tkinter.VERTICAL)
diet_listbox = tkinter.Listbox(diet_frame, selectmode="multiple", yscrollcommand=diet_scrollbar.set, exportselection=0)
diet_list = ["Vegetarian", "Vegan", "Pescetarian", "Dairy-Free", "Gluten-Free", "Lactose-Free", "Low-Cholesterol", "Halal", "Kosher", "Keto", "Paleo"]
for diet_item in diet_list:
    diet_listbox.insert(tkinter.END, diet_item)

diet_listbox.grid(row=0, column=0, sticky="nsew")
diet_scrollbar.config(command=diet_listbox.yview)
diet_scrollbar.grid(row=0, column=1, sticky="ns")

preferences_frame.columnconfigure(0, weight=1)
preferences_frame.rowconfigure(1, weight=1)

# Cuisine
cuisine_label = tkinter.Label(preferences_frame, text="Cuisine")
cuisine_label.grid(row=0, column=1)
cuisine_frame = tkinter.Frame(preferences_frame)
cuisine_frame.grid(row=1, column=1)

cuisine_scrollbar = tkinter.Scrollbar(cuisine_frame, orient=tkinter.VERTICAL)
cuisine_listbox = tkinter.Listbox(cuisine_frame, selectmode="multiple", yscrollcommand=cuisine_scrollbar.set, exportselection=0)
cuisine_list = ["African", "American", "Chinese", "French", "Greek", "Indian", "Italian", "Japanese", "Korean", "Mexican", "Middle-Eastern", "Spanish", "Thai", "Vietnamese"]
for cuisine_item in cuisine_list:
    cuisine_listbox.insert(tkinter.END, cuisine_item)

cuisine_listbox.grid(row=0, column=0, sticky="nsew")
cuisine_scrollbar.config(command=cuisine_listbox.yview)
cuisine_scrollbar.grid(row=0, column=1, sticky="ns")

preferences_frame.columnconfigure(1, weight=1)
preferences_frame.rowconfigure(1, weight=1)

# Food
# food_label = tkinter.Label(preferences_frame, text="Food (separate by commas)")
# food_text = tkinter.Text(preferences_frame, width=5, height=10)
# food_label.grid(row=0, column=2)
# food_text.grid(row=1, column=2, sticky="ew", padx=5)
food_label = tkinter.Label(preferences_frame, text="Food")
food_combo_box = ttk.Combobox(preferences_frame, values=["Main dish", "Side dish", "Dessert", "Other"])
food_label.grid(row=0, column=2)
food_combo_box.grid(row=1, column=2, sticky="ew", padx=5)

# Other
other_label = tkinter.Label(preferences_frame, text="Other (separate by commas)")
other_text = tkinter.Text(preferences_frame, width=5, height=2)
other_label.grid(row=2, column=1)
other_text.grid(row=3, column=1, sticky="ew", padx=5)

for widget in preferences_frame.winfo_children():
    widget.grid_configure(padx=10, pady=10)

# Submit Button
button = tkinter.Button(frame, text="Submit", command=enter_data)
button.grid(row=2, column=0, sticky="news", padx=20, pady=10)

# Clear Button
clear_button = tkinter.Button(frame, text="Clear", command=clear_form)
clear_button.grid(row=3, column=0, sticky="news", padx=20, pady=10)

window.mainloop()
