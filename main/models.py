# -*- encoding: utf-*-
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.mail import send_mail

class Account(models.Model):
    user_id = models.CharField(primary_key=True, max_length=45)
    social_id = models.CharField(max_length=45, blank=True, null=True)
    social_app = models.CharField(max_length=45, blank=True, null=True)
    social_name = models.CharField(max_length=45)
    username = models.CharField(max_length=45)
    phone = models.CharField(max_length=10)
    birth = models.DateField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    is_active = models.IntegerField()
    comment = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'acc___db'


class ActionLog(models.Model):
    act_id = models.CharField(primary_key=True, max_length=45)
    staff = models.ForeignKey('Staff', models.DO_NOTHING)
    act_time = models.DateTimeField(blank=True, null=True)
    act_ops = models.CharField(max_length=45)

    class Meta:
        db_table = 'action_log___db'


class AccountLog(models.Model):
    acclog_id = models.CharField(primary_key=True, max_length=45)
    user = models.ForeignKey(Account, models.DO_NOTHING)
    wh_happen = models.DateTimeField(blank=True, null=True)
    acc_oops = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'acc_log___db'


class BkList(models.Model):
    bk_uuid = models.CharField(primary_key=True, max_length=45)
    user = models.ForeignKey(Account, models.DO_NOTHING, blank=True, null=True)
    store = models.ForeignKey(
        'Store', models.DO_NOTHING, blank=True, null=True)
    bk_date = models.DateField()
    time_session = models.CharField(max_length=10)
    bk_st = models.TimeField()
    bk_ed = models.TimeField(blank=True, null=True)
    wh_bk = models.DateTimeField(blank=True, null=True)
    adult = models.PositiveIntegerField()
    children = models.PositiveIntegerField()
    bk_ps = models.CharField(max_length=200, blank=True, null=True)
    bk_habit = models.CharField(max_length=200, blank=True, null=True)
    event_type = models.CharField(max_length=20, blank=True, null=True)
    is_cancel = models.IntegerField()
    waiting_num = models.PositiveIntegerField()
    entire_time = models.IntegerField()
    bk_price = models.PositiveIntegerField()
    is_confirm = models.IntegerField()

    class Meta:
        db_table = 'bk_list___db'


class Production(models.Model):
    prod_uuid = models.CharField(primary_key=True, max_length=45)
    store = models.ForeignKey('Store', models.DO_NOTHING)
    prod_name = models.CharField(max_length=45)
    prod_img = models.CharField(max_length=100)
    prod_price = models.PositiveIntegerField(blank=True, null=True)
    prod_desc = models.CharField(max_length=200, blank=True, null=True)
    prod_created = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'prod___db'


class Store(models.Model):
    store_id = models.CharField(primary_key=True, max_length=45)
    store_name = models.CharField(unique=True, max_length=45)
    store_address = models.CharField(max_length=45)
    store_phone = models.CharField(max_length=20)
    store_fax = models.CharField(max_length=20, blank=True, null=True)
    tk_service = models.IntegerField()
    stay_time = models.IntegerField()
    pay_md = models.CharField(max_length=4, blank=True, null=True)
    seat = models.PositiveIntegerField()
    store_created = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'store___db'


class StoreEvent(models.Model):
    event_id = models.CharField(primary_key=True, max_length=45, default=None)
    store = models.ForeignKey(Store, models.DO_NOTHING)
    event_type = models.CharField(max_length=45)
    event_date = models.DateField()
    time_session = models.CharField(max_length=45)
    event_created = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'store_event___db'


class Staff(AbstractBaseUser, models.Model, PermissionsMixin):
    staff_id = models.CharField(primary_key=True, max_length=45)
    store = models.ForeignKey('Store', models.DO_NOTHING)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=45)
    staff_name = models.CharField(max_length=45)
    staff_phone = models.CharField(max_length=10, blank=True, null=True)
    staff_birth = models.DateField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    staff_level = models.PositiveIntegerField()
    staff_created = models.DateTimeField(blank=True, null=True)
    is_active = models.IntegerField()

    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'staff___db'
    # @property
    # def is_authenticated(self):
    #     return True

# auth


class StaffManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_admin, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_admin=is_admin,
                          is_active=True,
                          is_superuser=is_superuser,
                          last_login=now,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)
    
