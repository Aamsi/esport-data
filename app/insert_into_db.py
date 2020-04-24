from app import db
from app.models import (League, Serie, Match, Team, Opponent,
                        Bo, Status, Result)
from app.data_request import RequestData
from sqlalchemy.exc import IntegrityError
from datetime import datetime


class InsertData():
    # Can propably add everything and then commit
    # I think I shouldn't use the flask-sqlalchemy package to handle my db outsite of models.py (I think, idk).
    # It would also allow me to use the database for another purpose
    # I'm learning

    def __init__(self):
        self.data = RequestData()

    def insert_into_leagues(self):
        for league in self.data.leagues:
            league_to_add = League(name=league['name'],
            api_id=league['api_id'])
            # I'll do a method for this
            try:
                db.session.add(league_to_add)
                db.session.commit()
            except IntegrityError:
                print('Already exists')
                db.session.rollback()

    def insert_into_series(self):
        # I'll try to do a generic method with some args
        for serie in self.data.series:
            league = League.query.filter_by(api_id=serie['league_api_id']).first() #I think I can search ids directly but not googled yet
            serie_to_add = Serie(
                name=serie['name'],
                api_id=serie['api_id'],
                league_id=league.id,
            )
            try:
                db.session.add(serie_to_add)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
    
    def insert_into_teams(self):
        for team in self.data.teams:
            serie = Serie.query.filter_by(api_id=team['serie_api_id']).first()
            team_to_add = Team(
                fullname=team['fullname'],
                acronym=team['acronym'],
                api_id=team['api_id'],
                serie_id=serie.id,
            )
            try:
                db.session.add(team_to_add)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
    
    def insert_into_bo(self):
        # Do a generic method for this
        bo_list = [match['bo'] for match in self.data.matches]
        bo_list = list(dict.fromkeys(bo_list))
        for bo in bo_list:
            bo_to_add = Bo(name=bo)
            try:
                db.session.add(bo_to_add)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
    
    def insert_into_status(self):
        #And this
        status_list = [match['status'] for match in self.data.matches]
        status_list = list(dict.fromkeys(status_list))
        for status in status_list:
            status_to_add = Status(name=status)
            try:
                db.session.add(status_to_add)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
    
    def insert_into_matches(self):
        # This one is specific so maybe I'll let it be
        for match in self.data.matches:
            serie = Serie.query.filter_by(api_id=match['serie_api_id']).first()
            bo = Bo.query.filter_by(name=match['bo']).first()
            status = Status.query.filter_by(name=match['status']).first()
            date = (match['date'])
            match_to_add = Match(
                api_id=match['api_id'],
                serie_id=serie.id,
                date=datetime(int(date[:4]), int(date[5:7]), int(date[8:10]),
                int(date[11:13]), int(date[14:16]), int(date[17:19])), #flemme
                best_of=bo.id,
                match_status=status.id,
            )
            try:
                db.session.add(match_to_add)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
    
    def insert_into_opponents(self):
        for match in self.data.matches:
            team1 = Team.query.filter_by(api_id=match['team1_id']).first()
            team2 = Team.query.filter_by(api_id=match['team2_id']).first()
            match_id = Match.query.filter_by(api_id=match['api_id']).first()
            opponents_to_add = Opponent(
                match_id=match_id.id,
                team1_id=team1.id,
                team2_id=team2.id,
            )
            try:
                db.session.add(opponents_to_add)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
        
    def insert_into_results(self):
        for match in self.data.matches:
            match_id = Match.query.filter_by(api_id=match['api_id']).first()
            team = Team.query.filter_by(api_id=match['winner_id']).first()
            result_to_add = Result(
                match_id=match_id.id,
                score_t1=match['score_t1'],
                score_t2=match['score_t2'],
                winner_id=0 if team == None else team.id, #Need to handle this before in self.data_requests.py
            )
            try:
                db.session.add(result_to_add)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def delete_data(self):
        # Delete everything in non-constant tables
        db.session.query(Opponent).delete()
        db.session.query(Result).delete()
        db.session.query(Match).delete()
        db.session.query(Team).delete()
        db.session.query(Serie).delete()
        db.session.query(League).delete()
        db.session.commit()

    
    def test(self):
        # I'll do it in a tests.py file with unittest
        leagues = League.query.all()
        series = Serie.query.all()
        teams = Team.query.all()
        bos = Bo.query.all()
        status = Status.query.all()
        matches = Match.query.all()
        opponents = Opponent.query.all()
        results = Result.query.all()

        print("Leagues:")
        for league in leagues:
            print(f"Name: {league.name} & Api_id: {league.api_id}")

        print("\nSeries:")
        for serie in series:
            print(f"Name: {serie.name} & Api_id: {serie.api_id} & league_id: {serie.league_id}")
        
        print("\nTeams: ")
        for team in teams:
            print(f"Fullname: {team.fullname} & Acronym: {team.acronym} & Api_id: {team.api_id} & Serie_id: {team.serie_id}")

        print("\nBo:")
        for bo in bos:
            print(f"Bo: {bo.name}")
        
        print("\nStatus:")
        for statu in status:
            print(f"Status: {statu.name}")
        
        print("\nMatches:")
        for match in matches:
            print(f"api_id: {match.api_id} & Serie id: {match.serie_id} & Date: {match.date} & Best of: {match.best_of} & Status: {match.match_status}")
        
        print("\n Opponents:")
        for opp in opponents:
            print(f"Match id: {opp.match_id} & Team 1 id: {opp.team1_id} & Team 2 id: {opp.team2_id}")
        
        print("\nResult: ")
        for result in results:
            print(f"Match id: {result.match_id} & Score T1: {result.score_t1} & Score T2: {result.score_t2} & Winner id: {result.winner_id}")
        

# Need to build this
# test_inserted = InsertData()
# test_inserted.insert_into_leagues()
# test_inserted.insert_into_series()
# test_inserted.insert_into_teams()
# test_inserted.insert_into_bo()
# test_inserted.insert_into_status()
# test_inserted.insert_into_matches()
# test_inserted.insert_into_opponents()
# test_inserted.insert_into_results()
# test_inserted.test()
# test_inserted.delete_data()
