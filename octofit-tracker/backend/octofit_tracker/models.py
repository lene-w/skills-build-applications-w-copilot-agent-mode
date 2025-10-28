from djongo import models

class User(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField(unique=True)
	team = models.CharField(max_length=100)
	def __str__(self):
		return self.name

class Team(models.Model):
	name = models.CharField(max_length=100, unique=True)
	members = models.JSONField(default=list)
	def __str__(self):
		return self.name

class Activity(models.Model):
	user_email = models.EmailField()
	activity = models.CharField(max_length=100)
	duration = models.IntegerField()
	def __str__(self):
		return f"{self.user_email} - {self.activity}"

class Leaderboard(models.Model):
	team = models.CharField(max_length=100)
	points = models.IntegerField()
	def __str__(self):
		return f"{self.team}: {self.points}"

class Workout(models.Model):
	user_email = models.EmailField()
	workout = models.CharField(max_length=100)
	date = models.CharField(max_length=20)
	def __str__(self):
		return f"{self.user_email} - {self.workout}"