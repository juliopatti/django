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
        

class Wines(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='name')
    fixed_acidity = models.DecimalField(max_digits=6, decimal_places=3, null=False, blank=False, verbose_name='fixed_acidity')
    volatile_acidity = models.DecimalField(max_digits=6, decimal_places=3, null=False, blank=False, verbose_name='volatile_acidity')
    citric_acid = models.DecimalField(max_digits=6, decimal_places=3, null=False, blank=False, verbose_name='citric_acid')
    residual_sugar = models.DecimalField(max_digits=6, decimal_places=3, null=False, blank=False, verbose_name='residual_sugar')
    chlorides = models.DecimalField(max_digits=6, decimal_places=3, null=False, blank=False, verbose_name='chlorides')
    free_sulfur_dioxide = models.DecimalField(max_digits=6, decimal_places=3, null=False, blank=False, verbose_name='free_sulfur_dioxide')
    total_sulfur_dioxide = models.DecimalField(max_digits=6, decimal_places=3, null=False, blank=False, verbose_name='total_sulfur_dioxide')
    density = models.DecimalField(max_digits=6, decimal_places=3, null=False, blank=False, verbose_name='density')
    pH = models.DecimalField(max_digits=6, decimal_places=3, null=False, blank=False, verbose_name='pH')
    sulphates = models.DecimalField(max_digits=6, decimal_places=3, null=False, blank=False, verbose_name='sulphates')
    alcohol = models.DecimalField(max_digits=6, decimal_places=3, null=False, blank=False, verbose_name='alcohol')
    quality = models.IntegerField(null=False, blank=False, verbose_name='quality')
    bin_quality = models.BooleanField(null=False, blank=False, verbose_name='bin_quality')
    train_set = models.BooleanField(default=True, verbose_name='train_set')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Wines"


