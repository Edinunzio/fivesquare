from django import forms

from models import *


class StoreForm(forms.Form):
    name = forms.CharField(widget=forms.widgets.TextInput())
    description = forms.CharField(widget=forms.widgets.TextInput())
    address1 = forms.CharField(widget=forms.widgets.TextInput())
    city = forms.CharField(widget=forms.widgets.TextInput())
    state = forms.CharField(widget=forms.widgets.TextInput())
    zipcode = forms.CharField(widget=forms.widgets.TextInput())
    latitude = forms.CharField(widget=forms.widgets.TextInput())
    longitude = forms.CharField(widget=forms.widgets.TextInput())

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super(StoreForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['name'].initial = self.instance.name
            self.fields['description'].initial = self.instance.description
            self.fields['address1'].initial = self.instance.address1
            self.fields['city'].initial = self.instance.city
            self.fields['state'].initial = self.instance.state
            self.fields['zipcode'].initial = self.instance.zipcode
            self.fields['latitude'].initial = self.instance.latitude
            self.fields['longitude'].initial = self.instance.longitude

    def save(self, commit=True):
        post = self.instance if self.instance else Store()
        post.name = self.cleaned_data['name']
        post.description = self.cleaned_data['description']
        post.address1 = self.cleaned_data['address1']
        post.city = self.cleaned_data['city']
        post.state = self.cleaned_data['state']
        post.zipcode = self.cleaned_data['zipcode']
        post.latitude = self.cleaned_data['latitude']
        post.longitude = self.cleaned_data['longitude']
        if commit:
            post.save()

        return post


class ReviewForm(forms.Form):
    CHOICES = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'))
    title = forms.CharField(widget=forms.widgets.TextInput())
    text = forms.CharField(widget=forms.widgets.Textarea())
    tags = forms.CharField(widget=forms.widgets.TextInput())
    rating = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    store_id = forms.CharField(widget=forms.widgets.TextInput())

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super(ReviewForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['title'].initial = self.instance.title
            self.fields['text'].initial = self.instance.text
            self.fields['tags'].initial = self.instance.tags
            self.fields['rating'].initial = self.instance.rating
            self.fields['store_id'].initial = self.instance.store_id
            self.fields['date_modified'].initial = self.instance.date_modified

    def save(self, commit=True):
        date_modified = datetime.now
        post = self.instance if self.instance else Review()
        post.title = self.cleaned_data['title']
        post.text = self.cleaned_data['text']
        post.tags = self.cleaned_data['tags'].split(',')
        post.rating = self.cleaned_data['rating']
        post.store_id = self.cleaned_data['store_id']
        post.date_modified = date_modified

        if commit:
            post.save()

        return post
