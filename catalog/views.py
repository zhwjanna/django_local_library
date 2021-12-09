from django.db import models
from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from .models import Book, Author, BookInstance, Genre

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_books_on_creativity = Book.objects.filter(title__icontains='imagination').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    
    num_genres = Genre.objects.count()

    num_visits = request.session.get('num_visits',0)
    request.session['num_visits'] = num_visits +1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_on_creativity': num_books_on_creativity,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

from django.views import generic

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author
    paginate_by = 10

class AdoptedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_adopted_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(candidate=self.request.user).filter(status__exact='d').order_by('id')

from django.contrib.auth.mixins import PermissionRequiredMixin

class AdoptedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_book_adopted'
    template_name = 'catalog/bookinstance_list_adopted_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='d').order_by('shippable_date')

import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import ExtendAdoptionForm

@login_required
@permission_required('catalog.can_mark_book_adopted', raise_exception=True)
def extended_adoption_staff(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = ExtendAdoptionForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.shippable_date = form.cleaned_data['extended_adoption_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-adopted') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_extended_adoption_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = ExtendAdoptionForm(initial={'extended_adoption_date': proposed_extended_adoption_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/adoption_extend_staff.html', context)

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.models import Author

class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_birth': '11/06/1898'}
    permission_required = 'catalog.can_mark_book_adopted'


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = 'catalog.can_mark_book_adopted'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_mark_book_adopted'

from catalog.models import Book

class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = ['title','author','summary','isbn','genre','language']
    permission_required = 'catalog.can_mark_book_adopted'

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = ['title','author','summary','isbn','genre','language']
    permission_required = 'catalog.can_mark_book_adopted'

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('all_adopted')
    permission_required = 'catalog.can_mark_book_adopted'
