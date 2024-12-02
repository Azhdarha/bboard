from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404, StreamingHttpResponse, \
    FileResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.template import loader
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.views.decorators.http import require_http_methods, require_GET, require_POST, require_safe
from django.db.models import Count

from bboard.forms import BbForm
from bboard.models import Bb, Rubric
from django.views.generic.base import View, TemplateView

def index(request):
    bbs = Bb.objects.order_by('-published')
    rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    context = {'bbs': bbs, 'rubrics': rubrics}

    return render(request, 'bboard/index.html', context)

# def index(request):
#     resp = HttpResponse('Сдесь будет', content_type='text/plain; charset=utf-8')
#     resp.write('лавная')
#     resp.writelines(('страница','сайта'))
#     resp['keywords'] = 'Python', 'Django'
#     return resp

# def index(request):
#     resp_content = (request = 'Здесь будет','гавная')
#     resp = StreamingHttpResponse(resp_content, content_type='text/plain; charset=utf-8')
#
#     return resp

#def index(request):
    # filename = r'c:/'
    # return FileResponse(open(filename, 'rb'))

    # filename = r'c:/'
    # return FileResponse(open(filename, 'rb'), as_attachment=True)

    # def index(request):
    #     data = {'title': 'Мотоцикол','content': 'Сарый', 'price': 10_000}
    #     return JsonResponse(data)

# def index(request):
#     bbs = Bb.objects.all()
#     rubrics = Rubric.objects.all()
#     context = {'bbs': bbs, 'rubtics': rubrics}
#     from django.

# def index(request):
#     bbs = Bb.objects.all()
#     rubrics = Rubric.objects.all()
#     context = {'bbs': bbs, 'rubtics': rubrics}
#     return HttpResponse(render_to_string('bboard/index.html',
# context, request))

def index(request):
#     print(request.scheme)
#     print(request.path)
#     print(request.path_info)
#     print(request.encoding)
#     print(request.path)
#     print(request.content_type)
#     print(request.content_params)
#     print(request.headers)
#     print(request.headers['Accept-Encoding'])
#     print(request.headers['Accept-encoding'])
#     print(request.headers['Accept-encoding'])
#     print(request.META)
#     print(request.META['CONTENT_TYPE'])
#     print(request.META['HTTP_ACCEPT'])
#     print(request.META['HTTP_USER_AGENT'])
#     print(request.resolver_match)

    bbs = Bb.objects.order_by('-published')
    rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    context = {'bbs': bbs, 'rubrics': rubrics}

    return render(request, 'bboard/index.html', context)


def by_rubric(request, rubric_id):
    # bbs = Bb.objects.filter(rubric=rubric_id)
    bbs = get_list_or_404(Bb, rubric=rubric_id)
    rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    current_rubric = Rubric.objects.get(pk=rubric_id)

    #bbs = current_rubric.objects.all()

    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}

    return render(request, 'bboard/by_rubric.html', context)


#def by_rubric(request, rubric_id, mode):

# class BbCreateView(CreateView):
#     template_name = 'bboard/create.html'
#     model = Bb
#     #form_class = BbForm
#     success_url = reverse_lazy('bboard:index')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
#         return context

class BbCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        form = BbForm()
        context = {'form': form, 'rubrics': Rubric.objects.annotate(
            cnt=Count('bb')).filter(cnt__gt=0)
        }
        return render(request, 'bboard/bb_create.html', context)

class BbRubricBbsView(TemplateView):
    template_name = 'bboard/rubric_bbs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bbs'] = Bb.objects.filter(rubric=context['rubric_id'])
        context['rubrics'] = Rubric.objects.annotate(
            cnt=Count('bb')).filter(cnt__gt=0)
        context['current_rubric'] = Rubric.objects.get(pk=context['rubric_id'])
        return context

    def post(self, request, *args, **kwargs):
        form = BbForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bboard:by_rubric', rubric_id=form.cleaned_data['rubric'].pk)
        else:
            context = {'form': form, 'rubrics': Rubric.objects.annotate(
                cnt=Count('bb')).filter(cnt__gt=0)}
            return render(request, 'bboard/bb_create.html', context)


def add(request):
    bbf = BbForm()
    context = {'form': bbf}
    return render(request, 'bboard/bb_create.html', context)

@require_http_methods(['GET','POST'])
def add_save(request):
    bbf = BbForm(request.POST)

    if bbf.is_valid():
        bbf.save()
        return HttpResponseRedirect(reverse('bboard:by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
    else:
        context = {'form': bbf}
        return render(request, 'bboard/bb_create.html', context)


def add_and_save(request):
    if request.method == 'POST':
        bbf = BbForm(request.POST)
        if bbf.is_valid():
            bbf.save()
            # return HttpResponseRedirect(reverse('bboard:by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
            return redirect('bboard:by_rubric', rubric_id=bbf.cleaned_data['rubric'].pk)
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
        #return HttpResponseNotFound('Такое обявление не существует')
        return Http404('Такое обявление не существует')

    rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    context = {'bb': bb, 'rubtics': rubrics}

    return render(request, 'bboard/bb_detail.html', context)
