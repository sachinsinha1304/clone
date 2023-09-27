from django.db import models

# Create your models here.
class CodingQuestion(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField()
    constraint = models.TextField()
    input = models.TextField()
    output = models.TextField()
    extra = models.TextField()

class TestCases(models.Model):
    question = models.ForeignKey(CodingQuestion, on_delete=models.CASCADE)
    input = models.TextField()
    output = models.TextField()

class test_status(models.Model):
    user = models.CharField(max_length=40)
    status = models.IntegerField()
    time = models.IntegerField(default=180)

class UserDetails(models.Model):
    name = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    gender = models.CharField(max_length=1)
    contact = models.CharField(max_length=10)
    address = models.TextField()
    psw = models.CharField(max_length=20, default='21@sax')


