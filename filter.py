"""CSC111 Winter 2024 Project 2

Module Description
==================
This module contains the code to filter the recipes

Copyright and Usage Information
===============================
This file is Copyright (c) 2024 Akanksha Anand Iyengar, Leilia Ho, Diana Akhmedova, Herena Li
"""

import recipes
from recipes import Recipe
import form
import tree

def filtered_recipes(recipes: list[Recipe], difficulty: str, time_threshold: int, calories: float,
                     allergies: list[str], diet: list[str], cuisines: list[str]) -> list[Recipe]:
    """Filters recipes based on the given criteria.
    
    Parameters:
    - recipes: List of Recipe objects to filter.
    - difficulty: Difficulty level by number of steps.
    - time: Time taken.
    - calories: Number of calories.
    - allergies: List of allergens.
    - diet: List of dietary preferences.
    - cuisine: List of preferred cuisines.
    
    It returns a list of filtered Recipe objects based on the criteria."""

    filtered_recipes = []
    for recipe in recipes:
        if (recipe.steps == difficulty and recipe.cooking_time <= time_threshold and recipe.calories <= calories and 
            not any(allergy.lower() in recipe.ingredients.lower() for allergy in allergies) and 
            all(pref.lower() in recipe.diet.lower() for pref in diet) and 
            any(cuisine.lower() in recipe.cuisine.lower() for cuisine in cuisines)):
            filtered_recipes.append(recipe)

    return filtered_recipes