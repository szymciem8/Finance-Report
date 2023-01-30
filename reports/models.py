from django.db import models


class FinanceReport(models.Model):
    name = models.CharField(max_length=255)
    stock = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    period = models.CharField(max_length=255)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=True, null=True, related_name='finance_reports')

    def __str__(self):
        return self.name
