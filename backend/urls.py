from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_swagger.views import get_swagger_view
import api.urls

admin.site.site_header = "Bar Rate Administration";
admin.site.site_title = "Bar Rate Administration";


schema_view = get_swagger_view(title='Bar Rate')

urlpatterns = [
    url(r'admin/', admin.site.urls),
    url('^api/', include(api.urls)),
    url(r'^$', schema_view)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
