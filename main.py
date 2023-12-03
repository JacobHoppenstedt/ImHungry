from recipe import Recipe
from cookbook import CookBook
import PySimpleGUI as sg           
from PIL import Image, ImageTk
from io import BytesIO
import requests
import bs4
import requests
import bs4
from icrawler.builtin import GoogleImageCrawler, GoogleFeeder, GoogleParser
from customlinkprinter import CustomLinkPrinter
import requests
rating_images = {
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
    font = ()
    print(f"Debug: Received file_urls in create_popup: {file_urls}")
    layout = [
        [sg.Text(item, justification='center', size=(400, 2))],
        [sg.Listbox(cookbook.get_recipe(item), size=(100, 20))],
        [sg.Text(cookbook.get_recipe_time(item), justification='center', size=(400, 2))],

        [sg.Image(key='_RECIPE_IMAGE_', size=(200, 150), pad=((125, 25), (20, 20)))],
        [sg.Image(key='_RATING_IMAGE_', size=(200, 150), pad=((125, 25), (20, 20)))],

        [sg.Button('OK')]
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
        print(f"Debug: Using file_url in create_popup: {file_urls[0]}")
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

    window.close()

def open_search_type(type):
    sorted_rating = False
    sorted_time = False
    if type=='Meal Name':
        layout = [
            [sg.Text("Search for a meal...", size=(400, 1))],
            [sg.Input(do_not_clear=True, size=(40, 2), enable_events=True, key='_INPUT_')],
            [sg.Button('Sort by Rating', size=(20, 2), key='_SORT_BY_RATING_')],
            [sg.Button('Sort by Time', size=(20, 2), key='_SORT_BY_TIME_')],
            [sg.Listbox(meal_names, size=(400, 400), enable_events=True, key='_LIST_')],
        ]
        tab_window = sg.Window(f'Search by {type}', layout, size=(800, 800), background_color='#F6F3E7')
        while True:
            event, values = tab_window.read()

            if event in (sg.WIN_CLOSED, 'OK'):
                break
            if values['_INPUT_'] != '':
                search_by_name(values['_INPUT_'], cookbook, tab_window)
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
                sort_by_rating(cookbook, tab_window, layout)
                sorted_rating = True
            if event == '_SORT_BY_TIME_':
                sort_by_time(cookbook, tab_window, layout)
                sorted_time = True

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
            [sg.Listbox([], size=(400, 400), enable_events=True, key='_INGREDIENT_LIST_')],
        ]
        tab_window = sg.Window(f'Search by {type}', layout, size=(800, 800), background_color='#F6F3E7')
        while True:
            event, values = tab_window.read()

            if event in (sg.WIN_CLOSED, 'OK'):
                break
            if values['_INGREDIENT_INPUT_'] != '':
                search_by_ingredients(values['_INGREDIENT_INPUT_'], cookbook, tab_window)
            else:
                tab_window.Element('_INGREDIENT_LIST_').Update([])

            if event == '_LIST_' and len(values['_LIST_']):
                selected_item = values['_LIST_'][0]
                create_popup(selected_item, cookbook, crawl_image(selected_item + 'food or drink'))
            if event == '_INGREDIENT_LIST_' and len(values['_INGREDIENT_LIST_']):
                selected_item = values['_INGREDIENT_LIST_'][0]
                create_popup(selected_item, cookbook, crawl_image(selected_item + 'food or drink'))
            if event == 'Back':
                break

        tab_window.close()
    
    

def search_by_name(search, cookbook, window):
    new_values = [x for x in meal_names if search.lower() in x.lower()]
    window.Element('_LIST_').Update(new_values)

def search_by_ingredients(search_ingredient, cookbook, window):
    search_ingredient = search_ingredient.lower()
    ingredient_results = cookbook.search_by_ingredients(search_ingredient)
    window.Element('_INGREDIENT_LIST_').Update(ingredient_results)

def sort_by_rating(cookbook, window, current_tab_layout):
    cookbook.mergesort_by_rating()
    updated_meal_names = [recipe.name for recipe in cookbook.recipe_list]
    updated_meal_names.reverse()
    window.Element('_LIST_').Update(updated_meal_names)

def sort_by_time(cookbook, window, current_tab_layout):
    cookbook.quicksort_by_time()
    cookbook.recipe_list = cookbook.recipe_list[5262:] + cookbook.recipe_list[:5262]
    updated_meal_names = [recipe.name for recipe in cookbook.recipe_list]
    window.Element('_LIST_').Update(updated_meal_names)

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

    google_crawler = GoogleImageCrawler(**init_params)
    google_crawler.downloader.file_urls = []
    google_crawler.crawl(keyword=recipe_name, **params)
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

init_params = {
    'feeder_cls': GoogleFeeder,
    'parser_cls': GoogleParser,
    'downloader_cls': CustomLinkPrinter, 
    }
keyword = "your_search_keyword"
params = {
    'filters': None,
    'offset': 0,
    'max_num': 100,
    'min_size': None,
    'max_size': None,
    'language': 'en',  
    'file_idx_offset': 0,
    'overwrite': False,
    }
sorted = False
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