from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, FormView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.views import View
from links.models import Link, Vote
from links.forms import LinkForm, VoteForm
from comments.forms import CommentForm
from comments.models import Comment, Point
from datetime import datetime, timedelta
from django.db.models import Count
from django.http import Http404
import json

class LinkListView(ListView):
    template_name = 'links/link_list.html'
    ordering = ['-rank']
    paginate_by = 25
    model = Link

    def get_queryset(self):
        queryset = super().get_queryset()
        cat = self.request.GET.get('cat', None)
        tag = self.request.GET.get('tag', None)
        if cat is not None and tag is None:
            return queryset.filter(category=cat)
        elif tag is not None and cat is None:
            return queryset.filter(tags__name__in=[tag])
        else: # return the original queryset
            return queryset

    # check if user has voted each link
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            voted = Vote.objects.filter(user=self.request.user)
            links_in_page = [link.id for link in context["object_list"]]
            voted = voted.filter(link_id__in=links_in_page)
            voted = voted.values_list('link_id', flat=True)
            context["voted"] = voted
        return context

class LinkLatestView(LinkListView):
    ordering = ['-date']

class LinkTopView(LinkListView):

    def get_queryset(self):
        queryset = super().get_queryset()
        date_filter = datetime.today() - timedelta(7)
        queryset = queryset.filter(date__gte=date_filter)
        queryset = queryset.annotate(num_votes=Count('votes')).order_by('-num_votes')
        return queryset

class LinkCreateView(CreateView):
    template_name = 'links/link_create.html'
    form_class = LinkForm
    model = Link

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        f = form.save(commit=False)
        f.user = self.request.user
        f.rank_score = 0.0
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('link_detail', kwargs={'pk': self.object.pk})

class LinkDetailView(DetailView):
    template_name = 'links/link_detail.html'
    paginate_by = 100 # refers to comments
    model = Link

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm() # nest new comment form

        # check if user has voted the link
        if self.request.user.is_authenticated:
            voted = Vote.objects.filter(user=self.request.user)
            voted = voted.filter(link_id=self.object.id)
            voted = voted.values_list('link_id', flat=True)
            context['voted'] = voted

        # paginate comments
        comments_list = self.object.comments.all()
        paginator = Paginator(comments_list, self.paginate_by)
        page = self.request.GET.get('page')
        comments = paginator.get_page(page)
        is_paginated = len(paginator.page_range ) > 1

        # add paginated comments to context
        context['is_paginated'] = is_paginated
        context['paginator'] = paginator
        context['page_obj'] = comments
        context['comments'] = comments

        # check if user has voted each comment
        if self.request.user.is_authenticated:
            comments_in_page = [comment.id for comment in comments_list]
            all_points = Point.objects.filter(user=self.request.user)
            all_points = all_points.filter(comment_id__in=comments_in_page)
            positives = all_points.filter(value = 1)
            positives = positives.values_list('comment_id', flat=True)
            negatives = all_points.filter(value = -1)
            negatives = negatives.values_list('comment_id', flat=True)
            context["positives"] = positives
            context["negatives"] = negatives

        return context

class LinkUpdateView(UpdateView):
    template_name = 'links/link_create.html'
    form_class = LinkForm
    model = Link

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        link = self.get_object()
        if link.user != self.request.user:
            raise Http404("No tienes permiso para realizar esta acción.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('link_detail', kwargs={'pk': self.object.pk})

class LinkDeleteView(DeleteView):
    success_url = reverse_lazy('link_list')
    model = Link

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        link = self.get_object()
        if link.user != self.request.user:
            raise Http404("No tienes permiso para realizar esta acción.")
        return super().dispatch(request, *args, **kwargs)

class VoteView(FormView):
    form_class = VoteForm
    model = Vote

    def create_response(self, vdict=dict(), valid_form=True):
        response = HttpResponse(json.dumps(vdict), content_type='application/json')
        response.status = 200 if valid_form else 500
        return response

    def all_votes(self, link):
        all_votes = Vote.objects.filter(link=link)
        all_votes = all_votes.count()
        return all_votes

    def user_votes(self, link, user):
        user_votes = Vote.objects.filter(link=link, user=user)
        return user_votes

    def form_valid(self, form):
        f = form.save(commit=False)
        f.user = self.request.user
        f.link = get_object_or_404(Link, pk=self.kwargs['pk'])

        all_votes = self.all_votes(f.link)
        user_votes = self.user_votes(f.link, f.user)
        has_voted = user_votes.count() > 0
        if not has_voted: # add vote
           all_votes = all_votes + 1
           f.save()
        else: # remove vote
            all_votes = all_votes - 1
            user_votes[0].delete()
        result = {
            "id": f.link.id, # id of link that was clicked
            "votes": all_votes, # number of votes of the link
        }
        return self.create_response(result, True)
