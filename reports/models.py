from django.db import models

# Create your models here.



class FinanceReport(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
