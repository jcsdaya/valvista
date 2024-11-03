from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User,Group
import os


class Media(models.Model):
    file = models.FileField(upload_to="media")

@receiver(models.signals.pre_save, sender=Media)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Media.objects.get(pk=instance.pk).file
    except Media.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

class Business(models.Model):
        COST_CHOICES = [
        ('0','0'),
        ('1-200','1-200'),
        ('201-500','201-500'),
        ('501+','501+'),     
        ]
        STATUS_CHOICES = [
        ('Open','Open'),
        ('Closed','Closed'),
        ('Temporarily Closed','Temporarily Closed'),
        ('For Renovation','For Renovation'),     
        ]
        refid = models.IntegerField(blank=True,null=True)
        username = models.CharField (max_length=100,unique=True)
        name = models.CharField (max_length=100,unique=True)
        email = models.EmailField (max_length=50)
        password = models.CharField (max_length=50)
        location = models.CharField (max_length=100,blank=True,null=True)
        description = models.CharField (max_length=1000,blank=True,null=True)
        categories = models.ManyToManyField('Category', related_name='businesses')
        time = models.CharField (max_length=20,blank=True,null=True)
        timeclose = models.CharField (max_length=20,blank=True,null=True)
        cost = models.CharField(max_length=100, blank=True,null=True,choices= COST_CHOICES)
        photos = models.ManyToManyField('Media',related_name='businesses',blank=True)
        thumbnail = models.ImageField(upload_to="media",blank=True,null=True)
        promo = models.ImageField(upload_to="media", blank=True,null=True)
        announcement = models.CharField(max_length=5000, blank=True,null=True)
        archived = models.BooleanField(default=False)
        approval = models.BooleanField(default= False,blank=True,null=True)
        map = models.CharField(max_length=2000,blank=True,null=True)
        status = models.CharField(max_length=100, blank=True,null=True,choices= STATUS_CHOICES)
        

        def __str__(self):
                return self.username

@receiver(post_save, sender=Business)
def create_user(sender, instance, created, **kwargs):
    if created:
        user = User.objects.create_user(username=instance.username, password=str(instance.password),email=str(instance.email))

        group_name = 'Business'
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Rating(models.Model):
    business = models.ForeignKey(Business, related_name='ratings', on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=100,null=True, blank=True)
    score = models.IntegerField(choices=[(i, f"{i} Star") for i in range(1, 6)])
    comment = models.TextField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['business', 'name'], name='unique_business_name')
        ]
    


