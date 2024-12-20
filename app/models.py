import uuid

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.db import models
from datetime import date


# Create your models here.


class Profile(models.Model):
    username = models.CharField(max_length=100, default='')
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    email = models.EmailField(default='')
    password = models.CharField(max_length=100, default='')
    confirm_password = models.CharField(max_length=100, default='')
    phone = models.IntegerField()
    messenger = models.CharField(max_length=100, default='')
    messengerusername = models.CharField(max_length=100,default='')
    country = models.CharField(max_length=100, default='')
    preferred_payment_method = models.CharField(max_length=100, default='')
    user_account = models.CharField(max_length=100, default='')
    website = models.CharField(max_length=100, default='')
    site_category = models.CharField(max_length=100,default='')
    reset_token = models.CharField(max_length=20, null=True, blank=True)  # Temporary reset token
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Main_page(models.Model):
    user = models.ForeignKey('Profile', related_name='user', on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    available_to_withdraw = models.IntegerField(default='')
    yesterday = models.IntegerField(default='')
    current_month = models.IntegerField(default='')
    thirty_days = models.IntegerField(default='')
    total = models.IntegerField(default='')

    def __str__(self):
        return f"Data for {self.user.username} on {self.date}"


class Summary(models.Model):
    user = models.ForeignKey('Profile', related_name='user1', on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    views = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    direct_links = models.IntegerField(default=0)
    clicks_views = models.IntegerField(default=0)
    registrations = models.IntegerField(default=0)
    registration_with_deposits_registration_ratio = models.IntegerField(default=0)
    total_new_deposit_amount = models.IntegerField(default=0)
    new_depositors = models.IntegerField(default=0)
    accounts_with_deposits = models.IntegerField(default=0)
    sum_of_all_deposits = models.IntegerField(default=0)
    revenue = models.IntegerField(default=0)
    number_of_deposits = models.IntegerField(default=0)
    active_players = models.IntegerField(default=0)
    average_profit_per_player = models.IntegerField(default=0)
    bonus_amount = models.IntegerField(default=0)
    total_rs_commission = models.IntegerField(default=0)
    cpa = models.IntegerField(default=0)
    referral_commission = models.IntegerField(default=0)
    overall_commission = models.IntegerField(default=0)

    def __str__(self):
        return f"Data for {self.user.username}  on {self.date}"


class Full_report(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateField()
    currency = models.CharField(max_length=10, default='USD')
    commission_structure = models.CharField(max_length=100)

    def __str__(self):
        return f"Transaction for {self.user.username} on {self.date}"


class Payment_history(models.Model):
    user = models.ForeignKey('Profile', related_name='user2', on_delete=models.CASCADE)
    currency = models.CharField(max_length=30, default='')
    date = models.DateField()
    payout = models.IntegerField()

    def __str__(self):
        return f"Data for {self.user.username}"


class Id(models.Model):
    user = models.ForeignKey('Profile', related_name='user3', on_delete=models.CASCADE)
    userid = models.IntegerField()

    def __str__(self):
        return self.user.username


class Commission_structure(models.Model):
    user = models.ForeignKey('Profile', related_name='user4', on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    commission_group_name = models.CharField(max_length=100)
    start_date = models.DateField()
    description = models.CharField(max_length=100)
    end_date = models.DateField()

    def __str__(self):
        return f"Data for {self.user.username}"


class Website(models.Model):
    user = models.ForeignKey('Profile', related_name='user5', on_delete=models.CASCADE)
    website_id = models.IntegerField()

    def __str__(self):
        return self.user.username


class Player_report(models.Model):
    user = models.ForeignKey('Profile', related_name='user6', on_delete=models.CASCADE)
    player_id = models.CharField(max_length=100)
    registration_date = models.DateField()

    def __str__(self):
        return f"Player report for {self.user.username}"


class Payment_history2(models.Model):
    user = models.ForeignKey('Profile', related_name='user7', on_delete=models.CASCADE)
    currency = models.CharField(max_length=100)
    time_interval = models.DateField()
    total_commission = models.IntegerField()

    def __str__(self):
        return f"Payment history 2 for {self.user.username}"


class Promo_code(models.Model):
    user = models.ForeignKey('Profile', related_name='user8', on_delete=models.CASCADE)
    promo_code_id = models.IntegerField()
    currency = models.CharField(max_length=100)

    def __str__(self):
        return f"Promo code id for {self.user.username}"


