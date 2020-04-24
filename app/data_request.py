import requests
import datetime
from app import app_lol

"""
    Take charge of requesting data to Pandoscore and build an ordered object to treat
"""


class RequestData():
    """
        - Request data from Pandascore for LOL major tournaments
    
        - object.leagues return a list of object with every league with its id: [{'api_id': 15432, 'name': LEC}, {...}]
    
        - object.series return a list of object with every serie with its id: [{'name': 'Spring 2020', 'api_id': 2348, 'league_api_id': 4197}, {...}]
    
        - object.teams return a list of object with teams, its id, and its associated serie id: [{'fullname': 'MAD Lions', 'acronym': 'MAD', 
                                                                                            'api_id': 126536, 'serie_api_id': 2348}, {...}]
                                                                                        
        - object.matches return a list of every match(see attr in RequestData.get_matches()): [{'serie_api_id': 2348, 'team1_id': 394, 
                                                                                'team2_id': 88, 'api_id': 557915, 'date': '2020-04-19T15:10:48Z', 
                                                                                'bo': 'best_of 5', 'score_t1': 0, 'score_t2': 3}, {...}]

        for more information about events hierarchy, visit https://developers.pandascore.co/doc/index.htm#section/Introduction/Events-hierarchy
    """

    API_KEY = app_lol.config["API_KEY"]

    def __init__(self):
        self.leagues = []
        self.series = []
        self.teams = []
        self.matches = []
        self.leagues_wanted = ['LCK', 'LEC', 'LPL', 'NA LCS']
        self.building = self.build()

    def get_leagues(self):
        res_leagues = requests.get(f"https://api.pandascore.co/lol/leagues?page[size]=100&token={self.API_KEY}")
        results_leagues = res_leagues.json()
        for result in results_leagues:
            if result['name'] in self.leagues_wanted:
                self.leagues.append({
                    'name': result['name'],
                    'api_id': int(result['id']),
                })

    def get_series(self):
        now = datetime.datetime.now()
        for league in self.leagues:
            res_series = requests.get(f"https://api.pandascore.co/leagues/{league['api_id']}/series?pages[size]=100&token={self.API_KEY}")
            results_series = res_series.json()
            for result in results_series:
                if result['year'] >= now.year - 1:
                    self.series.append({
                        'name': result['full_name'],
                        'api_id': result['id'],
                        'league_api_id': league['api_id'],
                    })
    
    def get_teams(self):
        for serie in self.series:
            res_teams = requests.get(f"https://api.pandascore.co/lol/series/{serie['api_id']}/teams?pages[size]=100&token={self.API_KEY}")
            results_teams = res_teams.json()
            for result in results_teams:
                self.teams.append({
                    'fullname': result['name'],
                    'acronym': result['acronym'],
                    'api_id': result['id'],
                    'serie_api_id': serie['api_id'],
                })
    
    def get_matches(self):
        for serie in self.series:
            res_teams = requests.get(f"https://api.pandascore.co/series/{serie['api_id']}/matches?pages[size]=30&token={self.API_KEY}")
            results_teams = res_teams.json()
            for result in results_teams:
                try:
                    self.matches.append({
                        'serie_api_id': serie['api_id'],
                        'team1_id': result['opponents'][0]['opponent']['id'],
                        'team2_id': result['opponents'][1]['opponent']['id'],
                        'api_id': result['id'],
                        'date': result['begin_at'],
                        'bo': f"{result['match_type']} {result['number_of_games']}",
                        'score_t1': result['results'][0]['score'],
                        'score_t2': result['results'][1]['score'],
                        'status': result['status'],
                        'winner_id': result['winner_id'],
                    })
                except IndexError:
                    print("Les donnees du match ne sont pas disponibles")

    def build(self):
        self.get_leagues()
        self.get_series()
        self.get_teams()
        self.get_matches()

    # def test(self):
    #     print(f"Leagues: {self.leagues} \n")
    #     print(f"Series: {self.series} \n")
    #     print(f"Teams: {self.teams} \n")
    #     print(f"Matches: {self.matches} \n")


