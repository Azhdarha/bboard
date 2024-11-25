from django.urls import path, re_path

from bboard.views import index, by_rubric, BbCreateView, add, add_save, add_and_save

app_name = 'bboard'

urlpatterns = [
    # path('add/', BbCreateView.as_view(), name='add'),
    #path('add/save/', add_save, name='add_save'),
    #path('add/', add, name='add'),
    path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('', index, name='index'),

    path('add/', add_and_save, name='add'),

    #re_path(r^'add/$', BbCreateView.as_view(), name='add'),
    #re_path(r'^(?P<int:rubric_id>[0-9]*)/$', by_rubric, name='by_rubric'),
    #re_path(r'^$', index, name='index'),
]
