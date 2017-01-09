import config
import requests


class RecipeDetailsService:

    def __init__(self):
        self.APP_ID = config.APP_ID
        self.APP_KEY = config.APP_KEY
        self.URL = "http://api.yummly.com/v1/api/recipe/{RECIPE_ID}?_app_id={APP_ID}&_app_key={APP_KEY}"

    def get_by_id(self, recipe_id):
        r = requests.get(self.URL.format(RECIPE_ID=recipe_id, APP_ID=self.APP_ID, APP_KEY=self.APP_KEY))
        if r.status_code == 200:
            return r.json()
        else:
            # raise exception on invalid id
            return




