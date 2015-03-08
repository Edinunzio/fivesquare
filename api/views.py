from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from forms import *


class StoreListView(ListView):
    """
    List of Stores
    """

    def __init__(self):
        """
        setup model and template data var
        :return:
        """
        self.model = Store
        self.context_object_name = "store_list"

    def get_template_names(self):
        return ["list.html"]

    def get_queryset(self):
        """
        Retrieves all store documents
        #TODO: reduce through geospatial filter AND be wary of reducing return for larger scaled potentials
        :return:ListView of all stores
        """
        # TODO: geospatial filter
        posts = self.model.objects
        return posts


class StoreDetailView(DetailView):
    """
    Individual Store Detail View
    """

    def __init__(self):
        """
        setup models, template vars, and form
        :return:
        """
        self.model = Store
        self.context_object_name = "store"
        self.reviews = Review
        self.review_form = ReviewForm()

    def get_template_names(self):
        return ["detail.html"]

    def get_object(self):
        """
        Returns reviews filtered by store id, ordered by date modified
        :return: store details, store reviews, store_id, form inputs, tags, ratings
        """
        store_id = self.kwargs['pk']
        details = self.model.objects(id=store_id)[0]
        reviews = self.reviews.objects.all().filter(store_id=store_id).order_by('-date_modified')
        tags = self.reviews.objects.filter(store_id=store_id).distinct('tags')
        ratings = reviews.average('rating')
        form = self.review_form

        return details, reviews, store_id, form, tags, ratings


class StoreUpdateView(UpdateView):
    def __init__(self):
        self.model = Store
        self.form_class = StoreForm
        self.context_object_name = "post"

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
    def __init__(self):
        self.model = Store
        self.form_class = StoreForm

    def get_template_names(self):
        return ["create.html"]

    def get_success_url(self):
        return reverse('list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        messages.success(self.request, "The store has been posted.")
        return super(StoreCreateView, self).form_valid(form)


class StoreDeleteView(DeleteView):
    def __init__(self):
        self.model = Store

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
    def __init__(self):
        self.model = Review
        self.context_object_name = "review_detail"

    def get_template_names(self):
        return ["review_detail.html"]

    def get_object(self):
        return Review.objects(id=self.kwargs['pk'])[0]


class ReviewUpdateView(UpdateView):
    def __init__(self):
        self.model = Review
        self.form_class = ReviewForm
        self.context_object_name = "review_update"

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
    def __init__(self):
        self.model = Review
        self.form_class = ReviewForm

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
    def __init__(self):
        self.model = Review

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