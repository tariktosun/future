from django.db import models

class User(models.Model):
    CLASS_YEAR_CHOICES = ( 
        (u'2012', u'Senior'),
        (u'2013', u'Junior'),
        (u'2014', u'Sophomore')
    )
    ADMIN_TITLE_CHOICES = (
        (u'ME', u'Member'),
        (u'OF', u'Officer'),
        (u'FC', u'Food Chair'),
        (u'BAMF', u'Developer')
    )

    netid = models.CharField(max_length=8, unique=True)
    firstname = models.CharField("First Name", max_length=30)
    lastname = models.CharField("Last Name", max_length=30)
    year = models.IntegerField("Class Year", max_length=4, choices=CLASS_YEAR_CHOICES)
    fbid = models.BigIntegerField("Facebook ID", unique=True)
    authenticated = models.BooleanField("User Authenticated?")
    authcode = models.CharField("Authentication Code", max_length=30)
    admin = models.CharField("Administrator Title", max_length=4, choices=ADMIN_TITLE_CHOICES)


class Tag(models.Model):
    text = models.CharField("Tag text", max_length=15)

# post is a superclass for many kinds of things that are posted
class Post(models.Model):
    
    #author = models.ForeignKey(User, verbose_name="Post Author")
    time = models.DateTimeField(auto_now_add=True)
#    tags = models.ManyToManyField(Tag) 
#    mentions = models.ManyToManyField(User)# , related_name="users_mentioned") 
        
# general purpose user post, with a title
class UserPost(Post):
    title = models.CharField("UserPost Title", max_length=80)
    text = models.TextField("UserPost Text")

# subordinate to other posts, no title
class Comment(Post):
    text = models.TextField("Comment Text")
    parent = models.ForeignKey(Post, verbose_name="Parent Post", related_name="parent_post")

