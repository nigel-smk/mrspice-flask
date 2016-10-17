from flask import Flask, request
from model import Ingredient
import json
from query_service import QueryService
app = Flask(__name__)
qs = QueryService()

@app.route('/matches', methods=['GET'])
def ingredient_query():
    ingredients = [Ingredient(param) for param in request.args.getlist('ingredient')]
    pairings = qs.get_ranked_pairings(*ingredients)
    return json.dumps(pairings)

if __name__ == '__main__':
    app.debug = True
    app.run()