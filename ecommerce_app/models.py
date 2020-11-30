from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def registration_validator(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 2:
            errors['first_name'] = "First name is too short"
        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last name is too short"
        Email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not Email_regex.match(post_data['email']):
            errors['email'] = "Incorrect email!"
        user_list = User.objects.filter(email = post_data['email'])
        if len(user_list) > 0:
            errors['unique_email'] = "Something went wrong"
        if len(post_data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if post_data['confirm'] != post_data['password']:
            errors['confirm'] = "Passwords don't match"
        return errors

    def login_validator(self, post_data):
        errors = {}
        Email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not Email_regex.match(post_data['confirm_email']):
            errors['email'] = "Incorrect email!"
        user = User.objects.filter(email = post_data['confirm_email'])
        if len(user) == 0:
            errors['no_email'] = "Email not found"
        else:
            if bcrypt.checkpw(post_data['confirm_pw'].encode(), user[0].password.encode()) != True:
                errors['password'] = "Incorrect password!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.EmailField()
    password = models.CharField(max_length = 255)
    confirm_pw = models.CharField(max_length = 255)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)
    shoes_bought = models.ManyToManyField('Shoe', related_name="bought_by")
    shoes_liked = models.ManyToManyField('Shoe', related_name="liked_by")
    objects = UserManager()
    #shoes_owned - list of shoes owned and uploaded

class ShoeManager(models.Manager):
    def shoe_validator(self, post_data):
        errors = {}
        if len(post_data['brand']) < 4:
            errors['brand'] = "Please enter a Brand"
        if len(post_data['name']) < 5:
            errors['name'] = "Please enter a more specific name"
        if len(post_data['size']) < 0:
            errors['size'] = "Please enter size"
        return errors

    def sell_validator(self, post_data):
        errors = {}
        if len(post_data['brand']) < 4:
            errors['brand'] = "Please enter a Brand"
        if len(post_data['name']) < 5:
            errors['name'] = "Please enter a more specific name"
        if post_data['size'] == '':
            errors['empty_size'] = "Enter size"
        elif float(post_data['size']) < 0:
            errors['size'] = "Please enter size"
        if post_data['price'] == '':
            errors['empty_price'] = "Enter Price"
        elif float(post_data['price']) < 0:
            errors['price'] = "Please enter a valid price"
        return errors

class Shoe(models.Model):
    name = models.CharField(max_length = 255)
    brand = models.CharField(max_length = 255)
    size = models.DecimalField(max_digits = 3, decimal_places = 1)
    desc = models.TextField()
    img = models.ImageField(upload_to='images/')
    price = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0)
    for_sale = models.BooleanField(default = False)
    liked = models.BooleanField(default = False)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now_add = True)
    uploaded_by = models.ForeignKey(User, related_name = "shoes_owned",default = "", blank = True, on_delete = models.CASCADE)
    objects = ShoeManager()
    #bought_by - list of people who bought this shoe
    #liked_by - list of people who liked this shoe 