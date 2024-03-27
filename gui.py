"""CSC111 Winter 2024 Project 2
TODO: add description and copyright
"""
import customtkinter as ctk
from PIL import Image
import recipes

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class App(ctk.CTk):
    """An app that recommends recipes to users.

    Instance Attributes:
        - self.generate_button: a button that displays the recipes in a new window when clicked
        - self.tab_window: an additional window to display the recipes
        - TODO
    """
    def __init__(self) -> None:
        super().__init__()

        # TODO: add questionnaire GUI

        self.generate_button = ctk.CTkButton(self, text="Generate Recipes", command=self.open_tab_window)
        self.generate_button.pack(side="top", padx=20, pady=20)

        self.tab_window = None

    def open_tab_window(self):
        """Opens a new tab window with a tabview.
        """
        if self.tab_window is None or not self.tab_window.winfo_exists():
            self.tab_window = TabWindow(self)  # create window if its None or destroyed
            # TODO: pass in recipe data
            tab_view = TabView(master=self.tab_window, recipes=placeholder_data)
            tab_view.pack(side="top", padx=20, pady=20)
        else:
            self.tab_window.focus()  # if window exists focus it


class TabWindow(ctk.CTkToplevel):
    """An additional window to display the tabview.

    Instance Attributes:
        - label: The label containing the text in the window
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.label = ctk.CTkLabel(self, text="Recipe Recommendations", font=("TkDefaultFont", 30))
        self.label.pack(padx=20, pady=20)


class TabView(ctk.CTkTabview):
    """A tabview with 5 tabs, one for each recipe.

    Instance Attributes:
        - label: The label containing the data of the recipe
        - label_img: The label containing the image of the spider chart for the recipe
    """
    def __init__(self, master, recipes: list[tuple[str, str]], **kwargs) -> None:
        """Initialize a tabview with 5 tabs using the given recipe data.

        Preconditions:
            - len(recipes) == 5
            - all(len(recipe) == 2 for recipe in recipes)
            - For each tuple in recipes, the first element contains the data of the recipe and the second element
            contains the path to an image
        """
        super().__init__(master, **kwargs)

        # create tabs
        for i in range(1, 6):
            self.add(f"Recipe {i}")

        # load images
        images = []
        for recipe in recipes:
            images.append(ctk.CTkImage(Image.open(recipe[1]), size=(640, 480)))
        # TODO: change image size depending on size of radar chart from plotly

        # add widgets on tabs
        for i in range(1, 6):
            self.label = ctk.CTkLabel(master=self.tab(f"Recipe {i}"), text=recipes[i - 1][0], justify='left', text_color='#FFCC70')
            self.label.grid(row=0, column=0, padx=20, pady=10)
            self.label_img = ctk.CTkLabel(master=self.tab(f"Recipe {i}"), image=images[i - 1], text='')
            self.label_img.grid(row=1, column=0, padx=20, pady=10)


if __name__ == "__main__":
    # TODO: use actual recipe data
    # placeholder recipe
    recipe_list = ['combine beans , onion , chilies , 1 / 2 teaspoon cumin , garlic powder and broth in crock pot',
                   'cook on low 8 hours or on high 4 hours',
                   'stir in cilantro , olive oil and remaining 1 / 2 teaspoon cumin',
                   'garnish with sour cream , if desired']
    steps = ''
    step_n = 1
    for step in recipe_list:
        new = step.replace(" , ", ", ")
        steps += f"{step_n}. {new.capitalize()}\n"
        step_n += 1

    placeholder_recipe = (f"arriba baked winter squash mexican style\n {steps}", "test_image.jpeg")
    placeholder_data = [placeholder_recipe for _ in range(5)]
    # For each tuple in placeholder_data, the first element contains the data of the recipe and the second element
    #         contains the path to an image

    app = App()
    app.mainloop()
