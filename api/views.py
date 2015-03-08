from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from forms import *


class StoreListView(ListView):
    model = Store
    context_object_name = "store_list"

    def get_template_names(self):
        return ["list.html"]

    def get_queryset(self):
        posts = Store.objects
        """if 'all_reviews' not in self.request.GET:
            posts = posts.filter(is_published=True)"""
        return posts


class StoreDetailView(DetailView):
    model = Store
    context_object_name = "store"

    def get_template_names(self):
        return ["detail.html"]

    def get_object(self):
        return Store.objects(id=self.kwargs['pk'])[0]

class ReviewUpdateView(UpdateView):
    model = Review
    form_class = ReviewForm
    context_object_name = "post"

    def get_template_names(self):
        return ["update.html"]

    def get_success_url(self):
        return reverse('list')

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "The review has been updated.")
        return super(ReviewUpdateView, self).form_valid(form)

    def get_object(self):
        return Store.objects(id=self.kwargs['pk'])[0]


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