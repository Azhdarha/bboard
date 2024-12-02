from django.db.models import Count
from django.http import (HttpResponse, HttpResponseRedirect, HttpResponseNotFound,
                         Http404, StreamingHttpResponse, FileResponse, JsonResponse)
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.template import loader
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import (require_http_methods,
                                          require_GET, require_POST, require_safe)
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import CreateView

from bboard.forms import BbForm
from bboard.models import Bb, Rubric


# Основной (вернуть)
def index(request):
    bbs = Bb.objects.order_by('-published')
    # rubrics = Rubric.objects.all()
    rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    context = {'bbs': bbs, 'rubrics': rubrics}

    return render(request, 'bboard/index.html', context)


def by_rubric(request, rubric_id):
    # bbs = Bb.objects.filter(rubric=rubric_id)
    bbs = get_list_or_404(Bb, rubric=rubric_id)
    # rubrics = Rubric.objects.all()
    rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    current_rubric = Rubric.objects.get(pk=rubric_id)

    # bbs = current_rubric.entries.all()

    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}

    return render(request, 'bboard/by_rubric.html', context)


class BbRubricBbsView(TemplateView):
    template_name = 'bboard/rubric_bbs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bbs'] = Bb.objects.filter(rubric=context['rubric_id'])
        context['rubrics'] = Rubric.objects.annotate(
            cnt=Count('bb')).filter(cnt__gt=0)
        context['current_rubric'] = Rubric.objects.get(pk=context['rubric_id'])
        return context


# Основной (вернуть)
# class BbCreateView(CreateView):
#     template_name = 'bboard/bb_create.html'
#     model = Bb
#     form_class = BbForm
#     success_url = reverse_lazy('bboard:index')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # context['rubrics'] = Rubric.objects.all()
#         context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
#         return context


class BbCreateView(View):
    def get(self, request, *args, **kwargs):
        form = BbForm()
        context = {'form': form, 'rubrics': Rubric.objects.annotate(
            cnt=Count('bb')).filter(cnt__gt=0)}
        return render(request, 'bboard/bb_create.html', context)

    def post(self, request, *args, **kwargs):
        form = BbForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bboard:by_rubric',
                            rubric_id=form.cleaned_data['rubric'].pk)
        else:
            context = {'form': form, 'rubrics': Rubric.objects.annotate(
                cnt=Count('bb')).filter(cnt__gt=0)}
            return render(request, 'bboard/bb_create.html', context)


def add_and_save(request):
    if request.method == 'POST':
        bbf = BbForm(request.POST)
        if bbf.is_valid():
            bbf.save()
            # return HttpResponseRedirect(reverse('bboard:by_rubric',
            #             kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
            return redirect('bboard:by_rubric',
                            rubric_id=bbf.cleaned_data['rubric'].pk)
        else:
            context = {'form': bbf}
            return render(request, 'bboard/bb_create.html', context)
    else:
        bbf = BbForm()

        context = {'form': bbf}
        return render(request, 'bboard/bb_create.html', context)


def bb_detail(request, bb_id):
    try:
        # bb = Bb.objects.get(pk=bb_id)
        bb = get_object_or_404(Bb, pk=bb_id)
    except Bb.DoesNotExist:
        # return HttpResponseNotFound('Такое объявление не существует')
        return Http404('Такое объявление не существует')

    rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    context = {'bb': bb, 'rubrics': rubrics}

    return render(request, 'bboard/bb_detail.html', context)
