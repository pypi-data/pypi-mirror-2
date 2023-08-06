from logging import getLogger

from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage
from django.http import *
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404, redirect
from django.template import loader, RequestContext
from django.views.generic import list_detail, simple

from bookreader.models import Book, Page



log = getLogger('bookreader.views.book')

def browse(request, **kwargs):
    kwargs.setdefault('template_object_name','book')
    kwargs.setdefault('queryset', Book.objects.all())
    return list_detail.object_list(request, **kwargs)

def view(request, object_id, **kwargs):
    kwargs.setdefault('template_object_name','book')
    kwargs.setdefault('queryset', Book.objects.all())
    kwargs['object_id'] = object_id
    return list_detail.object_detail(request, **kwargs)

def read(request, object_id, **kwargs):
    kwargs.setdefault('paginate_by', 2)
    kwargs.setdefault('page', None)
    kwargs.setdefault('allow_empty', True)
    kwargs.setdefault('template_name', 'bookreader/book_read.html')
    kwargs.setdefault('template_loader', loader)
    kwargs.setdefault('extra_context', {})
    kwargs.setdefault('context_processors',None)
    kwargs.setdefault('template_object_name', 'object')
    kwargs.setdefault('mimetype',None)
    
    book = get_object_or_404(Book, pk=object_id)
    
    if book.offset_reading_view:
        pages = [None] + list(book.pages.all())
    else:
        pages = book.pages.all()
    
    if kwargs['paginate_by']:
        paginator = Paginator(pages, kwargs['paginate_by'],
                              allow_empty_first_page=kwargs['allow_empty'])
        if not kwargs['page']:
            kwargs['page'] = request.GET.get('page', 1)
        try:
            page_number = int(kwargs['page'])
        except ValueError:
            if kwargs['page'] == 'last':
                page_number = paginator.num_pages
            else:
                # Page is not 'last', nor can it be converted to an int.
                raise Http404
        try:
            page_obj = paginator.page(page_number)
        except InvalidPage:
            raise Http404
        c = RequestContext(request, {
            '%s_list' % kwargs['template_object_name']: page_obj.object_list,
            'paginator': paginator,
            'page_obj': page_obj,
            'book': book,
            'is_paginated': True,
        }, kwargs['context_processors'])
    else:
        c = RequestContext(request, {
            '%s_list' % kwargs['template_object_name']: pages,
            'paginator': None,
            'page_obj': None,
            'book': book,
            'is_paginated': False,
        }, context_processors)
        if not allow_empty and len(pages) == 0:
            raise Http404
    for key, value in kwargs['extra_context'].items():
        if callable(value):
            c[key] = value()
        else:
            c[key] = value
    
    t = kwargs['template_loader'].get_template(kwargs['template_name'])
    return HttpResponse(t.render(c), mimetype=kwargs['mimetype'])

def pages(request, object_id, **kwargs):
    kwargs.setdefault('extra_context', {})
    kwargs.setdefault('template_name', 'bookreader/book_pages.html')
    
    book = get_object_or_404(Book, pk=object_id)
    
    sequence = request.REQUEST.get('sequence',None)
    
    kwargs['extra_context']['book'] = book
    if sequence:
        kwargs['extra_context']['sequence'] = sequence
        try:
            kwargs['extra_context']['sequence_page'] = book.pages.get(sequence=sequence)
        except Page.DoesNotExist:
            print 'invalid sequence!'
            pass
    
    return list_detail.object_list(request, book.pages.all(), **kwargs)

def page(request, object_id, sequence, **kwargs):
    book = get_object_or_404(Book, pk=object_id)
    
    try:
        page= book.pages.get(sequence=sequence)
    except Page.DoesNotExist:
        raise Http404('Invalid sequence for %s' % (str(book),))
    
    return list_detail.object_detail(book.pages.all(), object_id=page.pk,
                                     **kwargs)

def compare(request, **kwargs):
    kwargs.setdefault('template', 'bookreader/book_comparison.html')
    return simple.direct_to_template(request, **kwargs)

def compare_portlet(request, **kwargs):
    kwargs.setdefault('template', 'bookreader/book_comparison_portlet.html')
    return simple.direct_to_template(request, **kwargs)

def add_to_compare(request, object_id, **kwargs):
    book = get_object_or_404(Book, pk=object_id)
    
    request.session.setdefault(settings.BOOKREADER_COMPARISON_SESSION_KEY,[])
    
    response = '{}'
    
    if book.identifier not in request.session[settings.BOOKREADER_COMPARISON_SESSION_KEY]:
        request.session[settings.BOOKREADER_COMPARISON_SESSION_KEY].append(book.identifier)
        request.session.modified = True
        response = '{added: "%s"}' % (book.identifier,)
    
    if request.is_ajax():
        return HttpResponse(response, mimetype='application/javascript')
    
    messages.add_message(request, messages.INFO, 'Added "%s" to comparison list' % (book.title,))
    
    if 'redirect' in request.GET:
        return HttpResponseRedirect(request.GET['redirect'])
    
    return compare(request, **kwargs)

def remove_from_compare(request, object_id, **kwargs):
    book = get_object_or_404(Book, pk=object_id)
    
    request.session.setdefault(settings.BOOKREADER_COMPARISON_SESSION_KEY,[])
    response = '{}'
    
    if book.identifier in  request.session[settings.BOOKREADER_COMPARISON_SESSION_KEY]:
        request.session[settings.BOOKREADER_COMPARISON_SESSION_KEY].remove(book.identifier)
        request.session.modified = True
        response = '{removed: "%s"}' % (book.identifier,)
    
    if request.is_ajax():
        return HttpResponse(response, mimetype='application/javascript')
    
    messages.add_message(request, messages.INFO, 'Removed "%s" from comparison list' % (book.title,))
    
    if 'redirect' in request.GET:
        return HttpResponseRedirect(request.GET['redirect'])
    
    return compare(request, **kwargs)

def reset_compare(request, **kwargs):
    request.session[settings.BOOKREADER_COMPARISON_SESSION_KEY] = []
    
    if request.is_ajax():
        return HttpResponse('{reset: 1}', mimetype='application/javascript')
    
    messages.add_message(request, messages.INFO, 'Reset comparison list')
    
    if 'redirect' in request.GET:
        return HttpResponseRedirect(request.GET['redirect'])
    
    return compare(request, **kwargs)

