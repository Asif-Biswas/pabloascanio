from django.db import models
from django.contrib.auth.models import User

# Create your models here.

ROLE_TYPE = (
    ('National', 'National'),
    ('Regional', 'Regional'),
    ('District', 'District'),
    ('Sector', 'Sector'),
    ('Standard', 'Standard'),
    ('No appy', 'No appy'),
)

class Role(models.Model):
    role_type = models.CharField(max_length=50, choices=ROLE_TYPE, default='No appy')
    name = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    
class Charge(models.Model):
    charge_type = models.CharField(max_length=50, choices=ROLE_TYPE, default='No appy')
    position_name = models.CharField(max_length=50)
    job_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class District(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Sector(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class State(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Municipality(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

Infrastructure_Type = (
    ('Own', 'Own'),
    ('Rented', 'Rented'),
    ('Lent', 'Lent'),
)

class Church(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    infrastructure_type = models.CharField(max_length=50, choices=Infrastructure_Type, default='Own')
    how_many_members = models.IntegerField()
    how_many_children = models.IntegerField()
    how_many_baptized = models.IntegerField()
    for_baptize = models.CharField(max_length=100)
    with_holy_spirit = models.CharField(max_length=100)
    group_or_cells = models.CharField(max_length=100)
    preaching_center = models.CharField(max_length=100)
    total_members = models.IntegerField() # how_many_members + how_many_children
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        total_members = self.how_many_members + self.how_many_children
        self.total_members = total_members
        month = self.start_date.strftime("%m")
        year = self.start_date.strftime("%Y")
        id_ = Church.objects.count() + 1
        self.code = f"M{month}A{year}C{id_:04d}"

        if self.total_members > 0 and self.total_members < 25:
            self.category = 'E'
        elif self.total_members > 26 and self.total_members < 75:
            self.category = 'D'
        elif self.total_members > 76 and self.total_members < 125:
            self.category = 'C'
        elif self.total_members > 126 and self.total_members < 250:
            self.category = 'B'
        elif self.total_members > 251 and self.total_members < 500:
            self.category = 'B1'
        elif self.total_members > 501 and self.total_members < 600:
            self.category = 'A'
        elif self.total_members > 601:
            self.category = 'A1'

        super().save(*args, **kwargs)


class UserProfile(models.Model):
    dni = models.CharField(max_length=50, unique=True)
    role_type = models.CharField(max_length=50, choices=ROLE_TYPE, default='No appy')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    observation = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
