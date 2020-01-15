# -*- encoding: utf-*-
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
import uuid

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
        return self._create_user(email, password, is_admin=False, is_superuser=False,
                                 **extra_fields)

    def create_admin(self, email, password=None, **extra_fields):
        return self._create_user(email, password, is_admin=True, is_superuser=False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, is_admin=True, is_superuser=True,
                                 **extra_fields)


class Staff(AbstractBaseUser, PermissionsMixin):
    staff_id = models.UUIDField(primary_key=True, default=uuid.uuid4())
    store = models.ForeignKey('Store', models.CASCADE)
    # username
    email = models.EmailField(unique=True, max_length=100)
    password = models.CharField(max_length=150)
    staff_name = models.CharField(max_length=45)
    staff_phone = models.CharField(max_length=10, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    staff_created = models.DateTimeField(blank=True, default=timezone.now())
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    objects = StaffManager()
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'staff___db'

    def __str__(self):
        return self.email

    def get_name(self):
        return self.staff_name

    # this methods are require to login super user from admin panel
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    # this methods are require to login super user from admin panel
    def has_module_perms(self, app_label):
        return self.is_superuser

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Account(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4())
    social_id = models.CharField(max_length=45, blank=True, null=True)
    social_app = models.CharField(max_length=45, blank=True, null=True)
    social_name = models.CharField(max_length=45)
    username = models.CharField(max_length=45)
    phone = models.CharField(max_length=10)
    birth = models.DateField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, default=timezone.now())
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'acc___db'


class BkList(models.Model):
    bk_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4())
    user = models.ForeignKey(Account, models.SET_NULL, blank=True, null=True)
    store = models.ForeignKey(
        'Store', models.SET_NULL, blank=True, null=True)
    bk_date = models.DateField()
    time_session = models.CharField(max_length=10)
    bk_st = models.TimeField()
    wh_bk = models.DateTimeField(blank=True, null=True)
    adult = models.PositiveIntegerField()
    children = models.PositiveIntegerField()
    bk_ps = models.CharField(max_length=200, blank=True, null=True)
    bk_habit = models.CharField(max_length=200, blank=True, null=True)
    event_type = models.CharField(max_length=20, blank=True, null=True)
    is_cancel = models.BooleanField(default=False)
    waiting_num = models.PositiveIntegerField()
    entire_time = models.BooleanField(default=False)
    bk_price = models.PositiveIntegerField()
    is_confirm = models.BooleanField(default=False)

    class Meta:
        db_table = 'bk_list___db'


class Production(models.Model):
    prod_id = models.UUIDField(primary_key=True, default=uuid.uuid4())
    store = models.ForeignKey('Store', models.CASCADE)
    prod_name = models.CharField(max_length=45)
    prod_price = models.PositiveIntegerField()
    prod_created = models.DateTimeField(blank=True, default=timezone.now())

    class Meta:
        db_table = 'prod___db'


class Store(models.Model):
    store_id = models.UUIDField(primary_key=True, default=uuid.uuid4())
    store_name = models.CharField(unique=True, max_length=45)
    store_address = models.CharField(max_length=45)
    store_phone = models.CharField(max_length=20)
    store_fax = models.CharField(max_length=20, blank=True, null=True)
    tk_service = models.BooleanField(default=False)
    seat = models.PositiveIntegerField()
    store_created = models.DateTimeField(blank=True, default=timezone.now())

    class Meta:
        db_table = 'store___db'


class StoreEvent(models.Model):
    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4())
    store = models.ForeignKey(Store, models.CASCADE)
    event_type = models.CharField(max_length=45)
    event_date = models.DateField()
    time_session = models.CharField(max_length=45)
    event_created = models.DateTimeField(blank=True, default=timezone.now())

    class Meta:
        db_table = 'store_event___db'


class StaffActionLog(models.Model):
    staff = models.ForeignKey(Staff, models.DO_NOTHING,)
    location = models.CharField(max_length=300)
    ip_address = models.CharField(max_length=200)
    operation = models.CharField(max_length=150)
    created_date = models.DateTimeField(blank=True, default=timezone.now())

    class Meta:
        db_table = 'staff_action_log___db'


class UserActionLog(models.Model):
    user = models.ForeignKey(Account, models.DO_NOTHING, )
    operation = models.CharField(max_length=200)
    location = models.CharField(max_length=300)
    created_date = models.DateTimeField(blank=True, default=timezone.now())
    ip_address = models.CharField(max_length=200)

    class Meta:
        db_table = 'user__action_log___db'
