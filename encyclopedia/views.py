from django.shortcuts import render
from django.http import HttpResponse
from markdown2 import Markdown
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    try:
        markdowner = Markdown()
        display_entry = markdowner.convert(util.get_entry(entry))
    except TypeError: 
        display_entry = "Requested page was not found"
    return render(request, "encyclopedia/entry.html", {
        "entry": display_entry
    })

