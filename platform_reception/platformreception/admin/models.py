from django.db import models

# Create your models here.
from django.db import models


class User(models.Model):
    user_id = models.BigAutoField(primary_key=True, unique=True)
    username = models.CharField(max_length=32, blank=False)
    password = models.CharField(max_length=50, blank=False)
    email = models.CharField(max_length=30, blank=False)
    gender = models.CharField(max_length=10, choices=[(0, "男"), (1, "女")], default=0)
    phone_number = models.CharField(max_length=20, blank=False)
    posts = models.CharField(max_length=20, blank=False)
    addtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user"
        app_label = "admin"
        verbose_name = "user_msg"


class Session_Reception(models.Model):
    session_id = models.CharField(max_length=100, blank=False, primary_key=True, unique=True)
    session_data = models.CharField(max_length=200, blank=False)
    expire_data = models.DateTimeField()

    class Meta:
        db_table = "session_reception"
        app_label = "admin"
        verbose_name = "login_session"
