from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.files import File
import markdown2
import random


from . import util


class NewForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea(), label="content")


class EditPage(forms.Form):
    content = forms.CharField(widget=forms.Textarea(), label="content")

class Search(forms.Form):
    searched = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search'}), label="")



def index(request):
    if request.method == "POST":
        search_form = Search(request.POST)
        if search_form.is_valid():
            search = search_form.cleaned_data["searched"]
            if search in util.list_entries():
                entry = util.get_entry(search)
                markeddown = markdown2.Markdown()
                page = markeddown.convert(entry)
                return render(request, "encyclopedia/page.html",
                {"page" : page, "title" : search, "search_form" : Search()})
            else:
                compared_pages = []
                for page in util.list_entries():
                    if search.lower() in page.lower():
                        compared_pages.append(page)
                
                return render(request, "encyclopedia/search.html", {
                    "pages" : compared_pages, "search_form" : Search()
                })
        else:
            return render(request, "encyclopedia/index.html",{
                "search_form" : Search(), "entries" : util.list_entries()
            })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(), "search_form" : Search()
        })


def page(request, name):
    title = name
    if (name in util.list_entries()):
        markdowned = markdown2.Markdown()
        subject = util.get_entry(f"{name}")
        page = markdowned.convert(subject)

        return render(request, "encyclopedia/page.html", {
            "page": page, "title": title, "search_form" : Search()})
    else:
        return render(request, "encyclopedia/error.html", {
            "error": "Page not found", "search_form" : Search()})


def create(request):
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            # see if the subject already has a page
            if (title in util.list_entries()):
                return render(request, "encyclopedia/error.html", {
                    "error": "Page already exists."
                })
            # save it as a new file in markdown
            util.save_entry(title, content)
            markdowned = markdown2.Markdown()
            entry = util.get_entry(title)
            newPage = markdowned.convert(entry)
            return render(request, "encyclopedia/page.html", {
                "page": newPage, "title": title
            })
        else:
            return render(request, "{% url 'create' %}",
                          {"form": form})

    else:
        return render(request, "encyclopedia/create.html",
                      {"form": NewForm()})


def randompage(request):
    # choose random page
    all_pages = util.list_entries()
    random_page = random.choice(all_pages)
    # get page and change it to from markdown to html
    page = util.get_entry(random_page)
    markdowned = markdown2.Markdown()
    converted_page = markdowned.convert(page)
    return render(request, "encyclopedia/page.html", {
        "page": converted_page, "title": random_page,  "search_form" : Search()
    })


def editpage(request, name):
    if request.method == "POST":
        form = EditPage(request.POST)
        if form.is_valid():
            title = name
            content = form.cleaned_data["content"]
            # save it as a new file in markdown
            util.save_entry(title, content)
            markdowned = markdown2.Markdown()
            entry = util.get_entry(title)
            newPage = markdowned.convert(entry)
            return render(request, "encyclopedia/page.html", {
                "page": newPage, "title": title, "search_form" : Search()
            })
        else:
            return render(request, "{% url 'create' %}",
                          {"form": form})
    else:
        page = util.get_entry(name)
        title = name
        form = EditPage(initial={'content': page})
        print(form)
        return render(request, "encyclopedia/edit.html", {
            "page": page, "title": title, "form": form
        })


