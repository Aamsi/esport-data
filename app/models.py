from app import db

# Learning to create a db with sql alchemy in flask context.

class League(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    api_id = db.Column(db.Integer, index=True, unique=True)
    series = db.relationship('Serie', backref='league', lazy='dynamic')

    def __repr__(self):
        return f"<League {self.name}>"


class Serie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=False)
    api_id = db.Column(db.Integer, index=True, unique=True)
    league_id = db.Column(db.Integer, db.ForeignKey('league.id'))
    teams = db.relationship('Team', backref='series', lazy='dynamic')
    matches = db.relationship('Match', backref='series', lazy='dynamic')

    def __repr__(self):
        return f"<Serie {self.name}>"


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), index=True, unique=True)
    acronym = db.Column(db.String(32), index=True, unique=False)
    api_id = db.Column(db.Integer, index=True, unique=True)
    serie_id = db.Column(db.Integer, db.ForeignKey('serie.id'))
    # Maybe try to add a db.relationship to get team's matches

    def __repr__(self):
        return f"<Team {self.name}>"


class Bo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(132), index=True, unique=True)

    def __repr__(self):
        return f"<BO {self.name}>"


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(132), index=True, unique=True)

    def __repr__(self):
        return f"<Status {self.name}>"


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.Integer, index=True, unique=True)
    serie_id = db.Column(db.Integer, db.ForeignKey('serie.id'))
    date = db.Column(db.DateTime, index=True)
    best_of = db.Column(db.Integer, db.ForeignKey('bo.id'))
    match_status = db.Column(db.Integer, db.ForeignKey('status.id'))
    opponents = db.relationship('Opponent', backref='match', lazy='dynamic')

    def __repr__(self):
        return f"<Match {self.id}>"


class Opponent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'))
    team1_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    team2_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    def __repr__(self):
        return f"<Opponents: {self.team1_id} - {self.team2_id}>"


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'))
    score_t1 = db.Column(db.Integer, index=True)
    score_t2 = db.Column(db.Integer, index=True)
    winner_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    def __repr__(self):
        return f"<Result: {self.score_t1} - {self.score_t2}"
    