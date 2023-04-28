# Time
import datetime
from django.utils import timezone
# Django
from SearchEngine.WebpageSearcher import WebpageSearcher
from django.shortcuts import render, redirect
from .forms import ProfileForm, SignUpForm, ResourceForm, CategoryForm
from .models import AnswerResource, Category
from django.conf import settings
from django.http import JsonResponse
# Flash messages
from django.contrib import messages
# Signup/Login stuff
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Paginator
from django.core.paginator import Paginator
# Filters
from .filters import UserFilter, ResourceFilter, CategoryFilter
# Logging
import logging
logger = logging.getLogger('ex_logger')
logger.info("core.views logger")

##############################
# Search model
searcher = WebpageSearcher()
AUTOCOMPLETE_MAX_RESULTS = 5
FAQ_MAX_RESULTS = 5
##############################


def thumbs_up_clicked(request):
    query = request.GET.get('title', '')
    resource = AnswerResource.objects.all().filter(title=query).first()
    if resource is None:
        return redirect('/search')
    resource.thumbsUps = resource.thumbsUps + 1
    print(resource.thumbsUps)
    resource.save()
    return redirect('/search')


def resource_clicked(request):
    query = request.GET.get('title', '')
    resource = AnswerResource.objects.all().filter(title=query).first()
    if resource is None:
        return redirect('/search')
    resource.clicks = resource.clicks + 1
    resource.save()
    return redirect('/search')


def resource_appeared(request):
    query = request.GET.get('title', '')
    resource = AnswerResource.objects.all().filter(title=query).first()
    if resource is None:
        return redirect('/search')
    resource.appearances = resource.appearances + 1
    resource.save()
    return redirect('/search')


def faq_for_category(category):
    if category is None:
        return list(AnswerResource.objects.order_by('-appearances').values()[:FAQ_MAX_RESULTS])

    return list(AnswerResource.objects.filter(categories__in=[category]).order_by('-appearances').values()[:FAQ_MAX_RESULTS])


def get_faq(request):
    category_name = request.GET.get('category', None)

    category = None
    if category_name is not None:
        category = Category.objects.filter(category_name=category_name).first()

    return JsonResponse({"faq": faq_for_category(category)})


def autocomplete_search(request):
    titles = list()
    if 'term' in request.GET:
        query = request.GET.get('term')
        category = request.GET.get('c', '')
        # if no category was actually selected
        if category == "Category search" or category == "Categoría":
            category = ""
        autocomplete_results = None
        category_object = None
        if category != '':
            # Safely handles invalid input -- even if the user manually changes the "?c=" field
            # to a category that doesn't exist, it will not filter on any category and return all matches
            category_object = Category.objects.all().filter(category_name=category).first()
        # Using the searcher
        if query != '':
            autocomplete_results = searcher.search(query, category_object)
            if not len(autocomplete_results):
                # Using just the title if no results came from the seracher
                autocomplete_results = AnswerResource.objects.filter(title__icontains=query)
                if category != '':
                    autocomplete_results = [resource for resource in autocomplete_results if category_object in list(resource.categories.all())]
        for resource in autocomplete_results:
            titles.append(resource.title)
    return JsonResponse(titles[:AUTOCOMPLETE_MAX_RESULTS], safe=False)


def search(request):
    # TODO: This should be made async
    query = request.GET.get('q', '')
    category = request.GET.get('c', '')
    results = None
    category_object = None
    faq = None

    if category != '':
        # Safely handles invalid input -- even if the user manually changes the "?c=" field
        # to a category that doesn't exist, it will not filter on any category and return all matches
        category_object = Category.objects.all().filter(category_name=category).first()

    if query == '':
        faq = faq_for_category(category_object)
    else:
        results = searcher.search(query, category_object)

    categories = Category.objects.all()

    return render(request, 'search.html', {
        "query": query,
        "results": results,
        "categories": categories,
        "faq": faq
    })


@login_required
def accounts(request):
    if request.user.is_superuser:
        records = User.objects.all().order_by('-last_login')

        myFilter = UserFilter(request.GET, queryset=records)
        records = myFilter.qs

        paginator = Paginator(records, settings.PAGINATOR_COUNT)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "accounts.html", {"page_obj": page_obj, 'myFilter': myFilter, 'user': request.user})
    else:
        messages.error(request, 'You do not have permission to access this resource.')
        return redirect('/search')


@login_required
def account_redirect(request):
    current_user = request.user
    return redirect('/account/' + str(current_user.id))


@login_required
def account(request, id):
    if request.user.id == id or request.user.is_superuser:
        try:
            current_user = User.objects.get(id=id)
            profile_form = ProfileForm(instance=request.user.profile)
            return render(request, "account.html", {'user': request.user, 'view_user': current_user, 'profile_form': profile_form})
        except:
            messages.error(request, 'Invalid user ID.')
            return redirect('/accounts')
    else:
        messages.error(request, 'You do not have permission to do that.')
        return redirect('/search')


@login_required
def update_account(request):
    record = request.user
    username = record.username
    if request.method == "POST":
        user_form = SignUpForm(request.POST, instance=record)

        user_form_valid = user_form.is_valid()
        if user_form_valid is False or user_form.cleaned_data['username'] != username:
            if len(user_form.errors) > 0:
                messages.error(request, user_form.errors)
            else:
                messages.error(request, 'Update failed.')
            return redirect('/account')
        else:
            user_form.save()
            messages.success(request, 'Updated successfully. Please re-login.')
            return redirect('/account')
    else:
        user_form = SignUpForm(instance=record)
        return render(request, 'update_account.html', {
            'user_form': user_form,
            'requester': request.user
        })


