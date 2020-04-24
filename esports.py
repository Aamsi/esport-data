from app import app_lol, db
from app.models import (League, Serie, Match, Team, Opponent,
                        Bo, Status, Result)

@app_lol.shell_context_processor
def make_shell_context():
    return {'db': db, 'League': League, 'Serie': Serie, 'Team': Team,
            'Match': Match, 'Opponent': Opponent, 'Bo': Bo,
            'Status': Status, 'Result': Result}
