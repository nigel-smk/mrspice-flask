from flask import Flask, request, Response
from model import Ingredient
import json
import os
from query_service import QueryService
app = Flask(__name__)
qs = QueryService()

@app.route('/matches', methods=['GET'])
def ingredient_query():
    ingredients = [Ingredient(param) for param in request.args.getlist('ingredient')]
    pairings = qs.get_ranked_pairings(*ingredients)
    data = json.dumps(pairings)
    response = Response(response=data,
                        status=200,
                        mimetype="application/json")
    return response

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)