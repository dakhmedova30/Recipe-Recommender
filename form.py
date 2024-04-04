"""CSC111 Winter 2024 Project 2

Module Description
==================
This module contains the code necessary to run the questionnaire form in the recipe recommender.

Copyright and Usage Information
===============================
This file is Copyright (c) 2024 Akanksha Anand Iyengar, Leilia Ho, Diana Akhmedova, Herena Li
"""

import tkinter
from tkinter import ttk
from tkinter import *
import tree
import gui


def clear_form() -> None:
    """Clears all previous answers in the form.
    """
    DIFFICULTY_COMBO_BOX.set('')
    TIME_COMBO_BOX.set('')
    CALORIES_SPINBOX.delete(0, tkinter.END)
    ALLERGY_STATUS_VAR.set('No')
    ALLERGIES_TEXT.delete("1.0", tkinter.END)
    DIET_LISTBOX.selection_clear(0, tkinter.END)
    CUISINE_LISTBOX.selection_clear(0, tkinter.END)
    FOOD_TEXT.delete("1.0", tkinter.END)
    OTHER_TEXT.delete("1.0", tkinter.END)


def enter_data() -> None:
    """Takes the inputs in the form and displays the five recommended recipes in a new tab.
    """
    difficulty = DIFFICULTY_COMBO_BOX.get()
    time = TIME_COMBO_BOX.get()
    calories = int(CALORIES_SPINBOX.get())
    allergy = ALLERGY_STATUS_VAR.get()
    list_allergies = ALLERGIES_TEXT.get("1.0", tkinter.END).strip().split(',')

    diet_selection = [DIET_LISTBOX.get(idx) for idx in DIET_LISTBOX.curselection()]
    cuisine_selection = [CUISINE_LISTBOX.get(idx) for idx in CUISINE_LISTBOX.curselection()]
    food = FOOD_TEXT.get("1.0", tkinter.END).strip().split(',')
    dish = [DISH_LISTBOX.get(idx) for idx in DISH_LISTBOX.curselection()][0]
    other = OTHER_TEXT.get("1.0", tkinter.END).strip().split(',')

    print("Difficulty:", difficulty)
    print("Time:", time)
    print("Calories:", calories)
    print("Allergy:", allergy)
    print("List Allergies:", list_allergies)
    print("Diet:", diet_selection)
    print("Cuisine:", cuisine_selection)
    print("Food:", food)
    print("Type of Dish", dish)
    print("Other:", other)
    print("---------------------------------")

    match difficulty:
        case "Beginner":
            n_steps = '5'
        case "Novice":
            n_steps = '10'
        case "Intermediate":
            n_steps = '20'
        case "Advanced":
            n_steps = '30'
        case _:
            n_steps = '30+'

    match time:
        case "0-29 Minutes":
            time_threshold = '30'
        case "30-79 Minutes":
            time_threshold = '80'
        case "80-159 Minutes":
            time_threshold = '160'
        case "160-239 Minutes":
            time_threshold = '240'
        case _:
            time_threshold = '240+'

    if calories < 500:
        calorie_level = '500'
    elif calories < 1000:
        calorie_level = '1000'
    elif calories < 1500:
        calorie_level = '1500'
    elif calories < 2000:
        calorie_level = '2000'
    else:
        calorie_level = '2000+'

    decision_tree = tree.build_decision_tree("filtered_merged.csv")
    portion = dish.lower()
    allergens = list_allergies
    diet = diet_selection
    cuisine = cuisine_selection
    recipes = decision_tree.check_equality(
        [portion, n_steps, time_threshold, calorie_level])
    recipes = tree.filter_recipes(recipes, allergens, diet, food, cuisine, other)

    recipes = recipes[:5]  # take the first five recipes
    # calculate cal_range
    if len(recipes) > 0:
        max_calories = max([recipe1.calories for recipe1 in recipes])
        min_calories = min([recipe2.calories for recipe2 in recipes])
        for recipe in recipes:
            recipe.cal_range = (min_calories, max_calories)

    gui.TabWindow(recipes)

    clear_form()


WINDOW = tkinter.Tk()
WINDOW.title("Questionnaire")

