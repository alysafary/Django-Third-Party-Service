from django import forms
from django.contrib import admin
from django.contrib.postgres.forms.array import SimpleArrayField

from app.models import AccessApiKey, ApiKeyScope, ApiKeyScopeView


class WhitelistedIPsForm(forms.ModelForm):
    whitelisted_ips = SimpleArrayField(
        forms.GenericIPAddressField(),
        label="Whitelisted IPs",
        help_text="Enter multiple IP addresses separated by commas.",
    )

    class Meta:
        model = AccessApiKey
        fields = "__all__"


@admin.register(AccessApiKey)
class AccessApiKeyAdmin(admin.ModelAdmin):
    list_display = ("name", "key", "is_enable", "whitelisted_ips")
    search_fields = ("key", "scopes")
    filter_horizontal = ("scopes",)
    readonly_fields = ("key",)
    form = WhitelistedIPsForm


@admin.register(ApiKeyScopeView)
class ApiKeyScopeViewAdmin(admin.ModelAdmin):
    restrict_access_to_developers = True
    list_display = ("id", "name", "regex")
    search_fields = ("name", "url")


@admin.register(ApiKeyScope)
class ApiKeyScopeAdmin(admin.ModelAdmin):
    restrict_access_to_developers = True
    list_display = ("title",)
    list_filter = ("views__app",)
    search_fields = ("title", "views")
    filter_horizontal = ("views",)
