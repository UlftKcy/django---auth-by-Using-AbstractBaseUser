from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
# Create your models here.

""" # AbstractUser ile default olarak gelen field'lara, ek field'lar(portfolio,profile_pic gibi) ekleyebiliriz.
class User(AbstractUser):
    portfolio = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to = 'profile.pics', blank = True) """
    
class CustomUserManager(BaseUserManager):
    # extra_fields : (kwargs) extra field'lar belirlemek için ekliyoruz(is_staff,is_active,username gibi)
    def createUser(self,email,password,**extra_fields):
        if not email:
            raise ValueError("Email field is mandatory")
        
        email = self.normalize_email(email)  # normalize_email : email formatına çeviriyor.
        user  = self.model(email=email,**extra_fields)
        user.set_password(password)  # user password'u şifreli bir şekilde oluşturulacak.
        user.save()
        return user
    
    def create_superuser(self,email,password,**extra_fields):
        # Aşağıdaki extra fields'lar zorunlu.Yoksa ekliyoruz.Ve True olmalı.
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff True")
        if extra_fields.get('is_active') is not True:
            raise ValueError("Superuser must have is_active True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser True")
        
        return self.createUser(email,password,**extra_fields)
    
# AbstractBaseUser ile default olarak gelmeyen field'ları oluşturmak gerekiyor.
class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField('email adress', unique=True)
    is_staff = models.BooleanField(default=False)  # user'ın admin site'a erişip erişemeyeceğini belirler.
    is_active = models.BooleanField(default=True)  # user'ı active veya pasif olarak belirleyebiliriz.
    date_joined = models.DateTimeField(auto_now_add=True)  # ilk register işlemi yapıldığı zaman, join zamanını ekle.
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()  # create user ve superuser işlemleri yapabilmektedir.
    
    def __str__(self) :
        return self.email  
    
        
