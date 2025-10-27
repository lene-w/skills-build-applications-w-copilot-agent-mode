from django.core.management.base import BaseCommand
from django.conf import settings
from djongo import models
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient(host='localhost', port=27017)
        db = client['octofit_db']

        # Clear collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create teams
        marvel_team = {'name': 'Marvel', 'members': []}
        dc_team = {'name': 'DC', 'members': []}
        db.teams.insert_many([marvel_team, dc_team])

        # Create users
        users = [
            {'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'team': 'Marvel'},
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': 'Marvel'},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': 'DC'},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': 'DC'},
        ]
        db.users.insert_many(users)

        # Add members to teams
        db.teams.update_one({'name': 'Marvel'}, {'$set': {'members': ['spiderman@marvel.com', 'ironman@marvel.com']}})
        db.teams.update_one({'name': 'DC'}, {'$set': {'members': ['wonderwoman@dc.com', 'batman@dc.com']}})

        # Create activities
        activities = [
            {'user_email': 'spiderman@marvel.com', 'activity': 'Running', 'duration': 30},
            {'user_email': 'ironman@marvel.com', 'activity': 'Cycling', 'duration': 45},
            {'user_email': 'wonderwoman@dc.com', 'activity': 'Swimming', 'duration': 60},
            {'user_email': 'batman@dc.com', 'activity': 'Yoga', 'duration': 40},
        ]
        db.activities.insert_many(activities)

        # Create leaderboard
        leaderboard = [
            {'team': 'Marvel', 'points': 75},
            {'team': 'DC', 'points': 100},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Create workouts
        workouts = [
            {'user_email': 'spiderman@marvel.com', 'workout': 'HIIT', 'date': '2025-10-25'},
            {'user_email': 'ironman@marvel.com', 'workout': 'Strength', 'date': '2025-10-26'},
            {'user_email': 'wonderwoman@dc.com', 'workout': 'Cardio', 'date': '2025-10-27'},
            {'user_email': 'batman@dc.com', 'workout': 'Pilates', 'date': '2025-10-28'},
        ]
        db.workouts.insert_many(workouts)

        # Ensure unique index on email for users
        db.users.create_index([('email', 1)], unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data.'))
