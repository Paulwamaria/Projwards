from django.db import models


# Create your models here.

class Project(models.Model):
    title = models.CharField(max-max_length=60)
    image = models.ImageField(upload_to='media/wards/', blank = True, null =True)
    descrption = models.TextField()
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

class Review(models.Model):
    
    Project = models.ForeignKey(Image, related_name = 'project_reviews',on_delete = models.CASCADE)
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
    design_votes = models.IntegerRangeField(min_value=0, max_value=10)
    content_votes = models.IntegerRangeField(min_value=0, max_value=10)
    usability_votes = models.IntegerRangeField(min_value=0, max_value=10)
    creativity_votes = models.IntegerRangeField(min_value=0, max_value=10)
    

    def __str__(self):
        return f'design {self.design_votes} usability {self.usability_votes} content {self.content_votes} creativity {self.creativity_votes}'

    def save_votes(self):
        self.save()

    def delete_votes(self):
        self.delete()