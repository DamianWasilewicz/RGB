# RGB
RedGreenBlue!

Shin Bamba (PM), Kenny Li, Soojin Choi, Joyce Liao

## 2Cook or Not2Cook

### Project Overview
Our website will allow users to create an account and look for either a recipe to cook at home or a restaurant to eat at.
Recipes can be searched by ingredients or recipe name. The results will display a list of recipes that matches the user's input. The user then selects a recipe to view its ingredients, instructions, and nutritional data of the ingredients.
Restaurants can be searched by cuisine or type of establishment. The user then selects a restaurant to view its information, which includes ratings, address, and menu.

### Launch Instructions
#### Running Flask App
1. Go to [root repository](https://github.com/shinbamba/RGB) and click "Clone or Download" button
2. Copy the ssh/https link and run `$ git clone <link>`
3. Make sure the latest version of Python (currently Python 3.7.1) is installed. If not, download it [here](https://www.python.org/downloads/).
4. Install virtualenv by running `$ pip install virtualenv`
   * Make a venv by running `$ python3 -m venv ENV_DIR`
   * Activate it by running `$ . /ENV_DIR/bin/activate`
   * Deactivate it by running `$ deactivate`
5. Install Flask and wheel with `$ pip install flask` and `$ pip install wheel` (this is a Flask application)
6. Create an `api.json` to store your api keys in. Python will look for only that file, so the file name must match.
   Run these commands in the terminal when in this root directory.
   `$ touch keys.json` and `$ echo { } > keys.json`
7. Run `$ python app.py`
8. Launch the root route (http://127.0.0.1:5000/) in your browser to go to the login page.

#### API information
Four APIs are used in this project:
##### Food2Fork
* Provides ingredients to recipes
* Sign up for a free account on the [documentation page](https://www.food2fork.com/about/api)
##### USDA Nutrients
* Provide nutritional information on given ingredients
* Obtain an API key [here](https://api.data.gov/signup/)
##### Zomato
* Provide information about restaurants based on location
* Make a Zomato account and obtain an API key [here](https://developers.zomato.com/api#headline1)
