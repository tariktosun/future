from django.db import models



class User(models.Model):
    CLASS_YEAR_CHOICES = ( 
        (u'2012', u'Senior')
        (u'2013', u'Junior')
        (u'2014', u'Sophomore')
    )

    ADMIN_TYPE_CHOICES = (
        (u'ME', u'Member')
        (u'OF', u'Officer')
        (u'FC', u'Food Chair')
        (u'BAMF', u'Developer')
    )

    netid = models.CharField(max_length=8i, unique=True)
    firstname = models.CharField("First Name", max_length=30)
    lastname = models.CharField("Last Name", max_length=30)
    year = models.IntegerField("Class Year", max_length=4, choices=CLASS_YEAR_CHOICES)
    fbid = models.BigIntegerField("Facebook ID", unique=True)
    authenticated = models.BooleanField("User Authenticated?")
    authcode = models.CharField("Authentication Code", max_length=30)
    adminid = models.CharField("Administrator Type", max_length=4, choices=ADMIN_TYPE_CHOICES)

class Post(models.Model):
    author = models.ForeignKey(User, verbose_name="Post Author")
    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField("Post Title", max_length=80)
    text = models.TextField("Post Text")
    
