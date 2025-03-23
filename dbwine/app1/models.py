from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, verbose_name='Name')
    email = models.CharField(max_length=50, null=False, blank=False, verbose_name='Email')
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Phone')
    role = models.CharField(max_length=30, null=True, blank=True, verbose_name='Role')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
