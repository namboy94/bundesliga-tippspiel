import os
import bundesliga_tippspiel.globals as glob
from unittest import TestCase
from sqlalchemy.orm import joinedload
from bundesliga_tippspiel.initialize import initialize_db, initialize_db_models
from bundesliga_tippspiel.models.match_data.Team import Team
from bundesliga_tippspiel.models.match_data.Player import Player


class MatchDataTest(TestCase):

    def setUp(self):
        self.cleanup()
        glob.app.config["TESTING"] = True
        initialize_db()
        initialize_db_models()

    def tearDown(self):
        self.cleanup()

    def cleanup(self):
        if os.path.isfile("test.db"):
            os.remove("test.db")

    def test_models(self):
        team = Team(name="A", short_name="B", abbreviation="C", icon="D")
        player = Player(team=team)
        self.assertEqual(player.team, team)
        glob.db.session.add(team)
        glob.db.session.add(player)
        glob.db.session.commit()

        query = Team.query.options(joinedload('players'))
        self.assertEqual(query, [team])
