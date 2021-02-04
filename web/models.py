from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser, UserManager, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.sessions.models import Session

fs = FileSystemStorage(location='/Users/apple/Documents/Project/wallet/media')



class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        # if not email:
        #     raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    
class User(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(blank=True)
    mobile = models.CharField(max_length=255, unique=True)
    is_staff = models.BooleanField(verbose_name='is_staff', default=True)
    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)
    is_active = models.BooleanField(verbose_name='is_active', default=True)
    role = models.CharField(verbose_name='role', max_length=255)

    objects =  UserManager()

    USERNAME_FIELD = "mobile"
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'user'

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name


class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.OneToOneField(Session, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_session'


class Wallet(models.Model):
    mobile = models.CharField(null=True, max_length=255)
    bal = models.FloatField(default=0)
    acctno = models.TextField(null=True, blank=True)
    bank = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'wallet'


class Log(models.Model):
    mobile = models.TextField(null=True, blank=True)
    rmobile = models.TextField(null=True, blank=True)
    ref = models.TextField(null=True, blank=True)
    amount = models.TextField(null=True, blank=True)
    date = models.TextField(null=True, blank=True)
    status = models.TextField(null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    fee = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'log'


class Pins(models.Model):
    mobile = models.TextField(null=True, blank=True)
    pin = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'pins'

class Utility(models.Model):
    service_name = models.CharField(max_length=100)
    service_id = models.CharField(max_length=100)
    variation_code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    variation_amount = models.FloatField()

    class Meta:
        db_table = 'utility'

class Banks(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20)

    class Meta:
        db_table = 'banks'