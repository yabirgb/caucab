"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import social.views
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.views import login, logout


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', social.views.home, name = "home"),
    url(regex=r'^me/$', view=social.views.profile, name='profile'),
    url(regex=r'^publish/$', view=social.views.publish, name='publish'),
    url(regex=r'^notifications/$', view=social.views.notifications, name='notifications'),
    url(r'^login/$', login,{"template_name" : "login.html",},name="login"),

      # Map the 'django.contrib.auth.views.logout' view to the /logout/ URL.
      # Pass additional parameters to the view like the page to show after logout
      # via a dictionary used as the 3rd argument.
     url(r'^logout/$', logout,{"next_page" : reverse_lazy('login')}, name="logout"),
]