FRAME = tkinter.Frame(WINDOW)
FRAME.pack()

# Saving Basic Info
BASIC_INFO_FRAME = tkinter.LabelFrame(FRAME, text="Basic Information")
BASIC_INFO_FRAME.grid(row=0, column=0, sticky="news", padx=20, pady=10)

# Difficulty
DIFFICULTY_LABEL = tkinter.Label(BASIC_INFO_FRAME, text="*Difficulty")
DIFFICULTY_COMBO_BOX = ttk.Combobox(BASIC_INFO_FRAME,
                                    values=["Beginner", "Novice", "Intermediate", "Advanced", "Expert"],
                                    state="readonly")
DIFFICULTY_LABEL.grid(row=0, column=0)
DIFFICULTY_COMBO_BOX.grid(row=1, column=0)

# Time Taken
TIME_LABEL = tkinter.Label(BASIC_INFO_FRAME, text="*Max Time Taken")
TIME_COMBO_BOX = ttk.Combobox(BASIC_INFO_FRAME,
                              values=["0-29 Minutes", "30-79 Minutes", "80-159 Minutes", "160-239 Minutes",
                                      "240+ Minutes"], state="readonly")
TIME_LABEL.grid(row=0, column=1)
TIME_COMBO_BOX.grid(row=1, column=1)

# Calories
CALORIES_LABEL = tkinter.Label(BASIC_INFO_FRAME, text="*Calories")
CALORIES_SPINBOX = tkinter.Spinbox(BASIC_INFO_FRAME, from_=0, to=5000)
CALORIES_LABEL.grid(row=0, column=2)
CALORIES_SPINBOX.grid(row=1, column=2)

# Allergy
ALLERGY_LABEL = tkinter.Label(BASIC_INFO_FRAME, text="Have Allergies?")
ALLERGY_STATUS_VAR = tkinter.StringVar(value="No")
ALLERGY_CHECK = tkinter.Checkbutton(BASIC_INFO_FRAME, text="Yes", variable=ALLERGY_STATUS_VAR, onvalue="Yes",
                                    offvalue="No")
ALLERGY_LABEL.grid(row=2, column=0)
ALLERGY_CHECK.grid(row=3, column=0)

# List Allergies
ALLERGIES_LABEL = tkinter.Label(BASIC_INFO_FRAME, text="List Allergies (separate by commas)")
ALLERGIES_TEXT = tkinter.Text(BASIC_INFO_FRAME, width=5, height=2)
ALLERGIES_LABEL.grid(row=2, column=1)
ALLERGIES_TEXT.grid(row=3, column=1, sticky="ew", padx=5)

for WIDGET in BASIC_INFO_FRAME.winfo_children():
    WIDGET.grid_configure(padx=10, pady=10)

# Saving Preferences
PREFERENCES_FRAME = tkinter.LabelFrame(FRAME, text="Preferences")
PREFERENCES_FRAME.grid(row=1, column=0, sticky="news", padx=20, pady=10)

# Diet
DIET_LABEL = tkinter.Label(PREFERENCES_FRAME, text="Diet (Optional)")
DIET_LABEL.grid(row=0, column=0)
DIET_FRAME = tkinter.Frame(PREFERENCES_FRAME)
DIET_FRAME.grid(row=1, column=0)

DIET_SCROLLBAR = tkinter.Scrollbar(DIET_FRAME, orient=tkinter.VERTICAL)
DIET_LISTBOX = tkinter.Listbox(DIET_FRAME, selectmode="multiple", yscrollcommand=DIET_SCROLLBAR.set, exportselection=0)
DIET_LIST = ["Vegetarian", "Vegan", "Pescetarian", "Dairy-Free", "Gluten-Free", "Lactose-Free", "Low-Cholesterol",
             "Halal", "Kosher", "Keto", "Paleo"]
for DIET_ITEM in DIET_LIST:
    DIET_LISTBOX.insert(tkinter.END, DIET_ITEM)

DIET_LISTBOX.grid(row=0, column=0, sticky="nsew")
DIET_SCROLLBAR.config(command=DIET_LISTBOX.yview)
DIET_SCROLLBAR.grid(row=0, column=1, sticky="ns")

