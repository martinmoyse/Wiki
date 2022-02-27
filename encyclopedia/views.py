import random
from django.http.response import HttpResponseRedirect
from markdown2 import Markdown
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from . import util

class EditEntry(forms.Form):
    title = forms.CharField(required=False)
    content = forms.CharField()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    if(util.get_entry(entry) != None):
        markdowner = Markdown()
        return render(request, "encyclopedia/entry.html", {
            "entry": entry,
            "entries": util.list_entries(),
            "display": markdowner.convert(util.get_entry(entry))
        })
    return render(request, "encyclopedia/no_entry.html")

def random_entry(request):
    entries = util.list_entries()
    title = random.choices(entries)
    return redirect(reverse('entry', args=title))

def search(request):
    title = request.GET.get('q')
    entries = util.list_entries()
    if not title:
        return redirect(reverse('index'))

    elif title in entries:
        markdowner = Markdown()
        return render(request, "encyclopedia/entry.html", {
                "entry": title,
                "entries": entries,
                "display": markdowner.convert(util.get_entry(title))
            })
    else:
        suggestions = []
        for entry in util.list_entries():
            if title.upper() in entry.upper():
                suggestions.append(entry)
        if len(suggestions) == 0:
            return render(request, "encyclopedia/no_entry.html")
        return render(request, "encyclopedia/search.html", {
            "entries": suggestions
        })

def edit(request, entry):
    if request.method == "GET":
        form = EditEntry(request.POST)
        return render(request, "encyclopedia/edit.html", {
            "entry": entry,
            "display": util.get_entry(entry),
        })

    if request.method == "POST":
        form = EditEntry(request.POST)
        if form.is_valid():
            title = entry
            content = form.cleaned_data.get("content")
            util.save_entry(title=title, content=content)
            return HttpResponseRedirect(reverse('entry', args=[title]))

def create_entry(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create_entry.html")

    if request.method=="POST":
        form = EditEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            for entry in util.list_entries():
                if title.upper() == entry.upper():
                    return render(request,"encyclopedia/entry_exists.html", {'title': title})
            content = form.cleaned_data.get("content")
            util.save_entry(title=title, content=content)
            return HttpResponseRedirect(reverse('entry', args=[title]))