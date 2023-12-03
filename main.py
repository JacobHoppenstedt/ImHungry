from recipe import Recipe
from cookbook import CookBook
import PySimpleGUI as sg           
from PIL import Image, ImageTk
from io import BytesIO
from icrawler.builtin import GoogleImageCrawler, GoogleFeeder, GoogleParser
from customlinkprinter import CustomLinkPrinter

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
def create_popup(item, cookbook):
    layout = [
        [sg.Text(item, justification='center', size=(400, 2))],
        [sg.Listbox(cookbook.get_recipe(item), size=(100, 20))],
        [sg.Text(cookbook.get_recipe_time(item), justification='center', size=(400, 2))],
        [sg.Image(key='_IMAGE_', size=(200, 150), pad=((125, 125), (20, 20)))],
        [sg.Button('OK')]
    ]

    window = sg.Window(item, layout, size=(800, 800), finalize=True)
    recipe_rating = float(cookbook.get_recipe_rating(item))

    image_path = None
    for rating_range, path in rating_images.items():
        if rating_range[0] <= recipe_rating <= rating_range[1]:
            image_path = path
            break

    if image_path:
        # Load the image and update the Image element
        image = Image.open(image_path)

        resized_image = image.resize((500, 100))
        bio = BytesIO()
        resized_image.save(bio, format="PNG")
        image_data = bio.getvalue()
        window['_IMAGE_'].update(data=image_data)

    # Event loop for the popup window
    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'OK'):
            break

    window.close()

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

# Initialize cookbook...
csv_file_path = "food_recipes.csv" 
cookbook = CookBook(csv_file_path)

# Sorting by time
cookbook.quicksort_by_time()
# puts NA recipes to end
cookbook.recipe_list = cookbook.recipe_list[5262:] + cookbook.recipe_list[:5262]
# Populate recipe names into list
meal_names = [recipe.name for recipe in cookbook.recipe_list]

# Define the layout for each tab
name_tab_layout = [
    [sg.Text("Search for a meal...", size=(400, 1))],
    [sg.Input(do_not_clear=True, size=(40, 2), enable_events=True, key='_INPUT_')],
    [sg.Button('Sort by Rating', size=(20, 2), key='_SORT_BY_RATING_')],
    [sg.Listbox(meal_names, size=(400, 400), enable_events=True, key='_LIST_')],

]

ingredient_tab_layout = [
    [sg.Text("Search for recipes by ingredients...", size=(400, 1))],
    [sg.Input(do_not_clear=True, size=(40, 2), enable_events=True, key='_INGREDIENT_INPUT_')],
    [sg.Listbox([], size=(400, 400), enable_events=True, key='_INGREDIENT_LIST_')],
]


# Create separate windows for each tab
name_tab_window = sg.Window('Search by Meal Name', name_tab_layout, size=(800, 800), background_color='#F6F3E7')
ingredient_tab_window = sg.Window('Search by Ingredients', ingredient_tab_layout, size=(800, 800), background_color='#F6F3E7')
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
while True:
    
    startup_event, startup_values = startup_window.read()
    # google_crawler = GoogleImageCrawler(**init_params)
    # google_crawler.downloader.file_urls = []
    # google_crawler.crawl(keyword=keyword, **params)
    # file_urls =  google_crawler.downloader.file_urls

    if startup_event == sg.WIN_CLOSED or startup_event == 'Quit':
        break
    
    # Open the respective search tab based on the button clicked
    if startup_event == 'Search by Recipe':
        current_tab_layout = name_tab_layout
        current_tab_window = name_tab_window
    elif startup_event == 'Search by Ingredient':
        current_tab_layout = ingredient_tab_layout
        current_tab_window = ingredient_tab_window

    while True:
        current_event, current_values = current_tab_window.read(timeout=100)

        if current_event == sg.WINDOW_CLOSED or current_event == 'Quit':
            break
        


        if current_tab_layout is name_tab_layout:
            if current_values['_INPUT_'] != '':
                search_by_name(current_values['_INPUT_'], cookbook, current_tab_window)
                sorted = False
            elif current_values['_INPUT_'] == '' and sorted != True:
                current_tab_window.Element('_LIST_').Update(meal_names)
            if current_event == '_SORT_BY_RATING_':
                sort_by_rating(cookbook, current_tab_window, current_tab_layout)
                sorted = True
        elif current_tab_layout is ingredient_tab_layout:
            if current_values['_INGREDIENT_INPUT_'] != '':
                search_by_ingredients(current_values['_INGREDIENT_INPUT_'], cookbook, current_tab_window)
            else:
                current_tab_window.Element('_INGREDIENT_LIST_').Update([])

        if current_event == '_LIST_' and len(current_values['_LIST_']):
            selected_item = current_values['_LIST_'][0]
            create_popup(selected_item, cookbook)
        if current_event == '_INGREDIENT_LIST_' and len(current_values['_INGREDIENT_LIST_']):
            selected_item = current_values['_INGREDIENT_LIST_'][0]
            create_popup(selected_item, cookbook)
        if current_event == 'Back':
            break

    current_tab_window.close()

startup_window.close()