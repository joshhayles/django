from django.db import models

class Property(models.Model):
    address = models.CharField(max_length=255)
    proposed_market_value = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    property_type = models.CharField(max_length=10, null=True)
    square_feet = models.IntegerField(default=2000)
    year_built = models.IntegerField(default=2010)
