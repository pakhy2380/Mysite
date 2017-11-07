# -*- coding: utf-8 -*-
from django.conf.urls import url
from .models import Recruit, Apply
from django.shortcuts import get_object_or_404, render #render에 HttpResponse, loader가 포함되어 있음
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.http import Http404
from django.views import generic
from django.utils import timezone

from .models import Recruit, Apply

class IndexView(generic.ListView): #home.
    template_name = 'taxi/index.html'
    context_object_name = 'latest_recruit_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Recruit.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Recruit
    template_name = 'taxi/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Recruit.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Recruit
    tempate_name = 'taxi/results.html'


def vote(request, recruit_id):
    recruit = get_object_or_404(Recruit, pk=recruit_id)
    try:
        selected_apply = recruit.apply_set.get(pk=request.POST['apply'])
    except (KeyError, apply.DoesNotExist):
        # Redisplay the recruit voting form.
        return render(request,'taxi/detail.html', {
            'recruit': recruit, 'error_message': "You didn't select an apply.",
            })
    else:
        selected_apply.accept = 1 #accept되면 true
        selected_apply.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('taxi:results', args=(recruit.id,)))
        #redirect로 해야 뒤로가기 했을 때 값이 엉키지 않음
