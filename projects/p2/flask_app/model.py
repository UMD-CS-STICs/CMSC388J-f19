import requests

class PokeClient(object):
    def __init__(self):
        self.sess = requests.Session()
        self.sess.headers.update({'User Agent': 'CMSC388J Fall 2019 Project 2'})
        self.base_url = 'https://pokeapi.co/api/v2/'

    def get_pokemon_list(self):
        """
        Returns a list of pokemon names
        """
        pokemon = []
        resp = self.sess.get(self.base_url + 'pokemon?limit=964')
        for poke_dict in resp.json()['results']:
            pokemon.append(poke_dict['name'])
        return pokemon
    
    def get_pokemon_info(self, pokemon):
        """
        Arguments:

        pokemon -- a lowercase string identifying the pokemon

        Returns a dict with info about the Pokemon with the 
        following keys and the type of value they map to:
        
        name      -> string
        height    -> int
        weight    -> int
        base_exp  -> int
        moves     -> list of strings
        abilities -> list of strings
        """
        if type(pokemon) != str:
            raise TypeError('The pokemon argument must be a string')

        resp = self.sess.get(self.base_url + ('pokemon/%s' % pokemon))

        if resp.status_code != 200:
            raise ValueError('The pokemon string you entered must be lowercase'
                             'and valid')
        
        resp = resp.json()
        
        result = {}

        result['name'] = resp['name']
        result['height'] = resp['height']
        result['weight'] = resp['weight']
        result['base_exp'] = resp['base_experience']

        moves = []
        for move_dict in resp['moves']:
            moves.append(move_dict['move']['name'])
        
        result['moves'] = moves

        abilities = []
        for ability_dict in resp['abilities']:
            abilities.append(ability_dict['ability']['name'])
        
        result['abilities'] = abilities

        return result

    def get_pokemon_with_ability(self, ability):
        """
        Arguments:

        ability -- a lowercase string identifying an ability

        Returns a list of strings identifying pokemon that have the specified ability
        """
        if type(ability) != str:
            raise TypeError('The pokemon argument must be a string')

        resp = self.sess.get(self.base_url + ('ability/%s' % ability))

        if resp.status_code != 200:
            raise ValueError('The ability string you entered must be lowercase'
                             'and valid')

        pokemon = []
        for poke_dict in resp.json()['pokemon']:
            pokemon.append(poke_dict['pokemon']['name'])
        
        return pokemon

# -- Example usage -- #
# if __name__=='__main__':
#     client = PokeClient()
#     l = client.get_pokemon_list()
#     print(len(l))
#     print(l[1])

#     i = client.get_pokemon_info(l[1])
#     print(i.keys())
#     print(i['name'])
#     print(i['base_exp'])
#     print(i['weight'])
#     print(i['height'])
#     print(i['abilities'])
#     print(len(i['moves']))


#     p = client.get_pokemon_with_ability('tinted-lens')
#     print(p)
