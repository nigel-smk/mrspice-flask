from model import Recipe, Ingredient, reset_graph
from pymongo import MongoClient
import time

url = 'mongodb://localhost:27017/'
username = ''
password = ''

totalLimit = 50000
pageLimit = 10
graphed = 0

client = MongoClient(url)

db = client.yummly

#TODO set uniqueness constraints if not exists

collection = db.recipes

reset_graph()

start_time = time.time()

while graphed < totalLimit:
    results = collection.find()[graphed : graphed + pageLimit]
    for result in results:

        web_id = result['id']
        recipeName = result['recipeName']
        recipe = Recipe(id=web_id)

        ingredients = []
        for ingredient_result in result['ingredients']:
            ingredients.append(Ingredient(name=ingredient_result))

        recipe.add()
        recipe.require_ingredients(ingredients)

    graphed += pageLimit
    print('Created {0} recipes'.format(graphed))

end_time = time.time()

print('Elapsed time = {0:.2f} seconds'.format(end_time - start_time))