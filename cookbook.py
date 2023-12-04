from recipe import Recipe
import csv

class CookBook:
    def __init__(self, csv_file): # Cookbook constructor
        self.recipe_list = []
        self.load_from_csv(csv_file)

    def load_from_csv(self, csv_file): # loads in data from csv file into Recipe objects
        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                name, time, rating, *ingredients = row
                ingredients_list = [ingredient.strip() for ingredient in " ".join(ingredients).split('//')]
                recipe = Recipe(name, time, rating, ingredients_list)
                self.add_entry(recipe)


    def add_entry(self, recipe): # adds to the recipe list
        self.recipe_list.append(recipe)

    def search_by_ingredients(self, search_ingredients):
            # Split the input string into a list of ingredients
            ingredients_list = [ingredient.strip().lower() for ingredient in search_ingredients.split(',')]

            # Filter recipes that contain all specified ingredients
            matching_recipes = [recipe.name for recipe in self.recipe_list if all(ingredient in recipe.ingredients for ingredient in ingredients_list)]

            return matching_recipes

    def get_recipe_rating(self, dish_name): # gets the rating of a recipe
        for recipe in self.recipe_list: # traverses recipe list
            if recipe.name == dish_name: # if the recipe name matches the dish name
                return recipe.rating # return the rating
        return "Rating not found"

    def get_recipe(self, dish_name): # gets the recipe
        for recipe in self.recipe_list: # traverses recipe list
            if recipe.name == dish_name: # if the recipe name matches the dish name
                return recipe.getIngredients() # return the ingredients
        return "Recipe not found"
    
    def get_recipe_time(self, dish_name): # same premise as above functions
        for recipe in self.recipe_list:
            if recipe.name == dish_name:
                return recipe.time

    def search_recipes_by_ingredients(self, query_ingredients):
        recipes_after_search = [recipe for recipe in self.recipe_list if all(ingredient in recipe.ingredients for ingredient in query_ingredients)]
        return recipes_after_search

    def quicksort_by_time(self): # quicksort helper function
            self.recipe_list = self._quicksort_by_time(self.recipe_list)

    def _quicksort_by_time(self, recipes):
        if len(recipes) <= 1: # base case
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


    def mergesort_by_rating(self): # merge sort helper function
        self.recipe_list = self._mergesort_by_rating(self.recipe_list)

    def _mergesort_by_rating(self, recipes):        
        if len(recipes) <= 1: # base case
            return recipes

        mid = len(recipes) // 2 # split the list in half
        left_half = recipes[:mid] # left half
        right_half = recipes[mid:] # right half

        left_half = self._mergesort_by_rating(left_half) # recursively sort the left half
        right_half = self._mergesort_by_rating(right_half) # recursively sort the right half

        return self._merge_by_rating(left_half, right_half) # merge the two halves

    def _merge_by_rating(self, left, right):
        result = [] # result list
        i = j = 0 # left and right index

        while i < len(left) and j < len(right): # while left and right index are less than their respective lengths
            if left[i].rating <= right[j].rating: # if left rating is less than or equal to the right rating
                result.append(left[i]) # add left rating to the result list
                i += 1 # increment left index
            else: # if right rating is greater than the left rating
                result.append(right[j]) # add right rating to the result list
                j += 1 # increment right index

        result.extend(left[i:]) # add rest of left list to result list
        result.extend(right[j:]) # add rest of right list to result list
        return result