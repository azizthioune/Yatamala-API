from django.db import models

from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models.deletion import CASCADE
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
import datetime
import uuid
from django.utils import timezone
from uuid import uuid4
from django.db import IntegrityError
from indicators.managers.user_manager import UserManager

ADMIN = 'admin'
VISITEUR = 'visiteur'

USER_TYPES = (
    (ADMIN, ADMIN),
    (VISITEUR, VISITEUR),
)

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(_('firstname'), max_length=30, blank=False)
    last_name = models.CharField(_('lastname'), max_length=30, blank=True)
    phone = models.CharField(
        _('phone number'), max_length=20, blank=True)
    user_type = models.CharField(max_length=15, choices=USER_TYPES, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(default=False)
    avatar = models.ImageField(
        default="avatars/default.png", upload_to='avatars/', blank=True)
    # list of stuff made by user
    #projet = models.ManyToManyField('Projet', blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # these field are required on registering
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Projet(models.Model):
    id_projet = models.AutoField(primary_key=True)
    code = models.CharField(max_length=200, unique=True, blank=False)
    nom = models.CharField(max_length=500, blank=False)
    montant = models.CharField(max_length=500, blank=False, default="")
    montant_usd = models.CharField(max_length=500, blank=False, default="")
    part_bailleur = models.CharField(max_length=500, blank=False, default="")
    date_approb = models.DateField(default=(timezone.now))
    date_vigueur = models.DateField(default=(timezone.now))
    date_cloture = models.DateField(default=(timezone.now))
    date_remb = models.DateField(default=(timezone.now))
    les_annee = models.CharField(max_length=500, blank=True, default="")
    pdo = models.TextField(blank=True)
    population = models.CharField(max_length=500, blank=True, default="")
    region = models.CharField(max_length=500, blank=True, default="")
    montant = models.CharField(max_length=500, blank=True, default="")
    montant_usd = models.CharField(max_length=500, blank=True, default="")
    part_bailleur = models.CharField(max_length=500, blank=True, default="")
    part_etat = models.CharField(max_length=500, blank=True, default="")
    created = models.CharField(max_length=500, blank=True, default="")
    #updated = models.DateTimeField(auto_now_add=True)
    updated = models.CharField(max_length=500, blank=True, default="")

    # THE OWNER OF THIS PROJECT
    # created_by = models.ForeignKey(
    #     'User', db_column='user', related_name='created_by', on_delete=models.CASCADE)

    def __str__(self):
        return self.code

    class Meta:
        db_table = "projet"


class Indicateur(models.Model):
    id_indicateur = models.AutoField(primary_key=True)
    projet = models.ForeignKey(
        Projet, related_name="indicateurs", db_column='id_projet', on_delete=models.CASCADE, default="null")
    code = models.CharField(max_length=200, unique=True, blank=False)
    libelle = models.CharField(max_length=500, blank=True, default="")
    niveau = models.CharField(max_length=500, blank=True, default="")
    unite = models.CharField(max_length=500, blank=True, default="")
    nature = models.CharField(max_length=500, blank=True, default="")
    calcul = models.CharField(max_length=500, blank=True, default="")
    reference = models.CharField(max_length=500, blank=True, default="0")
    cible = models.CharField(max_length=200, blank=True, default="")
    valeur = models.CharField(max_length=500, blank=True, default="")
    datemaj = models.DateField(default=(timezone.now))
    description = models.TextField(blank=True, default="")
    created = models.CharField(max_length=500, blank=True, default="")
    updated = models.CharField(max_length=500, blank=True, default="")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "indicateur"


class Indicateursuivi(models.Model):
    id_indicateursuivi = models.AutoField(primary_key=True)
    indicateur = models.ForeignKey(
        Indicateur, related_name="indicateursSuivi", db_column='id_indicateur', on_delete=models.CASCADE)
    valeur = models.CharField(max_length=200, blank=True, default="")
    datemaj = models.DateField(default=(timezone.now))
    observation = models.TextField(blank=True, default="")
    created = models.CharField(max_length=500, blank=True, default="")
    updated = models.CharField(max_length=500, blank=True, default="")

    def __str__(self):
        return self.observation

    class Meta:
        db_table = "indicateursuivi"


class Annee(models.Model):
    id_annee = models.AutoField(primary_key=True)
    code = models.CharField(max_length=200, unique=True, blank=False)
    observation = models.CharField(max_length=500, blank=True, default="")
    resume = models.CharField(max_length=500, blank=True, default="")
    created = models.CharField(max_length=500, blank=True, default="")
    updated = models.CharField(max_length=500, blank=True, default="")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "annee"


class Indicateurplan(models.Model):
    id_indicateurplan = models.AutoField(primary_key=True)
    indicateur = models.ForeignKey(
        Indicateur, related_name="indicateurPlan", db_column='id_indicateur', on_delete=models.CASCADE)
    annee = models.ForeignKey(
        Indicateur, related_name="indicateurPlan_annee", db_column='id_annee', on_delete=models.CASCADE)
    libelle = models.CharField(max_length=500, blank=True, default="")
    cible = models.CharField(max_length=500, blank=True, default="")
    valeur = models.CharField(max_length=500, blank=True, default="")
    datemaj = models.CharField(max_length=500, blank=True, default="")
    observation = models.CharField(max_length=500, blank=True, default="")
    resume = models.CharField(max_length=500, blank=True, default="")
    created = models.CharField(max_length=500, blank=True, default="")
    updated = models.CharField(max_length=500, blank=True, default="")

    def __str__(self):
        return self.libelle

    class Meta:
        db_table = "indicateurplan"
