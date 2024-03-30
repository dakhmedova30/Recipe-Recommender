"""CSC111 Winter 2024 Project 2

Module Description
==================
This module contains the code necessary to run the recipe recommender.

Copyright and Usage Information
===============================
This file is Copyright (c) 2024 Akanksha Anand Iyengar, Leilia Ho, Diana Akhmedova, Herena Li
"""
import recipes
import tree
import gui
import form

if __name__ == '__main__':
    recipes = tree.recommend_recipes("filtered_merged.csv")
    recipes = recipes[:5]  # take the first five recipes

    # calculate cal_range
    if len(recipes) > 0:
        max_calories = max([recipe.calories for recipe in recipes])
        min_calories = min([recipe.calories for recipe in recipes])
        for recipe in recipes:
            recipe.cal_range = (min_calories, max_calories)

    # open the tabview
    gui.TabWindow(recipes)