PREFERENCES_FRAME.columnconfigure(0, weight=1)
PREFERENCES_FRAME.rowconfigure(1, weight=1)

# Cuisine
CUISINE_LABEL = tkinter.Label(PREFERENCES_FRAME, text="Cuisine (Optional)")
CUISINE_LABEL.grid(row=0, column=1)
CUISINE_FRAME = tkinter.Frame(PREFERENCES_FRAME)
CUISINE_FRAME.grid(row=1, column=1)

CUISINE_SCROLLBAR = tkinter.Scrollbar(CUISINE_FRAME, orient=tkinter.VERTICAL)
CUISINE_LISTBOX = tkinter.Listbox(CUISINE_FRAME, selectmode="multiple", yscrollcommand=CUISINE_SCROLLBAR.set,
                                  exportselection=0)
CUISINE_LIST = ["African", "American", "Chinese", "French", "Greek", "Indian", "Italian", "Japanese", "Korean",
                "Mexican", "Middle-Eastern", "Spanish", "Thai", "Vietnamese"]
for CUISINE_ITEM in CUISINE_LIST:
    CUISINE_LISTBOX.insert(tkinter.END, CUISINE_ITEM)

CUISINE_LISTBOX.grid(row=0, column=0, sticky="nsew")
CUISINE_SCROLLBAR.config(command=CUISINE_LISTBOX.yview)
CUISINE_SCROLLBAR.grid(row=0, column=1, sticky="ns")

PREFERENCES_FRAME.columnconfigure(1, weight=1)
PREFERENCES_FRAME.rowconfigure(1, weight=1)

# Food
FOOD_LABEL = tkinter.Label(PREFERENCES_FRAME, text="Food (separate by commas)")
FOOD_TEXT = tkinter.Text(PREFERENCES_FRAME, width=5, height=10)
FOOD_LABEL.grid(row=0, column=2)
FOOD_TEXT.grid(row=1, column=2, sticky="ew", padx=5)

# Type of Dish
DISH_LABEL = tkinter.Label(PREFERENCES_FRAME, text="*Type of Dish")
DISH_LABEL.grid(row=2, column=0)
DISH_FRAME = tkinter.Frame(PREFERENCES_FRAME)
DISH_FRAME.grid(row=3, column=0)

# dish_scrollbar = tkinter.Scrollbar(DISH_FRAME, orient=tkinter.VERTICAL)
DISH_LISTBOX = tkinter.Listbox(DISH_FRAME, selectmode="single", exportselection=0, width=23, height=4)
DISH_LIST = ["Main Dish", "Side Dish", "Dessert", "Other"]
for DISH_ITEM in DISH_LIST:
    DISH_LISTBOX.insert(tkinter.END, DISH_ITEM)

DISH_LISTBOX.grid(row=0, column=0, sticky="nsew")
# dish_scrollbar.config(command=DISH_LISTBOX.yview)
# dish_scrollbar.grid(row=0, column=1, sticky="ns")

# PREFERENCES_FRAME.columnconfigure(2, weight=1)
# PREFERENCES_FRAME.rowconfigure(3, weight=1)

# Other
OTHER_LABEL = tkinter.Label(PREFERENCES_FRAME, text="Other (separate by commas)")
OTHER_TEXT = tkinter.Text(PREFERENCES_FRAME, width=5, height=3)
OTHER_LABEL.grid(row=2, column=1)
OTHER_TEXT.grid(row=3, column=1, sticky="ew", padx=5)

for WIDGET in PREFERENCES_FRAME.winfo_children():
    WIDGET.grid_configure(padx=10, pady=10)

# Submit Button
BUTTON = tkinter.Button(FRAME, text="Submit", command=enter_data)
BUTTON.grid(row=2, column=0, sticky="news", padx=20, pady=10)

# Clear Button
CLEAR_BUTTON = tkinter.Button(FRAME, text="Clear", command=clear_form)
CLEAR_BUTTON.grid(row=3, column=0, sticky="news", padx=20, pady=10)

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all('form.py', config={
        'max-line-length': 120,
        'extra-imports': ['tkinter', 'tree', 'gui'],
        'allowed-io': []
    })
