from django.db import models

class Contracts_completed(models.Model):
    name = models.CharField(max_length=100)
    
    street_number_and_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state_or_province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    phone_cell = models.CharField(max_length=20)
    phone_home = models.CharField(max_length=20)
    email = models.EmailField()

    school = models.CharField(max_length=100)
    school_email = models.EmailField()
    school_mobile = models.CharField(max_length=20)
    school_contact_person = models.CharField(max_length=100)

    company_name = models.CharField(max_length=100)
    company_street_number_and_name = models.CharField(max_length=100)
    company_city = models.CharField(max_length=100)
    company_state_or_province = models.CharField(max_length=100)
    company_postal_code = models.CharField(max_length=20)
    company_country = models.CharField(max_length=100)
    intern_supervisor = models.CharField(max_length=100, blank=True)

    supervisor_phone = models.CharField(max_length=20, blank=True)
    supervisor_email = models.EmailField(blank=True)

    start_date = models.DateField()
    end_date = models.DateField()
    intern_title = models.CharField(max_length=100, choices=[
        ('Intern', 'Intern'),
        ('Student', 'Student'),
        ('Learner', 'Learner'),
        ('Graduate', 'Graduate'),
        ('Transferee', 'Transferee')
    ])
    duties_description = models.TextField()
    hours = models.CharField(null=True, blank=True)
    
    intern_signature = models.TextField()
    hr_signature = models.TextField()

    def __str__(self):
        return f"Contract for {self.name} at {self.company_name}"

class Duty(models.Model):
    contract = models.ForeignKey(Contracts_completed, on_delete=models.CASCADE, related_name='duties')
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Duty for {self.contract.name}: {self.description[:20]}"