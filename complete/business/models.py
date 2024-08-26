from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User,Group


class Business(models.Model):
        refid = models.IntegerField(blank=True,null=True)
        username = models.CharField (max_length=50,unique=True)
        email = models.EmailField (max_length=50)
        password = models.CharField (max_length=50)
        approval = models.BooleanField(default= False,blank=True,null=True)

        def __str__ (self):
                return self.username
        
@receiver(post_save, sender=Business)
def create_user(sender, instance, created, **kwargs):
    if created:
        user = User.objects.create_user(username=instance.username, password=str(instance.password))

        group_name = 'Business'
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)

class BusinessDetails(models.Model):
        CATEGORY_CHOICES = [
        ('Leisure', 'Leisure'),
        ('Educational', 'Educational'),
        ('Historical', 'Historical'),
        ('Diner', 'Diner'),
        ]
        COST_CHOICES = [
        ('0','0'),
        ('1-200','1-200'),
        ('201-500','201-500'),
        ('501+','501+'),     
        ]
        businessowner=models.ForeignKey(Business,on_delete=models.CASCADE)
        name = models.CharField (max_length=100,blank=True,null=True)
        location = models.CharField (max_length=100,blank=True,null=True)
        description = models.CharField (max_length=1000,blank=True,null=True)
        category = models.CharField (max_length=100,default='Leisure',choices=CATEGORY_CHOICES)
        category2 = models.CharField (max_length=100, blank=True,null=True,choices=CATEGORY_CHOICES)
        category3 = models.CharField (max_length=100, blank=True,null=True,choices=CATEGORY_CHOICES)
        time = models.CharField (max_length=20,blank=True,null=True)
        timeclose = models.CharField (max_length=20,blank=True,null=True)
        cost = models.CharField(max_length=100, blank=True,null=True,choices= COST_CHOICES)
        photo = models.ImageField(upload_to="media",blank=True,null=True)
        photos = models.ImageField(upload_to="media", blank=True,null=True)
        thumbnail = models.ImageField(upload_to="media",blank=True,null=True)
        promo = models.ImageField(upload_to="media", blank=True,null=True)
        announcement = models.CharField(max_length=5000, blank=True,null=True)
        archived = models.BooleanField(default=False)
        approval = models.BooleanField(default= False,blank=True,null=True)
        map = models.CharField(max_length=2000,blank=True,null=True)

        def __str__ (self):
                return self.name


