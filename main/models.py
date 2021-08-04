from django.db import models
import re


class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}

        EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")

        if len(postData["first_name"]) < 4:
            errors["first_name"] = "First Name must be at least 4 characters."
        if len(postData["last_name"]) < 4:
            errors["last_name"] = "Last Name must be at least 4 characters."
        if not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Invalid Email Address"
        if len(postData["password"]) < 8:
            errors["password"] = "Password must be at least 8 characters."
        if postData["password"] != postData["confirm_password"]:
            errors["password"] = "Passwords do not match"

        return errors
    
    def edit_validator(self, postData):
        errors = {}

        EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")

        if len(postData["first_name"]) < 4:
            errors["first_name"] = "First Name must be at least 4 characters."
        if len(postData["last_name"]) < 4:
            errors["last_name"] = "Last Name must be at least 4 characters."
        if not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Invalid Email Address"

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


class RetailerManager(models.Manager):
    def retailer_validator(self, postData):
        errors = {}

        if len(postData["retailer"]) < 3:
            errors["retailer"] = "Retailer name must be at least 3 characters."
        if len(postData["type"]) < 6:
            errors["type"] = "Retail type must be defined."
        if len(postData["specialty"]) < 7:
            errors["specialty"] = "Retailer specialty must be defined."
        if len(postData["city"]) > 15:
            errors["city"] = "City cannot be longer than 15 characters."
        if len(postData["state"]) > 2:
            errors["state"] = "Please use the two letter abbreviation for the state."

        return errors


class Retailer(models.Model):
    retailer = models.CharField(max_length=20)
    type = models.CharField(max_length=16)
    specialty = models.CharField(max_length=45)
    city = models.CharField(max_length=15)
    state = models.CharField(max_length=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = RetailerManager()


class ReviewManager(models.Manager):
    def review_validator(self, postData):
        errors = {}

        if len(postData["review"]) < 20:
            errors["review"] = "Review must be at least 20 characters."

        return errors


class Review(models.Model):
    review = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    retailer = models.ForeignKey(
        Retailer, related_name="reviews", on_delete=models.CASCADE
    )
    author = models.ForeignKey(User, related_name="written_reviews", on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="liked_reviews")

    objects = ReviewManager()


# Create your models here.
