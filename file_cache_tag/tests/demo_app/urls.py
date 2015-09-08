from django.conf.urls import patterns, url

from views import DemoPage

urlpatterns = patterns(
    '',
    url(r'^test/', DemoPage.as_view()),
)