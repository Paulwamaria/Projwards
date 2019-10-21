from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import Profile


# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=60)
    image = models.ImageField(upload_to='media/wards/', blank = True, null =True)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    project_link = models.URLField(unique=True, blank = True, null =True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def save_project(self):
        self.save()

    def delete_project(self):
        self.delete()

    def get_absolute_url(self):
        return reverse('project-detail',kwargs = {'pk':self.pk} )

    
    def datepublished(self):
        return self.created_on.strftime('%B %d %Y')


class Review(models.Model):
    
    Project = models.ForeignKey(Project, related_name = 'project_reviews',on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
   
    content = models.TextField()

    def __str__(self):
        return self.content

    def save_reviews(self):
        self.save()

    def delete_reviews(self):
        self.delete()


class Vote(models.Model):
    project = models.ForeignKey(Project, related_name = 'project_votes', on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    design_votes = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(10), MinValueValidator(0)])
     
    content_votes = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(10), MinValueValidator(0)])
    usability_votes = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(10), MinValueValidator(0)])
    creativity_votes = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(10), MinValueValidator(0)])
    

    def __str__(self):
        return f'design {self.design_votes} usability {self.usability_votes} content {self.content_votes} creativity {self.creativity_votes}'

    def save_votes(self):
        self.save()

    def delete_votes(self):
        self.delete()