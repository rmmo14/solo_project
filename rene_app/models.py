from django.db import models
import re

# Create your models here.
class myManager(models.Manager):
    def my_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if postData['password'] != postData['confirm_pw']:
            errors['confirm_pw'] = "Passwords do not match!"
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = myManager()

class Question(models.Model):
    topic=(
        ('algebra', "ALGEBRA"),
        ('precalculus', "PRECALCULUS"),
        ('calculus', "CALCULUS"),
        ('calculus2', " CALCULUS2")
    )
    topics = models.CharField(max_length=255, choices=topic, default='algebra')
    description = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="q_posted", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # https://www.youtube.com/watch?v=OrbQY6-ltww for reference

class Solution(models.Model):
    attempt = models.TextField()
    resource = models.URLField(max_length=200)
    solution_for = models.ForeignKey(Question, related_name="sol_posted", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)