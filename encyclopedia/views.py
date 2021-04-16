from django.shortcuts import render
from django.http import HttpResponse
from . import util
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import markdown2
import secrets

entryList = util.list_entries()
class EntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content")
    #submit = forms.CharField(label="Submit")

class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

def index(request):
    if request.method == "POST":
        #search
        search = request.POST.get('q') #searched data
        if search in entryList:
            return entry(request, search)
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": [s for s in entryList if search.lower() in s.lower()]
            })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entryName):
    if entryName not in entryList:
        return render(request, "encyclopedia/error.html")
    
    return render(request, "encyclopedia/entry.html", {
        "name": entryName,
        "content": markdown2.markdown(util.get_entry(entryName)),
    })

def add(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            if title in entryList:
                return render(request, "encyclopedia/add.html",{
                    "form": form,
                    "message": "Error: This entry already exists"
                })
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("index"))

            
        else:
            return render(request, "tasks/add.html",{
                "form": form
            })

    return render(request, "encyclopedia/add.html", {
        "form": EntryForm()
        })


def random(request):
    return entry(request, secrets.choice(entryList))

def edit(request, entryName):
    #name = entryName
    content = util.get_entry(entryName)
    form = EditForm(initial={"content":content})
    if request.method == "POST":
        #postForm = EditForm(request.POST)
        #util.save_entry(entryName, postForm.data["content"])
        util.save_entry(entryName, request.POST["new_content"])
        return entry(request, entryName)


    
    return render(request, "encyclopedia/edit.html", {
        "name": entryName,
        "content": content,
        "form": form,
    })




        
    