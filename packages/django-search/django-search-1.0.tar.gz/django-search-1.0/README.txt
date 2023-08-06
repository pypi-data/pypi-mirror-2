ABOUT
=====

django-search is a django reusable app to perform custom search over a queryset in a simple way using custom tags. It is inspired by the simplicity of django-pagination (other django reusable app you should use if you aren't) and it's use is very similar.

Install
=======

Install it as a normal python package using pip::

    pip install django-search

You can also download the zip, uncompress it and run::

    python setup.py install

Then you must add *search* app in your settings.py file and you are done::

    INSTALLED_APPS = (
            ...
            'search'
    )

Usage
=====

In order to use django-search in a template you must load search_tags::

    {% load search_tags %}

Then place the {% search %} tag where you want the search form to be displayed. The tag has this structure::

    {% search queryset field1 field2 ... %}

where *queryset* is a queryset object (not evaluated or sliced) and *field1 field2 ...* are any number of fields in your queryset model for the search to be performed. In example::

    {% search userlist username first_name last_name %}

will search a match for the search terms in the form input in user.username, user.first_name OR user.last_name (note the OR).

In deep
=======

How the search is performed
---------------------------

The string typed in the input field will be splitted by spaces having single and double quotes in account without matching case, so if the string is::

    John "tiny mouth" 'any term'

the queryset will be filtered so user.username contains *John* OR user.first_name contains *John* OR user.last_name contains *John* AND user.username contains *tiny mouth* OR user.first_name contains *tiny mouth* OR user.last_name contains *tiny mouth* AND user.username contains *any term* OR user.first_name contains *any term* OR user.last_name contains *any term*.

It's a simple search that returns less but more accurate results as user adds search terms.

How it works
------------

The search tag renders a template with a form using GET method that includes a text and a submit input. If the user adds a search string and clicks the button a parameter named *search* will be set in request.GET and your view will be called again. Then, in the second view run if the search tag finds that parameter it will filter the queryset using it's value as search terms.

Styling
-------

The inputs rendered have two classes, *search-text* and *search-button* so you can style them as you want.

Useful context variables
------------------------

The search tag puts two useful variables in context:

* **remove_search_link**: Has the link to remove the search parameter from GET keeping all other parameters that might be there so if the user hits it the queryset will be shown unfiltered again. It can be used (after the search tag) as::

    <a href="{{remove_search_link}}">Remove</a>

* **search_terms**: Has the seach string as it was typed by the user. It can be useful with *remove_search_link* to allow the user to know what is beeing applied to the queryset this way::

    {% if search_terms %}
        Searching by {{search_terms}}: <a href="{{remove_search_link}}">Remove</a>
    {% endif %}

