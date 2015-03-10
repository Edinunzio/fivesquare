from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from fivesquare.settings import MY_LOCATION
from forms import *


class StoreListView(ListView):
    """
    List of Stores
    """

    def __init__(self):
        """
        Setup model and template data var
        :return:
        """
        self.model = Store
        self.location = Location
        self.context_object_name = "store_list"

    def get_template_names(self):
        return ["list.html"]


    def get_queryset(self, coord=MY_LOCATION, lm=None):
        """
        Retrieves all store documents

        :return:ListView of all stores
        """
        _posts = []
        db = Connection().geo_businesses

        if 'limit' in self.request.GET:
            lm = int(self.request.GET["limit"])
            for doc in db.places.find({"loc": {"$near": coord}}).limit(lm):
                repr(doc)
                _posts.append(doc)
        else:
            for doc in db.places.find({"loc": {"$near": coord}}):
                repr(doc)
                _posts.append(doc)

        posts = _posts
        return posts


class StoreDetailView(DetailView):
    """
    Individual Store Detail View
    """

    def __init__(self):
        """
        Setup models, template vars, and form
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
    """
    Updating store info view
    """
    def __init__(self):
        """
        Setup model, form, and template var
        :return:
        """
        self.model = Store
        self.form_class = StoreForm
        self.geo_index = GeoIndex
        self.context_object_name = "post"

    def get_template_names(self):
        return ["update.html"]

    def get_success_url(self):
        return reverse('list')

    def form_valid(self, form):
        """
        Validates and saves form data
        :param form: store info data
        :return:
        """
        self.object = form.save()
        messages.success(self.request, "The store has been updated.")
        return super(StoreUpdateView, self).form_valid(form)

    def get_object(self):
        """
        Gets current store info
        :return: store details
        """
        return self.model.objects(id=self.kwargs['pk'])[0]


class StoreCreateView(CreateView):
    """
    View to create new store
    """
    def __init__(self):
        """
        Setup model, form
        :return:
        """
        self.model = Store
        self.location = Location
        self.form_class = StoreForm

    def get_template_names(self):
        return ["create.html"]

    def get_success_url(self):
        return reverse('list')

    def form_valid(self, form):
        """
        Validates and saves form data input by user
        :param form:
        :return:
        """
        self.object = form.save(commit=False)
        messages.success(self.request, "The store has been posted.")
        return super(StoreCreateView, self).form_valid(form)


class StoreDeleteView(DeleteView):
    """
    Removes store
    """
    def __init__(self):
        """
        Setup model
        :return:
        """
        self.model = Store

    def get_success_url(self):
        return reverse('list')

    def get(self, *args, **kwargs):
        """
         Removes store while skipping confirmation page
        :param args:
        :param kwargs:
        :return:
        """
        return self.delete(self.request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Removes store
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, "The store has been removed.")
        return redirect(self.get_success_url())

    def get_object(self):
        return self.model.objects(id=self.kwargs['pk'])[0]


class ReviewDetailView(DetailView):
    """
    Individual view of a review.
    """
    def __init__(self):
        """
        Setup model, template var
        :return:
        """
        self.model = Review
        self.context_object_name = "review_detail"

    def get_template_names(self):
        return ["review_detail.html"]

    def get_object(self):
        return Review.objects(id=self.kwargs['pk'])[0]


class ReviewUpdateView(UpdateView):
    """
    View to edit review
    """
    def __init__(self):
        """
        Setup model, form, template var
        :return:
        """
        self.model = Review
        self.form_class = ReviewForm
        self.context_object_name = "review_update"

    def get_template_names(self):
        return ["update.html"]

    def get_success_url(self):
        return reverse('list')

    def form_valid(self, form):
        """
        Validates and saves form data
        :param form:
        :return:
        """
        self.object = form.save()
        messages.success(self.request, "The review has been updated.")
        return super(ReviewUpdateView, self).form_valid(form)

    def get_object(self):
        return self.model.objects(id=self.kwargs['pk'])[0]


class ReviewCreateView(CreateView):
    """
    View to create reviews
    """
    def __init__(self):
        """
        Setup model, form
        :return:
        """
        self.model = Review
        self.form_class = ReviewForm

    def get_template_names(self):
        return ["review.html"]

    def get_success_url(self):
        return reverse('list')

    def form_valid(self, form):
        """
        Validates and saves form data, and inserts timestamp into record
        :param form:
        :return:
        """
        self.date_modified = datetime.now
        self.object = form.save(commit=False)
        messages.success(self.request, "The review has been posted.")
        return super(ReviewCreateView, self).form_valid(form)


class ReviewDeleteView(DeleteView):
    """
    Removes Reviews
    """
    def __init__(self):
        """
        Setup model
        :return:
        """
        self.model = Review

    def get_success_url(self):
        return reverse('list')

    def get(self, *args, **kwargs):
        """
        Removes review while skipping confirmation page
        :param args:
        :param kwargs:
        :return:
        """
        return self.delete(self.request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Removes review from store
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, "The review has been removed.")
        return redirect(self.get_success_url())

    def get_object(self):
        return self.model.objects(id=self.kwargs['pk'])[0]