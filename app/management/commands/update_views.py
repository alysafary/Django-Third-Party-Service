from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.urls import URLPattern, URLResolver  # type: ignore

from app.models import ApiKeyScopeView


class Command(BaseCommand):
    help = "Extract views and save them to ApiKeyScopeView"

    def handle(self, *args, **options):
        urlconf = getattr(settings, "ROOT_URLCONF", None)
        if not urlconf:
            self.stderr.write(self.style.ERROR("ROOT_URLCONF is not set in settings."))
            return

        try:
            urlconf_module = __import__(urlconf, fromlist=["urlpatterns"])
            urlpatterns = urlconf_module.urlpatterns
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error loading ROOT_URLCONF: {e}"))
            return

        views = self.extract_views_from_urlpatterns(urlpatterns)
        self.save_or_update_views(views)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully processed {len(views)} views.")
        )

    def extract_views_from_urlpatterns(self, urlpatterns, base="", namespace=None):
        views = []
        for p in urlpatterns:
            if isinstance(p, URLPattern):
                try:
                    name = p.name or ""
                    regex = p.pattern.regex.pattern
                    if base.startswith("^third\-party/"):  # noqa: W605
                        views.append((p.callback, base + regex, name))
                except Exception:
                    continue
            elif isinstance(p, URLResolver):
                try:
                    patterns = p.url_patterns
                except ImportError:
                    continue
                if namespace and p.namespace:
                    _namespace = f"{namespace}:{p.namespace}"
                else:
                    _namespace = p.namespace or namespace
                pattern = p.pattern.regex.pattern
                views.extend(
                    self.extract_views_from_urlpatterns(
                        patterns, base + pattern, namespace=_namespace
                    )
                )
        return views

    def save_or_update_views(self, views):
        for func, regex, name in views:
            try:
                view = ApiKeyScopeView.objects.get(Q(name=name) | Q(regex=regex))
                view.name = name
                view.regex = regex
                view.save()
                self.stdout.write(self.style.SUCCESS(f"Updated view: {view}"))
            except ApiKeyScopeView.DoesNotExist:
                view = ApiKeyScopeView.objects.create(
                    name=name,
                    regex=regex,
                )
                self.stdout.write(self.style.SUCCESS(f"Created view: {view}"))
