from cookbook import CookBook
import PySimpleGUI as sg           
from PIL import Image
from io import BytesIO
import requests
import webbrowser
from icrawler.builtin import GoogleImageCrawler, GoogleFeeder, GoogleParser
from customlinkprinter import CustomLinkPrinter
import requests

rating_images = { # dictionary of rating images
    (4.5, 5.0): "images/Star_rating_5_of_5.png",
    (4.0, 4.5): "images/Star_rating_4.5_of_5.png",
    (3.5, 4.0): "images/Star_rating_4_of_5.png",
    (3.0, 3.5): "images/Star_rating_3.5_of_5.png",
    (2.5, 3.0): "images/Star_rating_3_of_5.png",
    (2.0, 2.5): "images/Star_rating_2.5_of_5.png",
    (1.5, 2.0): "images/Star_rating_2_of_5.png",
    (1.0, 1.5): "images/Star_rating_1.5_of_5.png",
    (0.5, 1.0): "images/Star_rating_1_of_5.png",
    (0.0, 0.5): "images/Star_rating_0.5_of_5.png",
}

def create_popup(item, cookbook, file_urls):
    text = item.replace(' ', '+')
    url = 'https://google.com/search?q=' + text + '+recipe'
    font = ('Arial', 16, 'underline')
    print(f"Debug: Received file_urls in create_popup: {file_urls}")
    layout = [
        [sg.Text(item, font=('Arial', 18, 'italic'), justification='center', size=(400, 2), pad=((0, 0), (10, 20)))],
        [sg.Listbox(cookbook.get_recipe(item), size=(100, 20), pad=((0, 0), (0, 20)))],
        [
            sg.Text(f'Time to cook: {cookbook.get_recipe_time(item)}', font=('Arial', 14), justification='center', size=(400, 2), pad=((0, 0), (0, 20))),
        ],
        [
            sg.Column(
                layout=[
                    [sg.Text('Link to Recipe', tooltip=url, enable_events=True, font=('Arial', 16, 'underline', 'bold'), key='_URL_')],
                    [sg.Image(key='_RATING_IMAGE_', size=(200, 150), pad=((0, 0), (30, 0)))],  # Adjusted the padding here
                ],
                justification='center',
                element_justification='center',
                pad=((50, 50), 0)  # Padding between columns
            ),
            sg.Column(
                layout=[
                    [sg.Image(key='_RECIPE_IMAGE_', size=(200, 150))],
                ],
                justification='center',
                element_justification='center',
                pad=((50, 50), 0)  # Padding between columns
            ),
        ],
    ]



    window = sg.Window(item, layout, size=(800, 800), finalize=True)
    recipe_rating = float(cookbook.get_recipe_rating(item))

    rating_image_path = None
    for rating_range, path in rating_images.items():
        if rating_range[0] <= recipe_rating <= rating_range[1]:
            rating_image_path = path
            break

    if rating_image_path:
        # Load the image and update the Image element
        rating_image = Image.open(rating_image_path)
        resized_rating_image = rating_image.resize((250, 50))
        rating_bio = BytesIO()
        resized_rating_image.save(rating_bio, format="PNG")
        rating_image_data = rating_bio.getvalue()
        window['_RATING_IMAGE_'].update(data=rating_image_data)
    if file_urls:
        recipe_image_url = file_urls[0]
        try:
            response = requests.get(recipe_image_url)
            recipe_image = Image.open(BytesIO(response.content))
            resized_recipe_image = recipe_image.resize((200, 200))
            recipe_bio = BytesIO()
            resized_recipe_image.save(recipe_bio, format="PNG")
            recipe_image_data = recipe_bio.getvalue()
            window['_RECIPE_IMAGE_'].update(data=recipe_image_data)
        except Exception as e:
            print(f"Error loading recipe image: {e}")

    # Event loop for the popup window
    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'OK'):
            break
        if event == '_URL_':
            webbrowser.open(url)

    window.close()

