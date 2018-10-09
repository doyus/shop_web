from django.db import models

# Create your models here.
class Yonghu(models.Model):
    username = models.CharField(max_length=50)
    password= models.CharField(max_length=8)
    shouhuo = models.CharField(max_length=80)
    phone = models.CharField(max_length=50)
    name = models.CharField(max_length=20)
    sex = models.CharField(max_length=8)
    passwordd = models.CharField(max_length=50)
class Shangping(models.Model):
    num = models.CharField(max_length=10)
    name = models.CharField(max_length=10)
    speck = models.TextField()
    img = models.CharField(max_length=80)
    manage = models.CharField(max_length=8)
class Gouwuche(models.Model):
    gnum = models.CharField(max_length=10)
    go1 = models.CharField(max_length=50)
    go2 = models.CharField(max_length=50)
    go3 = models.CharField(max_length=50)


class Guanliyuan(models.Model):
    username = models.CharField(max_length=50)
    password= models.CharField(max_length=8)
    phone = models.CharField(max_length=50)
    passwordd = models.CharField(max_length=50)
