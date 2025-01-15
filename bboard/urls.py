from django.urls import path
from django.views.generic.dates import WeekArchiveView, DayArchiveView
from django.views.generic.edit import CreateView

from bboard.models import Bb
from bboard.views import (index, by_rubric, BbCreateView,
                          add_and_save, bb_detail, BbRubricBbsView,
                          BbDetailView, BbEditView, BbDeleteView, BbIndexView,
                          BbRedirectView, edit, rubrics, bbs, search)

app_name = 'bboard'

urlpatterns = [
    # path('<int:year>/week/<int:week>/',
    #      WeekArchiveView.as_view(model=Bb, date_field='published',
    #                              context_object_name='bbs')),
    # path('<int:year>/<int:month>/<int:day>/',
    #      DayArchiveView.as_view(model=Bb, date_field='published',
    #                             month_format='%m',
    #                             context_object_name='bbs')),
    path('<int:year>/<int:month>/<int:day>/', BbRedirectView.as_view(),
         name='old_archive'),

    path('rubrics/', rubrics, name='rubrics'),
    path('bbs/<int:rubric_id>/', bbs, name='bbs'),

    path('add/', BbCreateView.as_view(), name='add'),
    path('edit/<int:pk>/', BbEditView.as_view(), name='edit'),
    # path('edit/<int:pk>/', edit, name='edit'),

    path('delete/<int:pk>/', BbDeleteView.as_view(), name='delete'),

    path('<int:rubric_id>/', BbRubricBbsView.as_view(), name='by_rubric'),

    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),

    path('search/', search, name='search'),

    path('', index, name='index'),
    # path('', BbIndexView.as_view(), name='index'),
]