def open_search_type(type):
    sorted_rating = False
    sorted_time = False
    if type=='Meal Name':
        layout = [
            [sg.Text("Search for a meal...", size=(400, 1))],
            [sg.Input(do_not_clear=True, size=(40, 2), enable_events=True, key='_INPUT_')],
            [sg.Button('Sort by Rating ↓', size=(20, 2), key='_SORT_BY_RATING_')],
            [sg.Button('Sort by Time ↑', size=(20, 2), key='_SORT_BY_TIME_')],
            [sg.Listbox(meal_names, size=(400, 400), enable_events=True, key='_LIST_')],
        ]
        tab_window = sg.Window(f'Search by {type}', layout, size=(800, 800), background_color='#F6F3E7')
        while True:
            event, values = tab_window.read()

            if event in (sg.WIN_CLOSED, 'OK'):
                break
            if values['_INPUT_'] != '':
                if sorted_time:
                    search_by_name(values['_INPUT_'], cookbook, tab_window, time_sorted_meal_names)
                elif sorted_rating:
                    search_by_name(values['_INPUT_'], cookbook, tab_window, rating_sorted_meal_names)
                else:
                    search_by_name(values['_INPUT_'], cookbook, tab_window, meal_names)
            elif values['_INPUT_'] == '':
                if sorted_rating:
                    sort_by_rating(cookbook, tab_window, layout)
                else:
                    tab_window.Element('_LIST_').Update(meal_names)
                if sorted_time:
                    sort_by_time(cookbook, tab_window, layout)
                else:
                    tab_window.Element('_LIST_').Update(meal_names)
            if event == '_SORT_BY_RATING_':
                rating_sorted_meal_names = sort_by_rating(cookbook, tab_window, layout)
                tab_window.Element('_LIST_').Update(rating_sorted_meal_names)
                search_by_name(values['_INPUT_'], cookbook, tab_window, rating_sorted_meal_names)
                sorted_rating = True
                sorted_time = False
            if event == '_SORT_BY_TIME_':
                time_sorted_meal_names = sort_by_time(cookbook, tab_window, layout)
                tab_window.Element('_LIST_').Update(time_sorted_meal_names)
                search_by_name(values['_INPUT_'], cookbook, tab_window, time_sorted_meal_names)
                sorted_time = True
                sorted_rating = False

            if event == '_LIST_' and len(values['_LIST_']):
                selected_item = values['_LIST_'][0]
                create_popup(selected_item, cookbook, crawl_image(selected_item + 'food or drink'))
            if event == '_INGREDIENT_LIST_' and len(values['_INGREDIENT_LIST_']):
                selected_item = values['_INGREDIENT_LIST_'][0]
                create_popup(selected_item, cookbook, crawl_image(selected_item + 'food or drink'))
            if event == 'Back':
                break
        tab_window.close()
    elif type=='Ingredients':
        layout = [
            [sg.Text("Search for recipes by ingredients...", size=(400, 1))],
            [sg.Input(do_not_clear=True, size=(40, 2), enable_events=True, key='_INGREDIENT_INPUT_')],
            [sg.Button('Sort by Rating ↓', size=(20, 2), key='_SORT_BY_RATING_')],
            [sg.Button('Sort by Time ↑', size=(20, 2), key='_SORT_BY_TIME_')],
            [sg.Listbox([], size=(400, 400), enable_events=True, key='_INGREDIENT_LIST_')],
        ]
        tab_window = sg.Window(f'Search by {type}', layout, size=(800, 800), background_color='#F6F3E7')
        while True:
            event, values = tab_window.read()

            if event in (sg.WIN_CLOSED, 'OK'):
                break
            if values['_INGREDIENT_INPUT_'] != '' and not sorted_rating and not sorted_time:
                search_by_ingredients(values['_INGREDIENT_INPUT_'], cookbook, tab_window)
            elif values['_INGREDIENT_INPUT_'] == '':
                tab_window.Element('_INGREDIENT_LIST_').Update('')
            if sorted_rating:
                search_by_ingredients(values['_INGREDIENT_INPUT_'], cookbook, tab_window, rating_sorted_meal_names)
            if sorted_time:
                search_by_ingredients(values['_INGREDIENT_INPUT_'], cookbook, tab_window, time_sorted_meal_names)
            if event == '_SORT_BY_RATING_':
                rating_sorted_meal_names = sort_by_rating(cookbook, tab_window, layout)
                tab_window.Element('_INGREDIENT_LIST_').Update(rating_sorted_meal_names)
                search_by_ingredients(values['_INGREDIENT_INPUT_'], cookbook, tab_window, rating_sorted_meal_names)
                sorted_rating = True
                sorted_time = False
            if event == '_SORT_BY_TIME_':
                time_sorted_meal_names = sort_by_time(cookbook, tab_window, layout)
                tab_window.Element('_INGREDIENT_LIST_').Update(time_sorted_meal_names)
                search_by_ingredients(values['_INGREDIENT_INPUT_'], cookbook, tab_window)
                sorted_time = True
                sorted_rating = False
            if event == '_LIST_' and len(values['_LIST_']):
                selected_item = values['_LIST_'][0]
                create_popup(selected_item, cookbook, crawl_image(selected_item + 'food or drink'))
            if event == '_INGREDIENT_LIST_' and len(values['_INGREDIENT_LIST_']):
                selected_item = values['_INGREDIENT_LIST_'][0]
                create_popup(selected_item, cookbook, crawl_image(selected_item + 'food or drink'))
            if event == 'Back':
                break

        tab_window.close()
    
    

