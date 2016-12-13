from pymongo import MongoClient

url = 'mongodb://localhost:27017/'
client = MongoClient(url)
db = client.yummly


def get_ranked_pairings(*ingredients, pairing_filter):
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
                "score": {
                    "$divide": ["$and_count", "$or_count"]
                },
                "pairing": {
                    "$arrayElemAt": [
                        {"$setDifference": ["$ingredients", ingredients]},
                        0
                    ]
                }
            }
        },
        {
            "$sort": {
                "score": -1
            }
        },
        {
            "$match": {
                "pairing": {"$regex": r".*{filter}.*".format(filter=pairing_filter), "$options": "i"}
            }
        }
    ]

    cursor = db.combinations50k.aggregate(pipeline)

    # TODO paginate and filter on server
    return list(cursor)
