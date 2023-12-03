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

    def search_by_ingredients(self, search_ingredient):
        results = []
        for recipe in self.recipe_list:
            if any(search_ingredient.lower() in ingredient.lower() for ingredient in recipe.ingredients):
                results.append(recipe.name)
        return results


    def get_recipe(self, dish_name):
        for recipe in self.recipe_list:
            if recipe.name == dish_name:
                return recipe.getIngredients()
        return "Recipe not found"
    
    def get_recipe_time(self, dish_name):
        for recipe in self.recipe_list:
            if recipe.name == dish_name:
                return recipe.time

    def search_recipes_by_ingredients(self, query_ingredients):
        recipes_after_search = [recipe for recipe in self.recipe_list if all(ingredient in recipe.ingredients for ingredient in query_ingredients)]
        return recipes_after_search

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


    def mergesort_by_rating(self):
        self.recipe_list = self._mergesort_by_rating(self.recipe_list)

    def _mergesort_by_rating(self, recipes):        
        if len(recipes) <= 1:
            return recipes

        mid = len(recipes) // 2
        left_half = recipes[:mid]
        right_half = recipes[mid:]

        left_half = self._mergesort_by_rating(left_half)
        right_half = self._mergesort_by_rating(right_half)

        return self._merge_by_rating(left_half, right_half)

    def _merge_by_rating(self, left, right):
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i].rating <= right[j].rating:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result

    
    def heapify(self, arr, n, i, key_func):
        largest = i
        left_child = 2 * i + 1
        right_child = 2 * i + 2

        if left_child < n and (key_func(arr[i]) < key_func(arr[left_child]) or (key_func(arr[i]) == key_func(arr[left_child]) and arr[i].time == 'N/A')):
            largest = left_child

        if right_child < n and (key_func(arr[largest]) < key_func(arr[right_child]) or (key_func(arr[largest]) == key_func(arr[right_child]) and arr[largest].time == 'N/A')):
            largest = right_child

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            self.heapify(arr, n, largest, key_func)


    def heap_sort_by_time(self):
        key_func = lambda recipe: (recipe.time_in_minutes(), recipe.time == 'N/A')

        n = len(self.recipe_list)

        # Build a max heap
        for i in range(n // 2 - 1, -1, -1):
            self.heapify(self.recipe_list, n, i, key_func)

        # Extract elements one by one
        for i in range(n - 1, 0, -1):
            self.recipe_list[i], self.recipe_list[0] = self.recipe_list[0], self.recipe_list[i]
            self.heapify(self.recipe_list, i, 0, key_func)