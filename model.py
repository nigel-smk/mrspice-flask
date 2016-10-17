from py2neo import Graph, Node, Relationship, Subgraph
import os
import copy

#url = os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474')
url = os.environ.get('GRAPHENEDB_URL', 'http://mrspice:ZakHDJjiV7xXj2WRHFwv@hobby-cpeliffpoeaggbkeanfikgol.dbs.graphenedb.com:24789/db/data/')
username = os.environ.get('NEO4J_USERNAME', 'neo4j')
password = os.environ.get('NEO4J_PASSWORD', 'tim54p4MS')


#graph = Graph(url + '/db/data/', username=username, password=password)
graph = Graph(url)

#general queries
def reset_graph():
    graph.delete_all()

'''
Return dictionary of every ingredient and the count of recipes that ingredient is in.
Wheres are ingredients that the recipes must require.
'''
def get_all_recipes_require_ingredient_counts(*wheres):
    query = "MATCH "
    for where in wheres:
        query += "(r:Recipe)-[:REQUIRES]->(:Ingredient{{name:'{0}'}}), ".format(where.node['name'])
    query += "(i:Ingredient)<-[:REQUIRES]-(r:Recipe) RETURN i.name AS name, count(r) AS total"
    cursor = graph.run(query)
    #dictionary comprehension
    return { record['name']: record['total'] for record in cursor }

#classes for manipulating nodes
class Recipe:

    def __init__(self, id, **kwargs):
        self.node = Node('Recipe', id=id, **kwargs)
        self.node.__primarylabel__ = 'Recipe'
        self.node.__primarykey__ = 'id'

    def get_node(self):
        return self.node

    def find(self):
        recipe = graph.find_one('Recipe', 'id', **dict(self.node))
        if recipe:
            self.node = recipe
        return recipe

    def add(self):
        if not self.find():
            graph.create(self.node)
            self.node = recipe
            return True
        else:
            return False

    def merge(self):
        graph.merge(self.node, 'Recipe', self.node[self.node.__primarykey__])

    def require_ingredient(self, ingredient):
        rel = Relationship(self.node, 'REQUIRES', ingredient.node)
        graph.create(rel)

    def require_ingredients(self, ingredients):
        subgraph = copy.copy(self.node)
        for ingredient in ingredients:
            subgraph |= Relationship(self.node, 'REQUIRES', ingredient.node)
        graph.merge(subgraph)

    def get_meta_data(self):
        #retrieve metadata from mongo
        pass


class Ingredient:

    def __init__(self, name, **kwargs):
        self.node = Node('Ingredient', name=name, **kwargs)
        self.node.__primarylabel__ = 'Ingredient'
        self.node.__primarykey__ = 'name'

    def __lt__(self, other):
        self_name = self.node[self.node.__primarykey__]
        other_name = other.node[other.node.__primarykey__]
        return self_name < other_name

    def __eq__(self, other):
        self_name = self.node[self.node.__primarykey__]
        other_name = other.node[other.node.__primarykey__]
        return self_name == other_name

    def __hash__(self):
        self_name = self.node[self.node.__primarykey__]
        return hash(self_name)

    def get_node(self):
        return self.node

    def is_remote(self):
        return not self.find()

    def find(self):
        ingredient = graph.find_one('Ingredient', **dict(self.node))
        if ingredient:
            self.node = ingredient
        return ingredient

    def add(self):
        if not self.find():
            graph.create(self.node)
            self.node = ingredient
            return True
        else:
            return False

    def merge(self):
        graph.merge(self.node, 'Ingredient', self.node[self.node.__primarykey__])
