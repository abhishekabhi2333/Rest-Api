from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.
class Dish(models.Model):
    name=models.CharField(max_length=100)
    category=models.CharField(max_length=50)
    price=models.IntegerField()
    image=models.ImageField(upload_to="dish_images",null=True)
    def __str__(self):
        return self.name

class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    review=models.CharField(max_length=100)
    rating=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    date=models.DateField(null=True,auto_now_add=True)
    dish=models.ForeignKey(Dish,on_delete=models.CASCADE)
    class Meta:
        unique_together=('user','dish')
