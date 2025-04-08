from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import timedelta
from django.conf import settings
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activity, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Clear existing data using raw MongoDB commands to avoid ORM issues
        client = MongoClient()
        db = client[settings.DATABASES['default']['NAME']]
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activity.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create users
        users = [
            User(email='thundergod@mhigh.edu', name='Thor', password='password1'),
            User(email='metalgeek@mhigh.edu', name='Tony Stark', password='password2'),
            User(email='zerocool@mhigh.edu', name='Steve Rogers', password='password3'),
            User(email='crashoverride@hmhigh.edu', name='Natasha Romanoff', password='password4'),
            User(email='sleeptoken@mhigh.edu', name='Bruce Banner', password='password5'),
        ]
        # Save users individually to ensure they are persisted
        for user in users:
            user.save()

        # Create teams
        team1 = Team(name='Blue Team')
        team2 = Team(name='Gold Team')
        team1.save()
        team2.save()

        # Create activities
        activities = [
            Activity(user=users[0], type='Cycling', duration=60, date='2025-04-08'),
            Activity(user=users[1], type='Crossfit', duration=120, date='2025-04-07'),
            Activity(user=users[2], type='Running', duration=90, date='2025-04-06'),
            Activity(user=users[3], type='Strength', duration=30, date='2025-04-05'),
            Activity(user=users[4], type='Swimming', duration=75, date='2025-04-04'),
        ]
        for activity in activities:
            activity.save()

        # Create leaderboard entries
        leaderboard_entries = [
            Leaderboard(team=team1, score=100),
            Leaderboard(team=team2, score=90),
        ]
        Leaderboard.objects.bulk_create(leaderboard_entries)

        # Create workouts
        workouts = [
            Workout(name='Cycling Training', description='Training for a road cycling event', duration=60),
            Workout(name='Crossfit', description='Training for a crossfit competition', duration=120),
            Workout(name='Running Training', description='Training for a marathon', duration=90),
            Workout(name='Strength Training', description='Training for strength', duration=30),
            Workout(name='Swimming Training', description='Training for a swimming competition', duration=75),
        ]
        Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))