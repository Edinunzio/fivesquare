from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from forms import *


class ReviewListView(ListView):
    model = Review
    context_object_name = "review_list"

    def get_template_names(self):
        return ["list.html"]

    def get_queryset(self, store_id):
        posts = Review.objects
        return posts


class StoreListView(ListView):
    model = Store
    context_object_name = "store_list"

    def get_template_names(self):
        return ["list.html"]

    def get_queryset(self):
        posts = Store.objects
        return posts


class StoreDetailView(DetailView):
    model = Store
    context_object_name = "store"
    reviews = Review
    review_form = ReviewForm()

    def get_template_names(self):
        return ["detail.html"]

    def get_object(self):
        id = self.kwargs['pk']
        details = Store.objects(id=id)[0]
        reviews = Review.objects.all().filter(store_id=id).order_by('-date_modified')
        tags = reviews.fields('tags')
        # reviews = self.reviews.objects#(store_id=id)
        # self.review_form.store_id = id
        form = self.review_form

        return details, reviews, id, form, tags

    """def get_queryset(self):
        posts = Review.objects(id=self.kwargs['pk'])[0]
        return posts"""


class StoreUpdateView(UpdateView):
    model = Store
    form_class = StoreForm
    context_object_name = "post"

    def get_template_names(self):
        return ["update.html"]

    def get_success_url(self):
        return reverse('list')

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "The store has been updated.")
        return super(StoreUpdateView, self).form_valid(form)

    def get_object(self):
        return Store.objects(id=self.kwargs['pk'])[0]


class StoreCreateView(CreateView):
    model = Store
    form_class = StoreForm

    def get_template_names(self):
        return ["create.html"]

    def get_success_url(self):
        return reverse('list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # self.object.user = self.request.user
        messages.success(self.request, "The store has been posted.")
        return super(StoreCreateView, self).form_valid(form)


class StoreDeleteView(DeleteView):
    model = Store

    def get_success_url(self):
        return reverse('list')

    def get(self, *args, **kwargs):
        """ Skip confirmation page """
        return self.delete(self.request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, "The store has been removed.")
        return redirect(self.get_success_url())

    def get_object(self):
        return Store.objects(id=self.kwargs['pk'])[0]



class ReviewDetailView(DetailView):
    model = Review
    context_object_name = "review_detail"

    def get_template_names(self):
        return ["review_detail.html"]

    def get_object(self):
        objs = Review.objects(id=self.kwargs['pk'])[0]
        return objs

class ReviewUpdateView(UpdateView):
    model = Review
    form_class = ReviewForm
    context_object_name = "review_update"

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


class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm

    def get_template_names(self):
        return ["review.html"]

    def get_success_url(self):
        return reverse('list')

    def form_valid(self, form):
        self.date_modified = datetime.now
        self.object = form.save(commit=False)
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