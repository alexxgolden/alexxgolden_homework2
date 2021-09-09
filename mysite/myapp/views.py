from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic


from .models import Choice, MyModel

class IndexView(generic.ListView):
    template_name = 'myapp/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return MyModel.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = MyModel
    context_object_name = 'question'
    template_name = 'myapp/detail.html'

class ResultsView(generic.DetailView):
    model = MyModel
    context_object_name = 'question'
    template_name = 'myapp/results.html'

def vote(request, question_id):
    question = get_object_or_404(MyModel, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'myapp/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('myapp:results', args=(question.id,)))
