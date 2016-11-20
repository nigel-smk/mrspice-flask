from model import Ingredient, Recipe, get_all_recipes_require_ingredient_counts
import time


class QueryService:

    def __init__(self):
        self.cache = {}

    '''
    Return a list of ingredients and their pairing value
    '''
    def get_ranked_pairings(self, *ingredients):
        if not ingredients:
            return self.get_initial_recommendations()

        pairings = []

        single_counts = self.get_counts()
        start = time.time()
        all_counts = self.get_counts(*ingredients)
        given_count = self.get_count(*ingredients)
        for pairee in all_counts:
            pairer_metric = all_counts[pairee] / float(given_count)
            pairee_metric = all_counts[pairee] / float(single_counts[pairee])

            pair_rank = pairer_metric * pairee_metric
            pairings.append({
                'ingt': pairee,
                'score': pair_rank
            })

        print('Elapsed time: {0}'.format(time.time() - start))
        return sorted(pairings, key=lambda pairing: pairing['score'], reverse=True)

    def get_count(self, *ingredients):
        #TODO raise error on 0 ingredients
        given = ingredients[:-1]
        if not given:
            return self.get_counts()[ingredients[-1].node['name']]
        return self.get_counts(*given)[ingredients[-1].node['name']]

    def get_counts(self, *ingredients):
        counts = self.retrieve_counts_from_cache(*ingredients)
        if not counts:
            counts = get_all_recipes_require_ingredient_counts(*ingredients)
            self.add_counts_to_cache(counts, *ingredients)
        return counts

    def add_counts_to_cache(self, pairings, *wheres):
        if wheres:
            key = tuple(sorted(wheres))
        else:
            key = None
        self.cache[key] = pairings

    def retrieve_counts_from_cache(self, *wheres):
        if wheres:
            key = tuple(sorted(wheres))
        else:
            key = None

        return self.cache.get(key)

    #TODO create separate route for initial recommendations?
    def get_initial_recommendations(self):
        counts = self.get_counts()
        ranked = [{'ingt': key, 'score': counts[key]} for key in counts]
        return sorted(ranked, key=lambda rank: rank['score'], reverse=True)

if __name__ == '__main__':
    qs = QueryService()
    ingredient1 = Ingredient('avocado')
    ingredient2 = Ingredient('lime')
    ingredient3 = Ingredient('cilantro')
    pairingz = qs.get_ranked_pairings(ingredient1, ingredient2, ingredient3)

    for p in pairingz:
        print(p)
