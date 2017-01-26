from pymongo import MongoClient
import config

URL = "mongodb://{username}:{password}@{host}".format(
    username=config.MONGO_USER,
    password=config.MONGO_PASS,
    host=config.MONGO_HOST
)
DATABASE = config.MONGO_DATABASE
RECIPES = config.RECIPES
COMBINATIONS = config.COMBINATIONS

client = MongoClient(URL)
db = client[DATABASE]

def get_precalc_ranked_pairings(pairing_filter, skip, limit, *ingredients):
    if not pairing_filter:
        pairing_filter = ''
    if skip:
        skip = int(skip)
    if limit:
        limit = int(limit)

    ingredients = list(ingredients)
    ingredients.sort()
    combo_id = '::'.join(ingredients)
    result = db[COMBINATIONS].find_one(
        {
            "_id": combo_id
        },
        {
            "_id": 0,
            "and_count": 0,
            "or_count": 0,
            "score": 0,
            "r": 0,
            "ingredients": 0,
            "pairings": {
                "$slice": [skip, limit]
            }
        })
    return list(result['pairings'])

def get_ranked_pairings(pairing_filter, skip, limit, *ingredients):
    if not pairing_filter:
        pairing_filter = ''
    if skip:
        skip = int(skip)
    if limit:
        limit = int(limit)
    r = len(ingredients) + 1
    pipeline = [
        {
            "$match": {
                "r": r,
                "ingredients": {
                    "$all": ingredients
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "score": {
                    "$divide": ["$and_count", "$or_count"]
                },
                "name": {
                    "$arrayElemAt": [
                        {"$setDifference": ["$ingredients", ingredients]},
                        0
                    ]
                }
            }
        },
        {
            "$match": {
                "name": {"$regex": r".*{filter}.*".format(filter=pairing_filter), "$options": "i"}
            }
        },
        {
            "$sort": {
                "score": -1
            }
        },
        {
            "$skip": skip
        },
        {
            "$limit": limit
        }
    ]

    cursor = db[COMBINATIONS].aggregate(pipeline)

    return list(cursor)


def get_all_ingredients(ingt_filter, skip, limit):
    if not ingt_filter:
        ingt_filter = ''
    if skip:
        skip = int(skip)
    if limit:
        limit = int(limit)
    pipeline = [
        {
            "$match": {
                "r": 1,
                "_id": {
                    "$regex": ".*{ingt_filter}.*".format(ingt_filter=ingt_filter),
                    "$options": "i"
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "name": {
                    "$arrayElemAt": [
                        "$ingredients",
                        0
                    ]
                },
                "score": "$and_count"
            }
        },
        {
            "$sort": {
                "score": -1
            }
        },
        {
            "$skip": skip
        },
        {
            "$limit": limit
        }
    ]

    cursor = db[COMBINATIONS].aggregate(pipeline)

    return list(cursor)


def calc_ranked_pairings(pairing_filter, skip, limit, *ingredients):
    # get list of pairing candidates
    candidates = get_pairing_candidates(*ingredients)

    pairings = []
    for candidate in candidates:
        combination = list(ingredients) + [candidate]
        combination.sort()

        and_count = db[RECIPES].find({
            "ingredients": {
                "$all": combination
            }
        }).count()

        or_count = db[RECIPES].find({
            "ingredients": {
                "$in": combination
            }
        }).count()

        # enter the combination into the database
        combo_id = '::'.join(combination)
        r = len(combination)

        # upsert
        db[COMBINATIONS].update_one(
            {"_id": combo_id},
            {
                "$set": {
                    "_id": combo_id,
                    "r": r,
                    "ingredients": combination,
                    "and_count": and_count,
                    "or_count": or_count
                }
            }
        )

        pairings.append({
            "name": candidate,
            "score": and_count / float(or_count)
        })

    # filter and skip/limit
    if not pairing_filter:
        pairing_filter = ''
    if skip:
        skip = int(skip)
    if limit:
        limit = int(limit)
    pairings = [p for p in pairings if pairing_filter in p['name']][skip:skip + limit]

    return pairings


def get_pairing_candidates(*ingredients):
    pipeline = [
        {
            "$match": {
                "ingredients": {
                    "$all": ingredients
                }
            }
        },
        {
            "$project": {
                "ingredients": {
                    "$setDifference": ["$ingredients", ingredients]
                }
            }
        },
        {
            "$unwind": "$ingredients"
        },
        {
            "$group": {
                "_id": None,
                "pairings": {
                    "$addToSet": "$ingredients"
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "pairings": 1
            }
        }
    ]

    return db[RECIPES].aggregate(pipeline).next()["pairings"]


def get_recipes(skip, limit, *ingredients):
    if skip:
        skip = int(skip)
    if limit:
        limit = int(limit)

    pipeline = [
        {
            "$match": {
                "ingredients": {
                    "$all": ingredients
                },
                # TODO need to handle image uncertainty on the client
                "imageUrlsBySize.90": {
                    "$exists": True
                }
            }
        },
        {
          "$project": {
              "_id": 0,
              "flavors": 1,
              "smallImageUrls": 1,
              "attributes": 1,
              "sourceDisplayName": 1,
              "totalTimeInSeconds": 1,
              "recipeName": 1,
              "imageUrlsBySize": 1,
              "id": 1,
              "ingredients": 1,
              "rating": 1,

              "size": {
                  "$size": "$ingredients"
              }
          }
        },
        {
            "$sort": {
                "size": 1
            }
        },
        {
            "$skip": skip
        },
        {
            "$limit": limit
        }
    ]

    cursor = db[RECIPES].aggregate(pipeline)
    return list(cursor)
