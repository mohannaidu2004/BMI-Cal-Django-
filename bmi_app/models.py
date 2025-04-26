from django.db import models

class BMIRecord(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    height = models.FloatField()  # in cm
    weight = models.FloatField()  # in kg
    bmi_value = models.FloatField()
    bmi_category = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}'s BMI Record - {self.bmi_value}"