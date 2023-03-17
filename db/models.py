from django.db import models

class Program(models.Model):
    PLATFORM_CHOICES = (
        ('Bugcrowd', 'Bugcrowd'),
        ('HackerOne', 'HackerOne'),
        ('Synack', 'Synack'),
        ('Intigriti', 'Intigriti'),
        # Add more platforms as needed
    )
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    program_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    program_url = models.URLField()

    class Meta:
        unique_together = ('platform', 'program_name')

    def __str__(self):
        return f'{self.platform} - {self.program_name} ({self.company_name})'


class Programs(models.Model):
    data = models.OneToOneField(Program, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.data.platform} - {self.data.program_name} ({self.data.company_name})'

