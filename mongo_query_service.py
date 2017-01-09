from mongo_model import get_ranked_pairings, get_all_ingredients, calc_ranked_pairings, get_recipes
import time


class MongoQueryService:

    def __init__(self):
        pass

    '''
    Return a list of ingredients and their pairing value
    '''
    def get_ranked_pairings(self, pairing_filter, skip, limit, *ingredients):
        # TODO need strategy for using stored combination after first calculation
        # calculate the pairings for any set of ingredients len >= 3
        if len(ingredients) >= 4:
            return calc_ranked_pairings(pairing_filter, skip, limit, *ingredients)
        # look up initial recommendations if len == 0
        elif not ingredients:
            return get_all_ingredients(pairing_filter, skip, limit)
        # otherwise lookup pre-calculated combination
        else:
            return get_ranked_pairings(pairing_filter, skip, limit, *ingredients)

    def get_recipes(self, *ingredients):
        return get_recipes(*ingredients)

if __name__ == '__main__':
    qs = MongoQueryService()
