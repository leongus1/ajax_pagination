from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ValidationError 
import re

# Create your models here.
class UserManager(models.Manager):
    def userValidator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors={}
        if len(postData['first_name'])<2:
            errors['first_name']="First name should be at least 2 characters"
        if len(postData['last_name'])<2:
            errors['last_name']="Last name should at least 2 characters"
        if len(postData['password'])<8:
            errors['pass_len'] = "Password should be at least 8 characters long"
        if not postData['conf_pw']==postData['password']:
            errors['pass_match'] = "Passwords do not match"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_format'] = ("Invalid email address!")
        return errors
    
    def userUpdateValidator(self, postData):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name'])<2:
            errors['first_name']="First name should be at least 2 characters"
        if len(postData['last_name'])<2:
            errors['last_name']="Last name should at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_format'] = ("Invalid email address!")
        return errors
        

#CREATE VALIDATIONS
def nameLen(value):
    if len(value)<2:
        raise ValidationError("Should be at least 2 characters long.")
    else:
        return value
    
def passLen(value):
    if len(value)<8:
        raise ValidationError('Password should be at least 8 characters long.')
    else:
        return value

#MODEL
class Users(models.Model):
    first_name = models.CharField(max_length=100, validators=[nameLen])
    last_name = models.CharField(max_length=100, validators=[nameLen])
    email = models.EmailField()
    password = models.CharField(max_length=255, validators=[passLen])
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    #quotes
    def __str__(self):
        return self.email