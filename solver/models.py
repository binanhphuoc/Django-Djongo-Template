from djongo import models
from sympy import sympify
from .kernel import *

class Attribute(models.Model):
  _id = models.ObjectIdField()
  parent_concept = models.ForeignKey('Concept',on_delete=models.CASCADE)
  symbol = models.CharField(max_length=255)
  description = models.TextField(default='',blank=True)

  def __str__(self):
    return str(self._id)

class Equation(models.Model):
  _id = models.ObjectIdField()
  parent_concept = models.ForeignKey('Concept',on_delete=models.CASCADE)
  syntax = models.TextField()
  name = models.CharField(max_length=255,default='',blank=True)
  description = models.TextField(default='',blank=True)

  def get(self, locals):
    return sympify(self.syntax, locals=locals)
    

class Concept(models.Model):
  _id = models.ObjectIdField(blank=True)
  name = models.CharField(max_length=255, unique=True)
  attributes = models.ArrayReferenceField(to=Attribute, default=list, blank=True)
  equations = models.ArrayReferenceField(to=Equation, default=list, blank=True)


