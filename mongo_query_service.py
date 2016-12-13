from mongo_model import get_ranked_pairings
import time


class MongoQueryService:

    def __init__(self):
        pass

    '''
    Return a list of ingredients and their pairing value
    '''
    def get_ranked_pairings(self, *ingredients):
        return get_ranked_pairings(*ingredients)

if __name__ == '__main__':
    qs = MongoQueryService()
