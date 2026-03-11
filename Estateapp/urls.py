from django.urls import path, re_path # type: ignore
from django.conf import settings # type: ignore
from django.conf.urls.static import static # type: ignore
from django.views.static import serve # type: ignore
from Estateapp import views


urlpatterns = [
    path('', views.index, name='index'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('projects/', views.projects, name='projects'),
    path('projects/filter/', views.filter_projects, name='projects-filter'),
    path('ready-to-move/', views.readytomove, name='readytomove'),
    path('under-construction/', views.underconstruction, name='underconstruction'),
    path('new-launch/', views.newlaunch, name='newlaunch'),
    
    path('location/', views.location, name='location'),
    path('locations/<slug:city_slug>/', views.location_projects, name='location_projects'),
    
    path('blogs/', views.blogs, name='blogs'),
    path('blogdetails/<slug:slug>/', views.BlogdetailView.as_view(), name='blogdetails'),
    path('contact/', views.contact, name='contact'),
    path('cities/', views.cities, name='cities'),
    path('citypage/', views.citypage, name="citypage"),
    path('luxury/', views.luxury, name='luxury'),
    path('ultraluxury/', views.ultraluxury, name='ultraluxury'),
    path('premium/', views.premium, name='premium'),
    path('converter/', views.converter, name='converter'),
    path('privacypolicy/', views.privacypolicy, name='privacypolicy'),
    path('<slug:slug>/thankyou/', views.ThankYouView.as_view(), name='thankyou'),
    
    # This should always be last
    path('<slug:slug>/', views.ProjectDetailView.as_view(), name='projectdetail'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Media files serving (already covered by the static call above)
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})]