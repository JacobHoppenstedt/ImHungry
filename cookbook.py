from recipe import Recipe
import csv

class CookBook:
    def __init__(self, csv_file):
        self.recipe_list = []
        self.load_from_csv(csv_file)

def load_from_csv(self, csv_file):
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 4: 
                name, time, rating, ingredient_str = row

                # Split ingredients by '//'
                ingredients = [ingredient.strip() for ingredient in ingredient_str.split('//')]

                recipe = Recipe(name, time, rating, ingredients)
                self.add_entry(recipe)
            else:
                print(f"Skipping invalid entry: {row}")


    def add_entry(self, recipe):
        self.recipe_list.append(recipe)

    def get_recipe(self, dish_name):
        for recipe in self.recipe_list:
            if recipe.name == dish_name:
                return recipe
        return "Recipe not found"



# Example usage:
csv_file_path = "food_recipes.csv"  # Replace with the actual path to your CSV file
cookbook = CookBook(csv_file_path)

# Example: Accessing recipes
dish = "Golden Crescent Rolls"
recipe = cookbook.get_recipe(dish)
print(f"Recipe for {dish}: {recipe}")