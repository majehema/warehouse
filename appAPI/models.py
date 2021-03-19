from django.db import models

# Create your models here.
class Article (models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

class Shelf (models.Model):
    row = models.IntegerField()
    bay = models.IntegerField()
    height = models.DecimalField(decimal_places=1, max_digits=2)
    width = models.DecimalField(decimal_places=1, max_digits=2)
    depth = models.DecimalField(decimal_places=1, max_digits=2)
    #models.ManyToManyRel(Article.id, Article)

class Warehouse (models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE)
    amount = models.IntegerField()

