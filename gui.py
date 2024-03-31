"""CSC111 Winter 2024 Project 2

Module Description
==================
This module contains the App, TabWindow, and TabView classes to display the GUI for the
recipe recommender.

Copyright and Usage Information
===============================
This file is Copyright (c) 2024 Akanksha Anand Iyengar, Leilia Ho, Diana Akhmedova, Herena Li
"""
import customtkinter as ctk
from PIL import Image
import recipes

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("dark-blue")


class TabWindow(ctk.CTkToplevel):
    """An additional window to display the tabview.

    Instance Attributes:
        - label: The label containing the text in the window
    """
    label: ctk.CTkLabel

    def __init__(self, recipe_data: list[recipes.Recipe], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.label = ctk.CTkLabel(self, text="Recipe Recommendations", font=("TkDefaultFont", 30))
        self.label.pack(padx=20, pady=20)

        tab_view = TabView(master=self, recipes_list=recipe_data)
        tab_view.pack(side="top", padx=20, pady=20)


class TabView(ctk.CTkTabview):
    """A tabview with 5 tabs, one for each recipe.

    Instance Attributes:
        - textbox: The textbox containing the data of the recipe
        - label_img: The label containing the image of the spider chart for the recipe
    """
    textbox: ctk.CTkTextbox
    label_img: ctk.CTkLabel

    def __init__(self, master: ctk.CTkToplevel, recipes_list: list[recipes.Recipe], **kwargs) -> None:
        """Initialize a tabview with 5 tabs using the given recipe data.

        Preconditions:
            - len(recipes) <= 5
            - all(len(recipe) == 2 for recipe in recipes)
            - For each tuple in recipes, the first element contains the data of the recipe and the second element
            contains the path to an image
        """
        super().__init__(master, **kwargs)

        # create tabs
        for i in range(1, 6):
            self.add(f"Recipe {i}")

        num_recipes = len(recipes_list)

        # add widgets on tabs
        for i in range(1, num_recipes + 1):
            # load the string representation of the recipe
            txt = str(recipes_list[i - 1])

            # load the radar chart
            recipes_list[i - 1].create_radar_chart("fig")
            img = ctk.CTkImage(Image.open("fig.png"), size=(590, 370))

            self.textbox = ctk.CTkTextbox(master=self.tab(f"Recipe {i}"), width=400, corner_radius=0,
                                          fg_color="transparent", wrap="word")
            self.textbox.grid(row=0, column=0, sticky="nsew")
            self.textbox.insert("0.0", txt)
            self.label_img = ctk.CTkLabel(master=self.tab(f"Recipe {i}"), image=img, text="")
            self.label_img.grid(row=1, column=0, padx=20, pady=10)

        for i in range(num_recipes + 1, 6):
            self.textbox = ctk.CTkTextbox(master=self.tab(f"Recipe {i}"), width=400, corner_radius=0,
                                          fg_color="transparent")
            self.textbox.grid(row=0, column=0, sticky="nsew")
            self.textbox.insert("0.0", "Not enough recipes fit the criteria.")


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all('gui.py', config={
        'max-line-length': 120,
        'extra-imports': ['customtkinter', 'PIL', 'recipes'],
        'allowed-io': []
    })
