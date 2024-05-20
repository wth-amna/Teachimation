from .models import Topic, User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import ProfileUpdateForm
from .forms import ProfileUpdateForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from .models import Topic
from .scrapper import scraper
# from .summarizer import summarize


User = get_user_model()


@login_required
def updateUser(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password")
            if password:
                user.set_password(password)
            user.save()
            update_session_auth_hash(request, user)  # Important to update session with new password
            return redirect('home')  # Redirect to home after successful update
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'base/updateuser.html', {'form': form})



@login_required(login_url='/login')
def home(request):
    return render(request, 'base/home.html')

def search_topics(query):
    topics = Topic.objects.filter(name__icontains=query)
    return topics


@login_required(login_url='/login')
@login_required(login_url='/login')
def search(request):
    query = request.GET.get('query', '').strip()
    if query:
            topics = search_topics(query)
            if topics: 
                # summary = topic.summary
                return render(request, 'base/lecture.html', {'topics': topics})
            else: 
                # If the topic does not exist, scrape the data
                urls = ["https://www.computerhope.com/", "https://www.geeksforgeeks.org/"]
                all_paragraphs = []
                for url in urls:
                     result = scraper(url, query)
                if result is not None:  # Check if scraper returns valid data
                    all_paragraphs.extend(result)
                else:
                    # Display message if topic does not exist
                    return render(request, 'base/lecture.html', {'message': "Topic not found. Please check your spelling or the data you're searching does not exist."})
                # Concatenate the scraped paragraphs into a single string
                scraped_data = ' '.join(all_paragraphs)
                # Save the scraped data to the database
                topics = Topic.objects.create(name=query, scraped_data=scraped_data)
                # Call the summarization command
                call_command('summarize')
                # Retrieve the updated topic with summary
                topics = Topic.objects.filter(name__icontains=query)
                return render(request, 'base/lecture.html',  {'topics': topics})
    else:
        return redirect('home')  # Redirect to home if no query is provided
    
def get_query(request):
    if request.method == 'GET':
        query = request.GET.get('query', '').strip()
        if query:
            topics = search_topics(query)
            if topics:
                # Convert topics to JSON and return as AJAX response
                return JsonResponse({'topics': list(topics)})
            else:
                # If the topic does not exist, scrape the data
                urls = ["https://www.computerhope.com/", "https://www.geeksforgeeks.org/"]
                all_paragraphs = []
                for url in urls:
                    result = scraper(url, query)
                    if result is not None:  # Check if scraper returns valid data
                        all_paragraphs.extend(result)

                if all_paragraphs:
                    # Save the scraped data to the database
                    scraped_data = ' '.join(all_paragraphs)
                    topics = Topic.objects.create(name=query, scraped_data=scraped_data)
                    topics.summary = ""
                    topics.save()
                    topics = Topic.objects.filter(name__icontains=query)
                    # Return JSON response with topics data
                    return render(request, 'base/lecture.html',  {'topics': topics})
                else:
                    # Return JSON response with error message
                    return JsonResponse({'error': "Topic not found. Please check your spelling or the data you're searching does not exist."}, status=404)
        else:
            # Return JSON response with error message
            return JsonResponse({'error': "No query provided."}, status=400)
    else:
        # For non-AJAX requests or other methods, redirect to home
        return redirect('home')



# @login_required(login_url='/login')
# def search(request):
#     query = request.GET.get('query', '').strip()
#     if query:
#         # Check if the topic exists in the database
#         try:
#             topic = search_topics(query)
#             summary = topic.summary
#             return render(request, 'base/lecture.html', {'summary': summary})
#         except Topic.DoesNotExist:
#             # If the topic does not exist, scrape the data
#             urls = ["https://www.computerhope.com/", "https://www.geeksforgeeks.org/"]
#             all_paragraphs = []
#             for url in urls:
#                 result = scrapper(url, query)
#                 all_paragraphs.extend(result)
#             # Concatenate the scraped paragraphs into a single string
#             scraped_data = ' '.join(all_paragraphs)
#             # Save the scraped data to the database
#             topic = Topic.objects.create(name=query, scraped_data=scraped_data)
#             # Call the summarization command
#             call_command('summarize')
#             # Retrieve the updated topic with summary
#             topic = Topic.objects.get(name__icontains=query)
#             summary = topic.summary
#             return render(request, 'base/lecture.html', {'summary': summary})
#     else:
#         return redirect('home')  # Redirect to home if no query is provided


# @login_required(login_url='/login')
# def search(request):
#     query = request.GET.get('query', '').strip()
#     if query:
#         topics = search_topics(query)
#         if not topics:
#             return render(request, 'base/lecture.html', {'error_message': 'Sorry, we don\'t have the topic.'})
#         else:
#             return render(request, 'base/lecture.html', {'topics': topics})
#     else:
#         return redirect('home')  # Redirect to home if no query is provided


@login_required(login_url='/login')
def topic(request):
    data = Topic.objects.all()
    return render(request, 'base/lecture.html', {'data': data})


def userProfile(request,pk):
    user = User.objects.get(id=pk)
    context = {'user':user}
    return render(request, 'base/profile.html',context)
    
def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST.get("username").lower()
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "base/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("home"))
        return render(request, "base/login.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        confirmation = request.POST.get("confirmation", "")
        
        # Check if username is empty
        if not username:
            return render(request, "base/signup.html", {"message": "Username is required."})
        
        # Ensure password matches confirmation
        if password != confirmation:
            return render(request, "base/signup.html", {"message": "Passwords must match."})
        
        try:
            # Attempt to create new user
            user = User.objects.create_user(username, email, password)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        except ValueError as e:
            # Handle the "The given username must be set" exception
            return render(request, "base/signup.html", {"message": str(e)})
        except IntegrityError:
            return render(request, "base/signup.html", {"message": "Username already taken."})
    else:
        return render(request, "base/signup.html", {"message": ""})