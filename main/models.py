from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

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
        self.total_members = self.how_many_members + self.how_many_children
        month = self.start_date.strftime("%m")
        year = self.start_date.strftime("%Y")
        id_ = Church.objects.count() + 1
        self.code = f"M{month}A{year}C{id_:04d}"
        super().save(*args, **kwargs)




class MyAccountManager(BaseUserManager):
    def create_user(self, name, surname, dni, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not dni:
            raise ValueError('User must have an username')

        user = self.model(
            email=self.normalize_email(email),
            dni=dni,
            name=name,
            surname=surname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, dni, password):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            name = name,
            surname = surname,
            dni = dni,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user



class Account(AbstractBaseUser):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    dni = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    role_type = models.CharField(max_length=50, choices=ROLE_TYPE, default='No appy')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    observation = models.TextField()

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'dni']

    objects = MyAccountManager()

    def full_name(self):
        return f'{self.name} {self.surname}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