@login_required
def update_profile(request, id):
    if request.user.id == id or request.user.is_superuser:
        record = None
        try:
            # Flow: user record exists
            record = User.objects.get(id=id)
        except:
            messages.error(request, 'This user does not exist.')
            return redirect('/accounts')

        if request.method == "POST":
            profile_form = ProfileForm(request.POST, instance=record.profile)

            profile_form_valid = profile_form.is_valid()
            if profile_form_valid is False and len(profile_form.errors) > 0:
                if len(profile_form.errors) > 0:
                    messages.error(request, profile_form.errors)
                return redirect('/update_profile/' + str(id))
            else:
                profile_form.save()
                messages.success(request, 'Account updated successfully.')
                return redirect('/account/' + str(id))
        else:
            profile_form = ProfileForm(instance=record.profile)
            return render(request, 'update_profile.html', {
                'profile_form': profile_form,
                'requester': request.user
            })
    else:
        messages.error(request, 'You do not have permission to do that.')
        return redirect('/search')


@login_required
def signup(request):
    if request.user.is_superuser:
        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.refresh_from_db()
                messages.success(request, "User " + user.username + " created successfully. They may now login with the password you supplied.")
                return redirect('/accounts')
            else:
                messages.error(request, form.errors)
                return redirect('/signup')
        else:
            form = SignUpForm()
        return render(request, "signup.html", {
            "user_form": form,
        })
    else:
        messages.error(request, 'You do not have permission to do that.')
        return redirect('/search')


@login_required
def new_resource(request):
    if request.method == "POST":
        # Create
        form = ResourceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resource created successfully')
            searcher.update_search_engine()
            return redirect('/resources')
        else:
            return render(request, "resource_form.html", {
                "form": form
            })
    else:
        # Render new form
        form = ResourceForm()
        return render(request, "resource_form.html", {
            "form": form
        })


@login_required
def update_resource(request, id):
    print("HELLO THERE ARE   ")
    record = None
    try:
        record = AnswerResource.objects.get(id=id)
    except:
        messages.error(request, 'This resource does not exist.')
        return redirect('/resources')

    if request.method == "POST":
        resource_form = ResourceForm(request.POST, instance=record)
        if resource_form.is_valid():
            record = resource_form.save()
            record.updated = datetime.datetime.now(tz=timezone.utc)
            record.save()
            messages.success(request, 'Resource updated successfully.')
            searcher.update_search_engine()
            return redirect('/resources')
        else:
            return render(request, "resource_form.html", {
                "form": resource_form
            })
    else:
        resource_form = ResourceForm(instance=record)
        return render(request, 'resource_form.html', {
            'form': resource_form,
        })


@login_required
def delete_resource(request, id):
    record = None
    try:
        record = AnswerResource.objects.get(id=id)
    except:
        messages.error(request, 'Invalid resource.')
        return redirect('/resources')

    try:
        record.delete()
        messages.success(request, 'Resource deleted successfully.')
        searcher.update_search_engine()
        return redirect('/resources')
    except Exception as e:
        messages.error(request, 'Deletion failed, see error: ' + str(e))
    return redirect('/resources')


@login_required
def view_resources(request):
    records = AnswerResource.objects.all().order_by('-updated')

    myFilter = ResourceFilter(request.GET, queryset=records)
    records = myFilter.qs

    paginator = Paginator(records, settings.PAGINATOR_COUNT + 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "resources.html", {"page_obj": page_obj, "myFilter": myFilter, "user": request.user})


@login_required
def new_category(request):
    if request.method == "POST":
        # Create
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully')
            return redirect('/categories')
        else:
            return render(request, "category_form.html", {
                "form": form
            })
    else:
        # Render new form
        form = CategoryForm()
        return render(request, "category_form.html", {
            "form": form
        })


@login_required
def update_category(request, id):
    record = None
    try:
        record = Category.objects.get(id=id)
    except:
        messages.error(request, 'This category does not exist.')
        return redirect('/categories')

    if request.method == "POST":
        category_form = CategoryForm(request.POST, instance=record)
        if category_form.is_valid():
            record = category_form.save()
            record.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('/categories')
        else:
            return render(request, "category_form.html", {
                "form": category_form
            })
    else:
        category_form = CategoryForm(instance=record)
        return render(request, 'category_form.html', {
            'form': category_form,
        })


@login_required
def delete_category(request, id):
    record = None
    try:
        record = Category.objects.get(id=id)
    except:
        messages.error(request, 'Invalid category.')
        return redirect('/categories')

    try:
        record.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('/categories')
    except Exception as e:
        messages.error(request, 'Deletion failed, see error: ' + str(e))
    return redirect('/categories')


@login_required
def view_categories(request):
    records = Category.objects.all()

    myFilter = CategoryFilter(request.GET, queryset=records)
    records = myFilter.qs

    paginator = Paginator(records, settings.PAGINATOR_COUNT + 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "categories.html", {"page_obj": page_obj, "myFilter": myFilter, "user": request.user})
