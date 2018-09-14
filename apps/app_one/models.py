from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
from django.core.validators import MaxValueValidator, MinValueValidator
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class userManager(models.Manager):
    def reg_validator(self, postData):
        print(postData)
        errors = {}
        if len(postData['fname']) == 0:
            errors['fname'] = 'We require a first name'
        elif len(postData['fname']) < 2:
            errors['fname'] = 'Your first name is too short'
        if len(postData['lname']) == 0:
            errors['lname'] = 'We require a last name'
        elif len(postData['lname']) < 2:
            errors['lname'] = 'Your last name is too short'
        if len(postData['email']) == 0:
            errors['email'] = 'An Email is required'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email']='Email is invalid'
        if len(postData['password']) == 0:
            errors['password'] = 'Please enter a password'
        elif len(postData['password']) < 8:
            errors['password'] = 'Password needs to be at least 8 characters'
        if len(postData['confirm']) == 0:
            errors['confirm'] = 'Confirm password can not be empty'
        if postData['password'] != postData['confirm']:
            errors['confirm'] = 'passwords must match!'
        if len(User.objects.filter(email = postData['email'])) > 0:
            errors['exists'] = "Email already exsists"
        if len(errors):
            return errors
        result = {}
        hash_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(
            fname = postData['fname'], 
            lname = postData['lname'], 
            email = postData['email'],
            password = hash_pw.decode())
        result['success'] = user
        return result


    def log_validator(self, postData):
        el_users = User.objects.filter(email = postData['email'])
        if len(el_users) > 0:
            user = el_users[0]
            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                return {"success": user}
            else:
                return {}
        else:
            return {}
    
class reviewManager(models.Manager):
    def review_validator(self, postData):
        print(postData)
        errors = {}
        if len(postData['title']) == 0:
            errors['title'] = 'A title is required'
        elif len(postData['title']) < 5:
            errors['title'] = 'The title is to short'
        if len(postData['text']) == 0:
            errors['text'] = 'Please make sure to write something'
        elif len(postData['text']) < 50:
            errors['text'] = 'The review needs to be at least 50 characters long'
        if len(postData['rating']) == 0:
            errors['rating'] = 'Rating needs to be at least 1'
        return errors



class User(models.Model):
    fname = models.CharField(max_length = 255)
    lname = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    user_level = models.SmallIntegerField(default=1)
    password = models.CharField(max_length = 255)
    confirm = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = userManager()

# class Game(models.Model):
#     title = models.CharField(max_length = 255)
#     price = models.FloatField()
#     # photo = models.ImageField(upload_to = 'images')
#     buyers = models.ManyToManyField(User, related_name = "purchasers")
#     reviewed_by = models.ForeignKey(User, related_name = "reviwers", on_delete = models.CASCADE, null = True)
#     created_at = models.DateTimeField(auto_now_add = True)
#     updated_at = models.DateTimeField(auto_now = True)

class Review(models.Model):
    title = models.CharField(max_length = 255)
    text = models.TextField(max_length = 2000)
    rating = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    author = models.ForeignKey(User, related_name = "authors", on_delete = models.CASCADE)
    picture = models.ImageField(upload_to = 'media')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = reviewManager()

class Comment(models.Model):
    text = models.TextField(max_length = 255)
    comment_by = models.ForeignKey(User, related_name= "commentors", on_delete = models.CASCADE)
    review_commented = models.ForeignKey(Review, related_name ="review", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


