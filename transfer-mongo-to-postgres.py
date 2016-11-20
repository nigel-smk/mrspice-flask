from pymongo import MongoClient
import psycopg2
import time

mongo_client = MongoClient('localhost', 27017)
mongo_db = mongo_client['yummly-mongo-dump']
pg_con = psycopg2.connect("dbname=pantri user='nigel' host='localhost' password=''")
pg_cursor = pg_con.cursor()


def main_loop():
    collection = mongo_db.recipes
    recipes = collection.find()
    count = 0
    for recipe in recipes:
        # the recipe id from yummly
        r_id = recipe['id']
        ingredients = recipe['ingredients']

        # the recipe id in the postgres database
        r_db_id = get_or_create_recipe(r_id)
        # list of database ids of ingredients from this recipe
        i_db_ids = get_or_create_ingredients(ingredients)
        # updating the join/reference table
        # Caution! the action is always to insert, with no checks for existing records
        create_relations(r_db_id, i_db_ids)

        # print(r_id)
        # print(ingredients)
        # print(r_db_id)
        # print(i_db_ids)

        pg_con.commit()

        count += 1
        if (count % 100 == 0):
            print(count)
        if count >= 3:
            break

def create_relations(r_db_id, i_db_ids):
    for i_id in i_db_ids:
        create_relation(r_db_id, i_id)

def create_relation(r_db_id, i_db_id):
    pg_cursor.execute("INSERT INTO recipe_to_ingredient(recipe_id, ingredient_id) VALUES (%s, %s)",
                      (r_db_id, i_db_id))

def get_or_create_ingredients(i_names):
    return [get_or_create_ingredient(name) for name in i_names]

def get_or_create_ingredient(i_name):
    pg_cursor.execute("SELECT id FROM ingredients WHERE name LIKE %s", (i_name,))
    select_res = pg_cursor.fetchone()
    if not select_res:
        pg_cursor.execute("INSERT INTO ingredients (name) VALUES (%s) RETURNING id;", (i_name,))
        insert_res = pg_cursor.fetchone()
        return insert_res[0]
    else:
        return select_res[0]

def get_or_create_recipe(r_id):
    pg_cursor.execute("INSERT INTO recipes (recipe_id) VALUES (%s) RETURNING id;", (r_id,))
    return pg_cursor.fetchone()[0]

    # pg_cursor.execute("SELECT id FROM recipes WHERE recipe_id LIKE %s", (r_id,))
    # select_res = pg_cursor.fetchone()
    # if not select_res:
    #     pg_cursor.execute("INSERT INTO recipes (recipe_id) VALUES (%s) RETURNING id;", (r_id,))
    #     insert_res = pg_cursor.fetchone()
    #     return insert_res[0]
    # else:
    #     return select_res[0]


if __name__ == "__main__":
    start_time = time.time()
    main_loop()
    end_time = time.time()
    print('Elapsed time = {0:.2f} seconds'.format(end_time - start_time))
