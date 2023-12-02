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
print("\nAfter sorting:")
for recipe in cookbook.recipe_list:
    print(recipe.name, recipe.time)

def create_popup(item):
    # Define the layout of the popup window
    layout = [
        [sg.Text(item, justification='center', size=(200, 1))],
        [sg.Button('OK')]
    ]

    # Create the popup window
    window = sg.Window('Popup', layout, size=(200, 200), finalize=True)

    # Event loop for the popup window
    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'OK'):
            break

    window.close()


names = ['Roberta', 'Kylie', 'Jenny', 'Helen',
        'Andrea', 'Meredith','Deborah','Pauline',
        'Belinda', 'Wendy']

# Define the window's contents
layout = [[sg.Text("Search for a meal...")],
          [sg.Input(do_not_clear=True, size=(20,1),enable_events=True, key='_INPUT_')],
          [sg.Listbox(names, size=(200,200), enable_events=True, key='_LIST_')],
          [sg.Button('Ok'), sg.Button('Quit')]]


window = sg.Window('I\'m Hungry...', layout, size=(400, 400))
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    if values['_INPUT_'] != '':
        search = values['_INPUT_']
        new_values = [x for x in names if search in x]  # do the filtering
        window.Element('_LIST_').Update(new_values)
    else:
        window.Element('_LIST_').Update(names)          # display original unfiltered list
    if event == '_LIST_' and len(values['_LIST_']):     # if a list item is chosen
        selected_item = values['_LIST_'][0]
        create_popup(selected_item)

window.close()