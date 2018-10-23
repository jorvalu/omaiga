from django.views.generic import CreateView, DeleteView, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from comments.forms import CommentForm, PointForm
from comments.models import Comment, Point
from links.models import Link
import json

class CommentCreateView(CreateView):
    form_class = CommentForm
    model = Comment

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        f = form.save(commit=False)
        f.user = self.request.user
        f.link = get_object_or_404(Link, pk=self.kwargs['pk'])
        last_comment = f.link.comments.last()
        if last_comment is None:
            f.corr = 1 # inicio del correlativo
        else: # último correlativo más 1
            f.corr = last_comment.corr + 1
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('link_detail', kwargs={'pk': self.kwargs['pk']})

class CommentDeleteView(DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse('link_detail', kwargs={'pk': self.kwargs['id']})

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user != self.request.user:
            raise Http404("No tienes permiso para realizar esta acción.")
        return super().dispatch(request, *args, **kwargs)

class PointView(FormView):
    form_class = PointForm
    model = Point

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def create_response(self, vdict=dict(), valid_form=True):
        response = HttpResponse(json.dumps(vdict), content_type='application/json')
        response.status = 200 if valid_form else 500
        return response

    def all_points(self, comment):
        all_points = Point.objects.filter(comment=comment)
        positives = all_points.filter(value=1).count()
        negatives = all_points.filter(value=-1).count()
        return positives, negatives

    def user_points(self, comment, user):
        user_points = Point.objects.filter(comment=comment, user=user)
        user_points = user_points
        return user_points

    def form_valid(self, form):
        f = form.save(commit=False)
        f.user = self.request.user
        f.comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        f.value = int(form.data['value'])

        result = {'id': f.comment.id}
        positives, negatives = self.all_points(f.comment)
        user_points = self.user_points(f.comment, f.user)
        has_points = user_points.count() > 0
        if not has_points and f.value == 1:
            positives = positives + 1
            result['total'] = positives + negatives
            result['karma'] = positives - negatives
            f.save()
            return self.create_response(result, True)
        if not has_points and f.value == -1:
            negatives = negatives + 1
            result['total'] = positives + negatives
            result['karma'] = positives - negatives
            f.save()
            return self.create_response(result, True)
        else:
            return self.create_response(result, False)
