from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
import json
import os
from mongo_query_service import MongoQueryService
from recipe_details_service import RecipeDetailsService
app = Flask(__name__)

app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', True)

cors = CORS(app) # origins='http://localhost:8100')
mq_svc = MongoQueryService()
rd_svc = RecipeDetailsService()


@app.route('/pairings', methods=['GET'])
def pairings_query():
    ingredients = request.args.getlist('ingredient')
    pairing_filter = request.args.get('filter')
    # TODO make skip and limit optional
    skip = request.args.get('skip')
    limit = request.args.get('limit')
    pairings = mq_svc.get_ranked_pairings(pairing_filter, skip, limit, *ingredients)
    data = json.dumps(pairings)
    response = Response(response=data,
                        status=200,
                        mimetype="application/json")
    return response


@app.route('/recipes', methods=['GET'])
def recipes():
    ingredients = request.args.getlist('ingredient')
    # TODO make skip and limit optional
    skip = request.args.get('skip')
    limit = request.args.get('limit')
    recipes = mq_svc.get_recipes(skip, limit, *ingredients)
    data = json.dumps(recipes)
    response = Response(response=data,
                        status=200,
                        mimetype="application/json")
    return response


@app.route('/details/<recipe_id>', methods=['GET'])
def details(recipe_id):
    details = rd_svc.get_by_id(recipe_id)
    data = json.dumps(details)
    response = Response(response=data,
                        status=200,
                        mimetype="application/json")
    return response


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