def search_by_name(search, cookbook, window, meals): 
    new_values = [x for x in meals if search.lower() in x.lower()] # if recipe name is in recipe_list
    window.Element('_LIST_').Update(new_values) # update the listbox with the new values

def search_by_ingredients(search_ingredients, cookbook, window, sorted_list=None):
    # Split the input string into a list of ingredients
    search_terms = [term.strip().lower() for term in search_ingredients.split(',')]
    
    # Filter recipes that contain any specified ingredient word
    matching_recipes = []
    for recipe in cookbook.recipe_list:
        recipe_ingredients_lower = [ingredient.lower() for ingredient in recipe.ingredients]
        if all(term in ' '.join(recipe_ingredients_lower) for term in search_terms):
            matching_recipes.append(recipe.name)
    if sorted_list:
        cookbook.mergesort_by_rating()
        search_terms = [term.strip().lower() for term in search_ingredients.split(',')]
        # Filter recipes that contain any specified ingredient word
        matching_recipes = []
        for recipe in cookbook.recipe_list:
            recipe_ingredients_lower = [ingredient.lower() for ingredient in recipe.ingredients]
            if all(term in ' '.join(recipe_ingredients_lower) for term in search_terms):
                matching_recipes.append(recipe.name)
        matching_recipes.reverse()
        window.Element('_INGREDIENT_LIST_').Update(matching_recipes)
    else:
        window.Element('_INGREDIENT_LIST_').Update(matching_recipes)
        



def sort_by_rating(cookbook, window, current_tab_layout):
    cookbook.mergesort_by_rating() # sort by rating
    updated_meal_names = [recipe.name for recipe in cookbook.recipe_list] # update recipe names
    updated_meal_names.reverse() # reverse list to sort from highest to lowest
    return updated_meal_names

def sort_by_time(cookbook, window, current_tab_layout):
    cookbook.quicksort_by_time() # sort by time
    cookbook.recipe_list = cookbook.recipe_list[5262:] + cookbook.recipe_list[:5262] # move recipes with 'N/A' to the end
    updated_meal_names = [recipe.name for recipe in cookbook.recipe_list] # update recipe names
    return updated_meal_names
    

def crawl_image(recipe_name):
    # Function to crawl for the image of the specified recipe
    init_params = {
        'feeder_cls': GoogleFeeder,
        'parser_cls': GoogleParser,
        'downloader_cls': CustomLinkPrinter,
    }
    params = {
        'filters': None,
        'offset': 0,
        'max_num': 1,
        'min_size': None,
        'max_size': None,
        'language': 'en',
        'file_idx_offset': 0,
        'overwrite': False,
    }

    # Referenced from https://github.com/hellock/icrawler/issues/73 for obtaining the file URLs
    google_crawler = GoogleImageCrawler(**init_params)
    google_crawler.downloader.file_urls = []
    google_crawler.crawl(keyword=recipe_name, **params)
    print(f"Debug: Retrieved file URLs: {google_crawler.downloader.file_urls}")
    return google_crawler.downloader.file_urls

# Initialize cookbook...
csv_file_path = "food_recipes.csv" 
cookbook = CookBook(csv_file_path)

# Populate recipe names into list
meal_names = [recipe.name for recipe in cookbook.recipe_list]


logo_path = "images/logo.png"
logo_image = Image.open(logo_path)

# Convert the logo image for PySimpleGUI
logo_bio = BytesIO()
logo_image.save(logo_bio, format="PNG")
logo_data = logo_bio.getvalue()
# Define the layout for the initial startup page
startup_layout = [
    [sg.Image(data=logo_data, key='_LOGO_', size=(600, 300), background_color='#F6F3E7')],
    [sg.Button('Search by Recipe', size=(20, 2), pad=((50, 50), (20, 20)))],
    [sg.Button('Search by Ingredient', size=(20, 2), pad=((50, 50), (20, 20)))],
    [sg.Button('Quit', size=(20, 2), pad=((50, 50), (20, 20)))],
]

# Create the initial startup window
startup_window = sg.Window('ImHungry', startup_layout, size=(1200, 700), background_color='#F6F3E7', element_justification='c')

while True:
    
    startup_event, startup_values = startup_window.read()

    if startup_event == sg.WIN_CLOSED or startup_event == 'Quit':
        break
    
    # Open the respective search tab based on the button clicked
    if startup_event == 'Search by Recipe':
        open_search_type('Meal Name')
    if startup_event == 'Search by Ingredient':
        open_search_type('Ingredients')

startup_window.close()