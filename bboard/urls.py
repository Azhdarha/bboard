from bboard.models import Bb
from django.urls import path, re_path

from bboard.views import index, by_rubric, BbCreateView, add, add_save, add_and_save, bb_detail, BbRubricBbsView
from django.views.generic.edit import CreateView



app_name = 'bboard'

urlpatterns = [
    path('add/', BbCreateView.as_view(), name='add'),
    #path('add/save/', add_save, name='add_save'),
    #path('add/', add, name='add'),
    path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('', index, name='index'),
    path('<int:rubric_id>/', BbRubricBbsView.as_view(), name='by_rubric'),

    # path('add/', add_and_save, name='add'),
    # path('add/', BbCreateView.as_view(model=Bb, template_name='bboard/bb_create.html'), name='add'),

    path('detail/<int:bb_id>/', bb_detail, name='detail')

    #re_path(r^'add/$', BbCreateView.as_view(), name='add'),
    #re_path(r'^(?P<int:rubric_id>[0-9]*)/$', by_rubric, name='by_rubric'),
    #re_path(r'^$', index, name='index'),
]
