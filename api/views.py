from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from models import *
from forms import *

class ReviewListView(ListView):
    model = Review
    context_object_name = "review_list"

    def get_template_names(self):
        return ["list.html"]

    def get_queryset(self):
        posts = Review.objects
        if 'all_reviews' not in self.request.GET:
            posts = posts.filter(is_published=True)
        return posts

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm

    def get_template_names(self):
        return ["create.html"]

    def get_success_url(self):
        return reverse('list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        messages.success(self.request, "The review has been posted.")
        return super(ReviewCreateView, self).form_valid(form)

class ReviewDetailView(DetailView):
    model = Review
    context_object_name = "review"

    def get_template_names(self):
        return ["detail.html"]

    def get_object(self):
        return Review.objects(id=self.kwargs['pk'])[0]

class ReviewUpdateView(UpdateView):
    model = Review
    form_class = ReviewForm
    context_object_name = "review"

    def get_template_names(self):
        return ["update.html"]

    def get_success_url(self):
        return reverse('list')

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "The review has been updated.")
        return super(ReviewUpdateView, self).form_valid(form)

    def get_object(self):
        return Review.objects(id=self.kwargs['pk'])[0]

class ReviewDeleteView(DeleteView):
    model = Review

    def get_success_url(self):
        return reverse('list')

    def get(self, *args, **kwargs):
        """ Skip confirmation page """
        return self.delete(self.request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, "The review has been removed.")
        return redirect(self.get_success_url())

    def get_object(self):
        return Review.objects(id=self.kwargs['pk'])[0]