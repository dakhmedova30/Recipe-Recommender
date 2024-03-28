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
    def __init__(self, master, recipes: list[recipes.Recipe], **kwargs) -> None:
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

    num_recipes = len(recipes)

    # add widgets on tabs
    for i in range(1, num_recipes + 1):
        # load the string representation of the recipe
        txt = str(recipes[i - 1])

        # load the radar chart
        recipes[i - 1].create_radar_chart("fig")
        img = ctk.CTkImage(Image.open("fig.png"), size=(700, 500))

        self.textbox = ctk.CTkTextbox(master=self.tab(f"Recipe {i}"), width=400, corner_radius=0,
                                      fg_color="transparent")
        self.textbox.grid(row=0, column=0, sticky="nsew")
        self.textbox.insert("0.0", txt)
        self.label_img = ctk.CTkLabel(master=self.tab(f"Recipe {i}"), image=img, text="")
        self.label_img.grid(row=1, column=0, padx=20, pady=10)

    for i in range(num_recipes + 1, 6):
        self.textbox = ctk.CTkTextbox(master=self.tab(f"Recipe {i}"), width=400, corner_radius=0,
                                      fg_color="transparent")
        self.textbox.grid(row=0, column=0, sticky="nsew")
        self.textbox.insert("0.0", "Not enough recipes fit the criteria.")

if __name__ == "__main__":
    # TODO: remove placeholder data
    placeholder_data = [recipes.r1 for _ in range(3)]  # example where there are only three recipes


    app = App()
    app.mainloop()
