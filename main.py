from recipe import Recipe
from cookbook import CookBook
import PySimpleGUI as sg           

# Example usage:
csv_file_path = "food_recipes.csv"  # Replace with the actual path to your CSV file
cookbook = CookBook(csv_file_path)

# Example: Accessing recipes
dish = "Golden Crescent Rolls"
recipe = cookbook.get_recipe(dish)
print(f"Recipe for {dish}: {recipe}")

# Sorting by time
cookbook.quicksort_by_time()
# After sorting
# print("\nAfter sorting:")
cookbook.recipe_list = cookbook.recipe_list[5261:] + cookbook.recipe_list[:5261]
for recipe in range(0, 100):
    print(cookbook.recipe_list[recipe].name, cookbook.recipe_list[recipe].time)
    

#populate recipe names into list
meal_names = []
for recipe in range(0, 10000):
    meal_names.append(cookbook.recipe_list[recipe].name)

#shows selected recipe/ingredients/photo of the meal
def create_popup(item):
    layout = [
        [sg.Text(item, justification='center', size=(200, 1))],
        [sg.Listbox(cookbook.get_recipe(item), size=(50, 10))],
        [sg.Text(cookbook.get_recipe_time(item), justification='center', size=(200, 1))],
        [sg.Button('OK')]
    ]

    window = sg.Window(item, layout, size=(400, 400), finalize=True)

    # Event loop for the popup window
    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'OK'):
            break

    window.close()



# Define the window's contents
layout = [[sg.Text("Search for a meal...")],
          [sg.Input(do_not_clear=True, size=(20,1),enable_events=True, key='_INPUT_')],
          [sg.Listbox(meal_names, size=(200,200), enable_events=True, key='_LIST_')],
          [sg.Button('Ok'), sg.Button('Quit')]]


window = sg.Window('I\'m Hungry...', layout, size=(400, 400))
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    if values['_INPUT_'] != '':
        search = values['_INPUT_']
        new_values = [x for x in meal_names if search.lower() in x.lower()]  # do the filtering  
        window.Element('_LIST_').Update(new_values)
    else:
        window.Element('_LIST_').Update(meal_names)          # display original unfiltered list
    if event == '_LIST_' and len(values['_LIST_']):     # if a list item is chosen
        selected_item = values['_LIST_'][0]
        create_popup(selected_item)

window.close()

