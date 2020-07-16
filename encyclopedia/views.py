from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from markdown2 import Markdown
from . import util
from os.path import join
from django.core.files import File
from django.shortcuts import redirect
import re
import random

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    body = forms.CharField(label="Body", widget=forms.Textarea(attrs={'class': 'form-control'}), required=True)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def markdown_to_html(data):
    markdowner = Markdown()
    html = markdowner.convert(util.get_entry(data))
    return html

def entry(request, entry):
    try:
        display_entry = markdown_to_html(entry)
    except TypeError: 
        display_entry = "Requested page was not found"
    #get title needed for directing edit page request
    title = request.get_full_path()
    title = title.strip("/")
    return render(request, "encyclopedia/entry.html", {
        "entry": display_entry,
        "title": title
    })

def search(request):
    #get the data
    query = request.GET.get('q')
    #make it lowercase to make case insenstive search
    query = query.casefold()
    #get list of entires
    entries = util.list_entries()
    #create an empty list to be populated with partial query matches
    search_results = []
    #check if query matches an entry
    for entry in entries:
        entry = entry.casefold()
        if entry == query:
            entry = markdown_to_html(entry)
            #return a redirect to entry page
            return redirect("/" + query)
            #check if the query a substring of an entry
        elif query in entry:
            search_results.append(entry)
    print(search_results)
    return render(request, "encyclopedia/search_results.html", {
        "search_results": search_results   }) 

def newpage(request):
    if request.method == "POST":
        #get contents into varibles 
        title = request.POST.get('title')
        print(title)
        body = request.POST.get('body')
        #logic here to check if title = an entry in list of entry. 
        entries = util.list_entries()
        for entry in entries:
            print(entry)
            if entry == title:
                return render(request, "encyclopedia/error.html", {
                    "message": "Title already exists"
                })
        # Format Title to escape Markdown and add underscore
        #find # and remove from string
        filetitle = title
        for char in filetitle:
            if char == "#":
                filetitle = filetitle.replace("#", "")
        #check if first char is a space and remove it.
        filetitle = filetitle.strip()
        #replace whitespace with underscores
        filetitle = filetitle.replace(" ", "_")
        ##build path to the file.
        path = join("/Users/graemebarnes/Desktop/web50/wiki/entries/" + filetitle + ".md")
        #write to file
        with open(path, 'w') as f:
            newpage = File(f)
            newpage.write(title)
            newpage.write("\n")
            newpage.write("\n")
            newpage.write(body)
        #take user to new page
        return redirect("/" + filetitle)
    else:
        return render(request, "encyclopedia/newpage.html", {
            "form":NewPageForm()
        })

def editpage(request, title):
    if request.method == "POST": 
    #get the updated content
        body = request.POST['body']
        #open file 
        path = join("/Users/graemebarnes/Desktop/web50/wiki/entries/" + title + ".md")
        print(path)
        print(title)
        print(body)
        with open(path, 'r') as f:
            existingpage = File(f)
            existingpage = existingpage.readlines()
            filetitle = existingpage[0]
            print(filetitle)
        with open(path, 'w') as f:
            updatedpage = File(f)
            updatedpage.write(filetitle)
            updatedpage.write("\n")
            updatedpage.write("\n")
            updatedpage.write(body)
        return redirect("/" + title)
    else:
        content = util.get_entry(title)
        #clean data so only post content is in varible
        content = content.splitlines()
        content = content[2:]
        content = ''.join(content)
        return render(request, "encyclopedia/editpage.html", {
            "content": content,
            "title": title
        })

def randompage(request):
    #get list of entries
    entries = util.list_entries()
    #get a random one
    page = random.choice(entries)
    #redirect to random page
    return redirect("/" + page)
