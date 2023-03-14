from email.headerregistry import Group
from django.shortcuts import render, redirect
import requests
import traceback
from .forms import ProfileForm, SignUpForm
from .models import Profile
from django.conf import settings
# Flash messages
from django.contrib import messages
# Signup/Login stuff
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
# Paginator
from django.core.paginator import Paginator
# Filters
from .filters import UserFilter
# Logging
from django.http import HttpResponse
import logging
logger = logging.getLogger('ex_logger')
logger.info("core.views logger")

##############################
# Search model
from SearchEngine.WebpageSearcher import WebpageSearcher
searcher = WebpageSearcher()
searcher.add_link("https://techboomers.com/")
searcher.add_link("https://seniornet.org/")
searcher.add_link("https://www.hbc.bank/11-ways-to-check-if-a-website-is-legit-or-trying-to-scam-you/")
##############################

def search(request):
   # TODO: This should be made async
   query = request.GET.get('q', '')
   result = ""
   if query != '':
      url, keywords = searcher.search(query)
      if url is None or url == "no result":
         result = "No matches found"
      else:
         result = "Closest match: " + url + "\n Keywords: " + keywords
   return render(request, 'search.html', {
      "result" : result,
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
      return render(request, "accounts.html", {"page_obj" : page_obj, 'myFilter': myFilter, 'user':request.user})
   else:
      messages.error(request, 'You do not have permission to access this resource.')
      return redirect('/home')

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
         return redirect('/home')
   else:
      messages.error(request, 'You do not have permission to do that.')
      return redirect('/home')

@login_required
def update_account(request):
   record = request.user
   username = record.username
   if request.method == "POST":
      user_form = SignUpForm(request.POST, instance=record)
      
      user_form_valid = user_form.is_valid()
      if user_form_valid == False or user_form.cleaned_data['username'] != username:
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
         return redirect('/home')

      if request.method == "POST":
         profile_form = ProfileForm(request.POST, instance=record.profile)
         
         profile_form_valid = profile_form.is_valid()
         if profile_form_valid == False and len(profile_form.errors) > 0:
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
      return redirect('/home')

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
            "user_form" : form,
         })
   else:
      messages.error(request, 'You do not have permission to do that.')
      return redirect('/home')