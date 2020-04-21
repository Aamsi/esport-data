import requests

from ids import TOKEN
"""
    Take charge of requesting data to Pandoscore and build an ordered object to treat
"""

class RequestData():
    """
        - Request data from Pandascore for LOL major tournaments
        - object.games_upcoming/running/past return dictionnary with all games for each competition in leagues_wanted
    """

    def __init__(self):
        self.results_tournaments_running = []
        self.results_matches_upcoming = []
        self.results_matches_running = []
        self.results_matches_past = []
        self.series_ids = {}
        self.games_upcoming = {}
        self.games_running = {}
        self.games_past = {}
        self.leagues_wanted = ['LCK', 'LEC', 'LPL', 'LCS']
        self.build = self.build_object()

    def request_data(self):
        """
            Get json files from Pandascore API
        """
        i = 1
        while i < 2:
            res_tournaments_running = requests.get(f"https://api.pandascore.co/lol/tournaments/running?page[number]={i}page[size]=100&token={TOKEN}")
            res_matches_upcoming = requests.get(f"https://api.pandascore.co/lol/matches/upcoming?page[number]={i}&page[size]=100&token={TOKEN}")
            res_matches_past = requests.get(f"https://api.pandascore.co/lol/matches/past?page[number]={i}&page[size]=100&token={TOKEN}")
            self.results_tournaments_running.extend(res_tournaments_running.json())
            self.results_matches_upcoming.extend(res_matches_upcoming.json())
            self.results_matches_past.extend(res_matches_past.json())
            i += 1
        
        res_matches_running = requests.get(f"https://api.pandascore.co/lol/matches/running?page[size]=100&token={TOKEN}")
        self.results_matches_running.extend(res_matches_running)
    
    def get_series_ids(self):
        """
            Get series id to retrieve matching games in build_match_object()
        """
        leagues_wanted = ['LCK', 'LEC', 'LPL', 'LCS']
        for result in self.results_tournaments_running:
            if result['league']['name'] in self.leagues_wanted:
                competition = f"{result['league']['name']} {result['serie']['season']} {result['serie']['year']} {result['name']}"

                if result['league_id'] not in self.series_ids:
                    self.series_ids[competition] = result['serie_id']

    def build_matches_upcoming(self):
        """
            Build match upcoming object: {'Competition name': [{'name': '...', 'date': '...'}, {...}, {...}]}
        """
        for serie_id in self.series_ids.items():
            objects_to_add = []
            for result in self.results_matches_upcoming:
                if serie_id[1] == result['serie_id']:
                    objects_to_add.append({'name': result['name'],
                                        'date': result['begin_at'],
                                        'bo': f"Best of {result['number_of_games']}"
                                    })
                    self.games_upcoming[serie_id[0]] = objects_to_add
    
    def build_matches_running(self):
        """
            Same as build_matches_upcoming but for matches currently playing
        """
        for serie_id in self.series_ids.items():
            objects_to_add = []
            for result in self.results_matches_running:
                try:
                    if serie_id[1] == result['serie_id']:
                        objects_to_add.append({'name': result['name'],
                                            'result': result['results'],
                                            'bo': f"Best of {result['number_of_games']}"
                                        })
                        self.games_running[serie_id[0]] = objects_to_add
                except TypeError:
                    self.games_running['Games'] = 'No games currently playing'
    
    def build_matches_past(self):
        """
            Same as build_matches_upcoming but for past matches 
        """
        for serie_id in self.series_ids.items():
            objects_to_add = []
            for result in self.results_matches_past:
                if serie_id[1] == result['serie_id']:
                    objects_to_add.append({'name': result['name'],
                                        'date': result['begin_at'],
                                        'winner': result['winner']['name'],
                                        'bo': f"Best of {result['number_of_games']}"
                                    })
                    self.games_past[serie_id[0]] = objects_to_add
    
    def build_object(self):
        """
            Call every method of RequestData() to build the object
        """
        self.request_data()
        self.get_series_ids()
        self.build_matches_upcoming()
        self.build_matches_running()
        self.build_matches_past()


data = RequestData()
print(data.games_upcoming)
print(data.games_running)
print(data.games_past)
