"""CSC111 Winter 2024 Project 2

Module Description
==================
This module contains the Recipe class to represent a recipe from the dataset.

Copyright and Usage Information
===============================
This file is Copyright (c) 2024 Akanksha Anand Iyengar, Leilia Ho, Diana Akhmedova, Herena Li
"""
from typing import Optional
import plotly.express as px
import pandas as pd


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
    tags: list[str]
    cal_range: tuple[int, int]

    def __init__(self, name: str, cooking_time: int, rating: int, ingredients: list[str], steps: list[str],
                 calories: float, tags: list[str], cal_range: Optional[tuple[int, int]] = (0, 0)) -> None:
        self.name = name
        self.cooking_time = cooking_time
        self.rating = rating
        self.ingredients = ingredients
        self.steps = steps
        self.calories = calories
        self.tags = tags
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
        >>> steps1 = ['heat oven to 250', 'toss lamb with salt and pepper', 'heat 2 tbls oil in dutch oven',\
         'brown lamb on all sides in two batches', 'set aside on plate',\
        'add onions to dutch oven and saute until softened', 'add garlic and cook an additional 30s',\
         'stir in flour and cook until lightly colored', 'add stock and deglaze pan']
        >>> ingredients1 = ['lamb shoulder', 'salt', 'ground black pepper', 'vegetable oil', 'onions', 'garlic cloves',\
         'flour', 'low sodium chicken broth', 'tomatoes with juice', 'bay leaves', 'ground coriander', \
         'ground cumin', 'ground cinnamon', 'ground ginger', 'chickpeas', 'fresh parsley']
        >>> r1 = Recipe("lamb stew", 150, 4, ingredients1, steps1, 605.5, [], (490, 730)) # steps 14, ingredients 16
        >>> r1.scale("cooking time")
        3
        >>> r1.scale("ingredients")
        4
        >>> r1.scale("steps")
        2
        >>> r1.scale("calories")
        2
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
                    interval = (self.cal_range[1] - self.cal_range[0]) / 4
                    r = [self.cal_range[0] + n * interval for n in range(0, 5)]
                    for index in range(1, 5):
                        if self.calories < r[index]:
                            return index

    def create_radar_chart(self, image_name: str) -> None:
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
        # df = pd.DataFrame(dict(
        #     r=[self.rating, self.scale("cooking time"), self.scale("steps"),
        #        self.scale("ingredients"), self.scale("calories")],
        #     theta=['Rating', 'Cooking Time', 'Complexity', 'No. of Ingredients', 'Calories']))
        df = pd.DataFrame({"r": [self.rating, self.scale('cooking time'), self.scale('steps'),
                                 self.scale('ingredients'), self.scale('calories')],
                           "theta": ['Rating', 'Cooking Time', 'Complexity', 'No. of Ingredients', 'Calories']})

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
