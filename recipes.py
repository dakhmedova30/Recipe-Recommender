"""CSC111 Winter 2024 Project 2

Module Description
==================
This module contains the Recipe class to represent a recipe from the dataset.

Copyright and Usage Information
===============================
This file is Copyright (c) 2024 Akanksha Anand Iyengar, Leilia Ho, Diana Akhmedova, Herena Li
"""

import plotly.express as px
import pandas as pd
from typing import Optional


class Recipe:
    """
    info for recipe
    """
    name: str
    cooking_time: int
    rating: int
    ingredients: list[str]
    steps: list[str]
    calories: float
    cal_range: tuple[int, int]

    def __init__(self, name: str, cooking_time: int, rating: int, ingredients: list[str], steps: list[str],
                 calories: float, cal_range: Optional[tuple[int, int]] = (0, 0)):
        self.name = name
        self.cooking_time = cooking_time
        self.rating = rating
        self.ingredients = ingredients
        self.steps = steps
        self.calories = calories
        self.cal_range = cal_range  # (min, max) calories out of the 5 recommended

    def __str__(self) -> str:
        """Returns a string representation of the recipe.
        """
        ingredients = ''
        for i in range(len(self.ingredients)):
            if i == 0:
                ingredients += self.ingredients[i]
            else:
                ingredients += ", " + self.ingredients[i]

        steps = ''
        step_n = 1
        for step in self.steps:
            steps += f"{step_n}. {step.capitalize()}\n"
            step_n += 1

        return (f"{self.name.title()}\nCooking Time: {self.cooking_time} minutes\nRating: {self.rating}\n"
                f"Ingredients: {ingredients}\nCalories: {self.calories}\nSteps:\n{steps}")

    def scale(self, category: str) -> int:
        """
        Assigns a value of 1-5 according to the value of the characteristics (for radar chart).
        >>> steps1 = ['heat oven to 250', 'toss lamb with salt and pepper', 'heat 2 tbls oil in dutch oven over medium high heat',\
        'brown lamb on all sides in two batches', 'set aside on plate', 'add onions to dutch oven and saute until softened', 'add garlic and cook an additional 30s', 'stir in flour and cook until lightly colored', 'add stock and deglaze pan', 'add tomatoes and spices and bring to simmer before adding lamb and returing to simmer', 'cover and place in oven until meat is almost tender', 'add chickpeas and return to oven until meat is tender and chicpeas are heated through', 'can be cooled , covered and refrigerated up tp 3 days before reheating on stovetop', 'stir in parsley , discard bay leaves and adjust seasoning just before serving']
        >>> ingredients1 = ['lamb shoulder', 'salt', 'ground black pepper', 'vegetable oil', 'onions', 'garlic cloves', 'flour', 'low sodium chicken broth', 'tomatoes with juice', 'bay leaves', 'ground coriander', 'ground cumin', 'ground cinnamon', 'ground ginger', 'chickpeas', 'fresh parsley']
        >>> r1 = Recipe("lamb stew", 150, 4, ingredients1, steps1, 605.5, (490, 730)) # steps 14, ingredients 16
        >>> r1.scale("cooking time")
        3
        >>> r1.scale("ingredients")
        4
        >>> r1.scale("steps")
        3
        >>> r1.scale("calories")
        4
        """
        match category:
            case "cooking time":
                if self.cooking_time < 30:
                    return 1
                if self.cooking_time < 80:
                    return 2
                if self.cooking_time < 160:
                    return 3
                if self.cooking_time < 240:
                    return 4
                else:
                    return 5
            case "ingredients":
                if len(self.ingredients) < 3:
                    return 1
                if len(self.ingredients) < 8:
                    return 2
                if len(self.ingredients) < 13:
                    return 3
                if len(self.ingredients) < 19:
                    return 4
                else:
                    return 5
            case "steps":
                if len(self.steps) < 5:
                    return 1
                if len(self.steps) < 10:
                    return 2
                if len(self.steps) < 20:
                    return 3
                if len(self.steps) < 30:
                    return 4
                else:
                    return 5
            case "calories":
                if self.cal_range[1] == self.calories:
                    return 5
                else:
                    interval = (self.cal_range[1] - self.cal_range[0]) / 5
                    r = [self.cal_range[0] + n*interval for n in range(0, 5)]
                    for index in range(1, 5):
                        if self.calories < r[index]:
                            return index + 1

    def create_radar_chart(self, image_name: str):
        """
        Generates an image of a radar chart for the recipe
        """
        # df = pd.DataFrame(
        #     {'Recipes': 'recipe1',
        #      'Attributes': ['Rating', 'Cooking Time', 'Complexity', 'No. of Ingredients', 'Calories'],
        #      'Score': [self.rating, self.scale("cooking time"), self.scale("steps"),
        #                self.scale("ingredients"), self.scale("calories")]})
        # fig = px.line_polar(df, r='Score', theta='Attributes', color='Recipes', line_close=True)
        # fig.update_traces(fill='toself')
        # fig.show()
        df = pd.DataFrame(dict(
            r=[self.rating, self.scale("cooking time"), self.scale("steps"),
               self.scale("ingredients"), self.scale("calories")],
            theta=['Rating', 'Cooking Time', 'Complexity', 'No. of Ingredients', 'Calories']))
        fig = px.line_polar(df, r='r', theta='theta', line_close=True, range_r=[0, 5])
        fig.update_traces(fill='toself')
        # fig.show()
        fig.write_image(f"{image_name}.png")


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all('recipes.py', config={
        'max-line-length': 120,
        'extra-imports': ['plotly.express', 'pandas'],
        'allowed-io': []
    })

    s = ['heat oven to 250', 'toss lamb with salt and pepper', 'heat 2 tbls oil in dutch oven over medium high heat',
             'brown lamb on all sides in two batches', 'set aside on plate',
             'add onions to dutch oven and saute until softened', 'add garlic and cook an additional 30s',
             'stir in flour and cook until lightly colored', 'add stock and deglaze pan',
             'add tomatoes and spices and bring to simmer before adding lamb and returing to simmer',
             'cover and place in oven until meat is almost tender',
             'add chickpeas and return to oven until meat is tender and chicpeas are heated through',
             'can be cooled , covered and refrigerated up tp 3 days before reheating on stovetop',
             'stir in parsley , discard bay leaves and adjust seasoning just before serving']

    i = ['lamb shoulder', 'salt', 'ground black pepper', 'vegetable oil', 'onions', 'garlic cloves', 'flour',
                   'low sodium chicken broth', 'tomatoes with juice', 'bay leaves', 'ground coriander', 'ground cumin',
                   'ground cinnamon', 'ground ginger', 'chickpeas', 'fresh parsley']
    r1 = Recipe("lamb stew", 150, 4, i, s, 605.5, (490, 730))  # steps 14, ingredients 16
