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
                name, time, rating, *ingredients = row
                ingredients_list = [ingredient.strip() for ingredient in " ".join(ingredients).split('//')]
                recipe = Recipe(name, time, rating, ingredients_list)
                self.add_entry(recipe)


    def add_entry(self, recipe):
        self.recipe_list.append(recipe)

    def get_recipe(self, dish_name):
        for recipe in self.recipe_list:
            if recipe.name == dish_name:
                return recipe.getIngredients()
        return "Recipe not found"


    def quicksort_by_time(self):
            self.recipe_list = self._quicksort_by_time(self.recipe_list)

    def _quicksort_by_time(self, recipes):
        if len(recipes) <= 1:
            return recipes

        # Use the first recipe as the pivot
        pivot_recipe = recipes[0]
        pivot_time = pivot_recipe.time_in_minutes()

        # Skip recipes with 'N/A' when comparing times
        less = [recipe for recipe in recipes[1:] if recipe.time_in_minutes() < pivot_time]
        equal = [recipe for recipe in recipes[1:] if recipe.time_in_minutes() == pivot_time]
        greater = [recipe for recipe in recipes[1:] if recipe.time_in_minutes() > pivot_time]
        na_recipes = [recipe for recipe in recipes[1:] if recipe.time_in_minutes() == float('inf')]

        # Recursively apply quicksort to less and greater portions
        sorted_recipes = self._quicksort_by_time(less) + [pivot_recipe] + equal + self._quicksort_by_time(greater) + na_recipes
        return sorted_recipes

