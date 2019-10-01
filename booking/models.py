# -*- encoding: utf-*-
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ActionLog(models.Model):
    act_id = models.CharField(primary_key=True, max_length=45)
    staff = models.ForeignKey('Staff', models.PROTECT)
    act_time = models.DateTimeField()
    act_ops = models.CharField(max_length=45)

    class Meta:
        db_table = 'action_log'


class BkList(models.Model):
    bk_uuid = models.CharField(primary_key=True, max_length=45)
    user = models.ForeignKey(Account, models.DO_NOTHING)
    store = models.ForeignKey('Store', models.DO_NOTHING)
    bk_date = models.DateTimeField()
    bk_st = models.DateField()
    bk_ed = models.DateField(blank=True, null=True)
    wh_bk = models.DateTimeField()
    adult = models.IntegerField()
    children = models.IntegerField()
    bk_ps = models.CharField(max_length=200, blank=True, null=True)
    tk_service = models.IntegerField()
    is_cancel = models.IntegerField()
    entire_time = models.IntegerField()

    class Meta:
        db_table = 'bk_list'


class Account(models.Model):
    user_id = models.CharField(primary_key=True, max_length=45)
    social_id = models.CharField(unique=True, max_length=45)
    username = models.CharField(max_length=45)
    phone = models.CharField(max_length=10)

    class Meta:
        db_table = 'account'

    def __str__(self):
        return self.username


class Production(models.Model):
    prod_uuid = models.CharField(primary_key=True, max_length=45)
    store = models.ForeignKey('Store', models.PROTECT)
    prod_name = models.CharField(max_length=45)
    prod_img = models.CharField(max_length=100)
    prod_price = models.PositiveIntegerField(blank=True, null=True)
    prod_desc = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'production'

    def __str__(self):
        return self.prod_name


class Staff(models.Model):
    staff_id = models.CharField(primary_key=True, max_length=45)
    store = models.ForeignKey('Store', models.PROTECT)
    staff_name = models.CharField(max_length=45)
    staff_id_num = models.CharField(unique=True, max_length=10)
    staff_phone = models.CharField(max_length=10)
    staff_birth = models.DateField()
    staff_gender = models.CharField(max_length=45)
    staff_address = models.CharField(max_length=45)
    staff_email = models.CharField(max_length=45)
    staff_level = models.PositiveIntegerField()
    staff_age = models.PositiveIntegerField()
    staff_skills = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'staff'

    def __str__(self):
        return self.staff_name


class Store(models.Model):
    store_id = models.CharField(primary_key=True, max_length=45)
    store_name = models.CharField(max_length=45)
    store_address = models.CharField(max_length=45)
    store_phone = models.CharField(max_length=20)
    store_fax = models.CharField(max_length=20, blank=True, null=True)
    tk_service = models.IntegerField()
    stay_time = models.IntegerField()
    pay_md = models.CharField(max_length=4)

    class Meta:
        db_table = 'store'

    def __str__(self):
        return self.store_name
