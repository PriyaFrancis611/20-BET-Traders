from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Profile(models.Model):
    username = models.CharField(max_length=100, default='')
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    email = models.EmailField(default='')
    confirm_email = models.EmailField(default='')
    password = models.CharField(max_length=100, default='')
    confirm_password = models.CharField(max_length=100, default='')
    phone = models.IntegerField()
    telegram = models.CharField(max_length=100, default='')
    country = models.CharField(max_length=100, default='')
    preferred_payment_method = models.CharField(max_length=100, default='')
    user_account = models.CharField(max_length=100, default='')
    website = models.CharField(max_length=100, default='')
    additional_info = models.TextField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Main_page(models.Model):
    user = models.ForeignKey('Profile', related_name='user', on_delete=models.CASCADE)
    available_to_withdraw = models.IntegerField(default='')
    yesterday = models.IntegerField(default='')
    current_month = models.IntegerField(default='')
    thirty_days = models.IntegerField(default='')
    total = models.IntegerField(default='')

    def __str__(self):
        return f"Data for {self.user.username}"


class Summary(models.Model):
    user = models.ForeignKey('Profile', related_name='user1', on_delete=models.CASCADE)
    views = models.IntegerField(default='')
    clicks = models.IntegerField(default='')
    direct_links = models.IntegerField(default='')
    clicks_views = models.IntegerField(default='')
    registrations = models.IntegerField(default='')
    registrations_click_ratios = models.IntegerField(default='')
    registration_with_deposits = models.IntegerField(default='')
    registration_with_deposits_registration_ratio = models.IntegerField(default='')
    total_new_deposit_amount = models.IntegerField(default='')
    overall_commission = models.IntegerField(default='')

    def __str__(self):
        return f"Data for {self.user.username}"


class Full_report(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    currency = models.CharField(max_length=10, default='USD')
    date = models.DateField()
    payout = models.DecimalField(max_digits=10, decimal_places=2)
    revenue = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"Transaction for {self.user.username} on {self.date}"


class Payment_history(models.Model):
    user = models.ForeignKey('Profile', related_name='user2', on_delete=models.CASCADE)
    currency = models.CharField(max_length=30, default='')
    date = models.DateField()
    payout = models.IntegerField()
    revenue = models.IntegerField()
    balance = models.IntegerField()
    status = models.CharField(max_length=30, default='')


    def __str__(self):
        return f"Data for {self.user.username}"
