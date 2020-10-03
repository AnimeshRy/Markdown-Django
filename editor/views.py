import re
from django.http import request, HttpResponseRedirect
from django.shortcuts import render
from . import storage
from markdown2 import Markdown
from django import forms
from django.urls import reverse
from random import choice

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry title", widget=forms.TextInput(
        attrs={'class': 'form-control col-md-8 col-lg-8', 'autocomplete': 'off'}))
    content = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control col-md-8 col-lg-8', 'rows': 20}))
    edit = forms.BooleanField(
        initial=False, widget=forms.HiddenInput(), required=False)

def index(request):
    return render(request, "editor/index.html", context={
        "entries" : storage.list_entries(),
        "length": len(storage.list_entries())
    })

def show_entry(request, entry):
    markdowner = Markdown()
    entrypage = storage.read_entry(entry)
    if entrypage is None:
        return render(request, "editor/error.html", context={
            "entrytitle": entry.capitalize()
        })
    else:
        return render(request, "editor/entry.html", context={
        "entry":markdowner.convert(entrypage),
        "entrytitle": entry.capitalize()
    })

def newEntry(request):
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if(storage.read_entry(title) is None or form.cleaned_data["edit"] is True):
                storage.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))
            else:
                return render(request, "editor/newEntry.html", {
                    "form": form,
                    "existing": True,
                    "entry": title
                })
        else:
            return render(request, "editor/newEntry.html", {
                "form": form,
                "existing": False
            })
    else:
        return render(request, "editor/newEntry.html", {
            "form": NewEntryForm(),
            "existing": False
        })

def random_entry(request):
    entries = storage.list_entries()
    randomEntry = choice(entries)
    return HttpResponseRedirect(reverse("entry", kwargs={'entry': randomEntry}))

def search(request):
    value = request.GET.get('q')
    if(storage.read_entry(value) is not None):
        return HttpResponseRedirect(reverse("entry", kwargs={'entry': value}))
    else:
        subentries = []
        allentries = storage.list_entries()
        for entry in allentries:
            if value.upper() in entry.upper():
                subentries.append(entry)
        return render(request, 'editor/index.html', context={
            "entries": subentries,
            "search": True,
            "value": value,
        })


def delete(request, entry):
    storage.delete_entry(entry)
    return HttpResponseRedirect(reverse("index"))


def edit(request, entry):
    entryPage = storage.read_entry(entry)
    if entryPage is None:
        return render(request, "editor/error.html", {
            "entrytitle": entry
        })
    else:
        form = NewEntryForm()
        form.fields["title"].initial = entry
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["content"].initial = entryPage
        form.fields["edit"].initial = True
        return render(request, "editor/newEntry.html", {
            "form": form,
            "edit": form.fields["edit"].initial,
            "entrytitle": form.fields["title"].initial
        })
