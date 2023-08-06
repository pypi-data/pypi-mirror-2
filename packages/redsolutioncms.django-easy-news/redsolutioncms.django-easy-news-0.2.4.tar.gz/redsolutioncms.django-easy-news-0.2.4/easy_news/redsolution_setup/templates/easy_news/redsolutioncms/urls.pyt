# ---- Easy news urls ----

{% if cms_settings.frontpage_handler.module == 'easy_news.redsolution_setup' %}
urlpatterns += patterns('',
    (r'^', include('easy_news.urls'))
)
{% else %}
urlpatterns += patterns('',
    (r'^news/', include('easy_news.urls')),
)
{% endif %}

from easy_news.models import News
news_dict = {
    'queryset': News.objects.filter(show=True),
    'date_field': 'date',
}

try:
    sitemaps
except NameError:
    sitemps = {}

sitemaps['news'] = GenericSitemap(news_dict)


{% if 'redsolutioncms.django-generic-ratings' in cms_settings.installed_packages %}
from ratings.handlers import ratings, RatingHandler
from ratings.forms import StarVoteForm
from easy_news.models import News

ratings.register(News, RatingHandler, allow_anonymous=True, form_class=StarVoteForm)
{% endif %}