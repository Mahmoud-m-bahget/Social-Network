from django.db import models
from django.contrib.auth.models import User
from.utils import get_random_code
from django.template.defaultfilters import slugify
from django.db.models import Q
from django.shortcuts import reverse
# Create your models here.


class ProfileManager(models.Manager):
    

    def get_all_profiles_to_invite(self,sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile  = Profile.objects.get(user=sender)
        qs       = Relationship.objects.filter(Q(sender=profile) | Q(recevier=profile))

        accepted = set([])

        for rel in qs :
            if rel.status == 'accepted':
                accepted.add(rel.recevier)
                accepted.add(rel.sender)
        
        avaliable = [profile for profile in profiles if profile not in accepted]

        return avaliable



    def get_all_profiles(self , me):
        profile = Profile.objects.all().exclude(user=me)
        return profile


class Profile(models.Model):
    first_name   = models.CharField(max_length=200,blank=True)
    last_name    = models.CharField(max_length=200,blank=True)
    user         = models.OneToOneField(User , on_delete=models.CASCADE)
    bio          = models.TextField(default="no bio ....." ,max_length=300)
    email        = models.EmailField(max_length=200,blank=True)
    country      = models.CharField(max_length=200,blank=True)
    avatar       = models.ImageField(default='avatar.png' , upload_to = 'avatars/')
    friends      = models.ManyToManyField(User , blank=True , related_name='friends')
    slug         = models.SlugField(unique=True, blank= True)
    updated      = models.DateTimeField(auto_now=True)
    created      = models.DateTimeField(auto_now_add=True)
    objects      = ProfileManager()

    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%Y')}"

    def get_absolute_url(self):
        return reverse("profiles:profile-detail-view", kwargs={"slug":self.slug})

    def get_friends(self):
        return self.friends.all()

    def get_friends_number(self):
        return self.friends.all().count()

    def get_post_num(self):
        return self.posts.all().count()

    def get_all_authors_postss(self):
        return self.posts.all()

    def get_like_given_num(self):
        likes = self.like_set.all()
        total_likes = 0
        for i in likes:
            if i.value=='like':
                total_likes +=1
        return total_likes

    def  get_like_recived_no(self):
        posts = self.posts.all()
        total_liked = 0 
        for item in posts:
            total_liked  += item.liked.all().count()
        
        return total_liked


    __initial_first_name = None
    __initail_last_name = None
    def __init__(self, *args , **kwargs):
        super().__init__(*args , **kwargs)
        self.__initial_first_name = self.first_name
        self.__initial_last_name = self.last_name



    def save(self,*args,**kwargs):
        ex = False
        to_slug = self.slug
        if self.first_name != self.__initial_first_name or self.last_name != self.__initial_last_name or self.slug=='' :
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
                ex = Profile.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug+" "+str(get_random_code()))
                    ex = Profile.objects.filter(slug=to_slug).exists()
        
            else:
                to_slug =str(self.user)
        self.slug = to_slug
        super().save(*args,**kwargs)


STATUS_CHOICES = (
    ('send','send'),
    ('accepted','accepted')
)


class RelationsManager(models.Manager):
    def invatations_received(self , receiver):
        qs = Relationship.objects.filter(recevier= receiver , status='send')
        return qs



class Relationship(models.Model):
    sender     = models.ForeignKey(Profile , on_delete=models.CASCADE , related_name='sender')
    recevier   = models.ForeignKey(Profile , on_delete=models.CASCADE , related_name='recevier')
    status     = models.CharField(max_length=8,choices=STATUS_CHOICES)
    updated    = models.DateTimeField(auto_now=True)
    created    = models.DateTimeField(auto_now_add=True)

    objects = RelationsManager()


    def __str__(self):
        return f"{self.sender}-{self.recevier}-{self.status}"