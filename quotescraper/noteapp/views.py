from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth.decorators import login_required

from .utils import get_mongodb
from .models import Tag, Author, Quote
from .forms import RegisterAuthor, RegisterQuote, RegisterTag


popular_tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]
popular_tags = [(tag, 2.75 * tag.num_quotes) for tag in popular_tags]


def main(request, page=1):
    """
    The main function is the entry point for the application.
    It returns a rendered template with context variables that are used in the template.
    
    
    :param request: Get the request object
    :param page: Specify the page number of the quotes to be displayed
    :return: A rendered template
    :doc-author: Trelent
    """
    context = {}
    # db = get_mongodb()
    # quotes = db.quotes.find()
    quotes = Quote.objects.all()

    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)

    context['popular_tags'] = popular_tags
    context['quotes'] = quotes_on_page
    return render(request, 'quotes/index.html', context=context)


def author_detail(request, author_id):
    """
    The author_detail function takes a request and an author_id as arguments.
    It then uses the Author model to get the author with that id, and renders
    the quotes/author.html template with that author object.
    
    :param request: Pass information from the client to the server
    :param author_id: Get the author object from the database
    :return: The author
    :doc-author: Trelent
    """
    author = Author.objects.get(pk=author_id)
    return render(request, 'quotes/author.html', context={'author': author})


def selected_tag(request, tag_name, page=1):
    """
    The selected_tag function takes a request and tag_name as arguments.
    It then gets the Tag object with the name of tag_name, and uses it to get all quotes that have that tag.
    It then creates a context dictionary containing those quotes, along with the popular tags (which are used in every page).
    Finally, it renders 'quotes/tags.html' using this context.
    
    :param request: Get the request object
    :param tag_name: Get the tag object from the database
    :param page: Determine which page of results to show
    :return: The quotes that have the selected tag
    :doc-author: Trelent
    """
    tag = Tag.objects.get(name=tag_name)
    quotes = Quote.objects.filter(tags=tag)
    context = {
        'tag': tag,
        'quotes': quotes,
        'popular_tags': popular_tags,
    }
    return render(request, 'quotes/tags.html', context=context)


@login_required
def add_author(request):
    """
    The add_author function is a view that allows the user to add an author.
    It takes in a request and returns either the form for adding an author or, if
    the form has been filled out correctly, it redirects to the root page.
    
    :param request: Get the request from the user
    :return: A render function that renders the add_author
    :doc-author: Trelent
    """
    if request.method == 'POST':
        form = RegisterAuthor(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/add_author.html', context={'form': form})

    return render(request, 'quotes/add_author.html', context={'form': RegisterAuthor()})


@login_required
def add_quote(request):
    """
    The add_quote function is a view that allows users to add quotes.
    It takes in the request object and returns an HTML page with a form for adding quotes.
    If the user submits the form, it will save their quote to our database.
    
    :param request: Get the current user
    :return: A redirect to the root page if the form is valid
    :doc-author: Trelent
    """
    if request.method == 'POST':
        form = RegisterQuote(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.user = request.user
            new_quote.save()
            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/add_quote.html', context={'form': form})

    return render(request, 'quotes/add_quote.html', context={'form': RegisterQuote()})

