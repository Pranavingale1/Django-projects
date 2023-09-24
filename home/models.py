from django.db import models

# Create your models here.
class Recipe(models.Model):
    recipe_name = models.CharField(max_length=50)
    recipe_description = models.TextField()
    recipe_image = models.ImageField(upload_to='recipe')

    def __str__(self) -> str:
        return self.recipe_name