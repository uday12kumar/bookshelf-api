import uuid

from django.contrib.auth.hashers import is_password_usable
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.db.models import Count
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from bookshelf.models import TimestampedModel


class UserManager(UserManager):
    """
     - Custom Manager for the User Model
    """

    def _create_user(self, first_name, last_name, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        user = self.model(first_name=first_name, last_name=last_name,
                          is_staff=is_staff,
                          is_superuser=is_superuser, is_active=True, last_login=now, **extra_fields)

        if password is not None:
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_user(self, first_name, last_name, password, **extra_fields):
        return self._create_user(first_name, last_name, password, False, False, **extra_fields)

    def create_superuser(self, first_name, last_name, password, **extra_fields):
        return self._create_user(first_name, last_name, password, True, True, **extra_fields)

    def check_user(self, number):
        try:
            return User.objects.get(mobile_number=number)
        except User.DoesNotExist:
            return False

    def make_user_inactive(self, user):
        user.is_active = False
        user.save()
        return user

    def remove_user_from_pool(self, user):
        user.admin_of_pools.clear()
        user.member_of_pools.clear()


class User(TimestampedModel, AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(_("active"), default=True)
    is_partner = models.BooleanField(default=False)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", 'last_name']

    objects = UserManager()

    def __unicode__(self):
        return self.get_full_name()

    def get_full_name(self):
        return u"{0} {1}".format(
            u"%s" % self.first_name or u"", u"%s" % self.last_name or u""
        )

    def get_short_name(self):
        return self.first_name

    def save(self, *args, **kwargs):
        is_hashed = is_password_usable(self.password)

        if is_hashed is False:
            self.set_password(self.password)
        if isinstance(self.first_name, str):
            self.first_name = self.first_name
        if isinstance(self.last_name, str):
            self.last_name = self.last_name
        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class UserTokenManager(models.Manager):
    def create_token(self, user):
        """Get user related token
                :param user: userobject
                :return: user token
        """
        if user.tokens.exists():
            usertoken = user.tokens.first()
            usertoken.key = str(uuid.uuid4())
            usertoken.save()
        else:
            usertoken = self.create(user=user, key=str(uuid.uuid4()))

        return usertoken.key


class UserToken(TimestampedModel):
    """
        Custom token model
    """
    key = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey(User, on_delete=True, related_name="tokens")

    objects = UserTokenManager()

    class Meta:
        verbose_name = "Token"
        verbose_name_plural = "Tokens"


class AuthorManager(models.Manager):
    def with_books(self):
        return Author.objects.all().prefetch_related('books').annotate(num_books=Count('books')).filter(
            num_books__gt=0)

    def with_out_books(self):
        return Author.objects.all().prefetch_related('books').annotate(num_books=Count('books')).exclude(
            num_books__gt=0)


class Author(TimestampedModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    objects = AuthorManager()

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
