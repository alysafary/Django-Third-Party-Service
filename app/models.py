import secrets

from django.contrib.postgres.fields import ArrayField

from django.db import models
from django.utils.translation import gettext as _
from django.core.validators import validate_ipv46_address


class AccessApiKey(models.Model):
    name = models.CharField(
        max_length=128, null=True, blank=True, verbose_name=_("name")
    )
    key = models.CharField(max_length=64, unique=True)
    is_enable = models.BooleanField(default=True, verbose_name=_("enable"))
    scopes = models.ManyToManyField("ApiKeyScope", verbose_name=_("scope"))
    whitelisted_ips = ArrayField(
        models.GenericIPAddressField(
            verbose_name=_("ip address"), validators=[validate_ipv46_address]
        ),
        verbose_name=_("whitelisted IPs"),
        blank=True,
        default=list,
    )

    class Meta:
        verbose_name = _("Access API Key")
        verbose_name_plural = _("Access API Keys")

    def __str__(self):
        return self.key

    def add_whitelisted_ip(self, ip):
        """Add an IP address to the whitelist."""
        validate_ipv46_address(ip)
        if ip not in self.whitelisted_ips:
            self.whitelisted_ips.append(ip)
            self.save()

    def remove_whitelisted_ip(self, ip):
        """Remove an IP address from the whitelist."""
        if ip in self.whitelisted_ips:
            self.whitelisted_ips.remove(ip)
            self.save()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.key = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)


class ApiKeyScopeView(models.Model):
    name = models.CharField(max_length=128, verbose_name=_("name"))
    url = models.CharField(max_length=128, verbose_name=_("url"))
    regex = models.TextField(verbose_name=_("regex"))

    class Meta:
        verbose_name = _("API Key Scope View")
        verbose_name_plural = _("API Key Scope Views")

    def __str__(self):
        return self.name


class ApiKeyScope(models.Model):
    views = models.ManyToManyField("ApiKeyScopeView", verbose_name=_("views name"))
    title = models.CharField(max_length=128, verbose_name=_("title"))

    class Meta:
        verbose_name = _("API Key Scope")
        verbose_name_plural = _("API Key Scopes")

    def __str__(self):
        return self.title
