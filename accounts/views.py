from django.contrib.auth import authenticate, login, logout  # Auth related functions
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, AnonymousUser  # User models
from django.core.exceptions import ValidationError  # Exceptions
from django.core.validators import validate_email  # Validators
from django.shortcuts import render, redirect  # Shortcut functions
from django.urls import reverse  # URL resolution
from django.views import View  # Class-based views

# Import models from your apps
from .models import CustomUser  # Adjust the import path as necessary
from videos.models import CommentRating, Video  # Adjust the import path as necessary

import os  # Standard library imports should usually be at the top
  # Assuming CustomUser is in the same app

class Login(View):
    template_name = 'accounts/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        print("Login view post method called")
        username = request.POST.get('username')
        password = request.POST.get('password')

        print("Username:", username)
        print("Password:", password)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Authentication was successful, log the user in
            login(request, user)

            # Assuming you have a way to distinguish CustomUser and its properties
            if isinstance(user, CustomUser):
                if user.is_superuser:
                    print("User is a superuser")
                    # Redirect superusers to the dashboard
                    return redirect('dashboard')
                else:
                    print("User is NOT a superuser")
                    # Redirect regular users to the profile page
                    return redirect('profile')
            else:
                print("User is NOT an instance of CustomUser")
        else:
            print("Authentication failed")
            # Authentication failed, show an error message
            error_message = "Invalid username or password"
            return render(request, self.template_name, {'error_message': error_message})

    
@login_required  # Use this decorator to ensure the user is logged in
def profile_view(request):
    user = request.user
    videos = Video.objects.all()

    # Fetch the counts of winning and losing trades
    
    context = {
        'user': user,
        'videos': videos
                
    }

    return render(request, 'accounts/profile.html', context)



from django.shortcuts import render
@login_required
def admin_dashboard(request):
    # Fetch all CustomUser objects
    users = CustomUser.objects.all()

    # Fetch all video objects
    videos = Video.objects.all()

    # Fetch all comment rating objects
    comment_ratings = CommentRating.objects.all()

    context = {
        'users': users,
        'videos': videos,
        'comment_ratings': comment_ratings,
    }

    return render(request, 'accounts/admin_dashboard.html', context)


def signup(request):
    if request.method == 'POST':
        # Retrieve form data using `get` to avoid KeyError if field does not exist
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')
        profile_picture = request.FILES.get('profile_picture')

        # Validate that none of the fields are empty
        if not all([first_name, last_name, email, password, username]):
            messages.error(request, "All fields must be filled out.")
            return render(request, 'accounts/signup.html')

        # Email validation
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email address.")
            return render(request, 'accounts/signup.html')

        # Check for unique username and email
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return render(request, 'accounts/signup.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, 'accounts/signup.html')

        # Password validation
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return render(request, 'accounts/signup.html')

        # Create and save the new user
        try:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # If a profile picture was provided, attach it to the user
            if profile_picture:
                user.profile_picture = profile_picture
                user.save()  # Save the user to update with profile picture

            # Login the user
            login(request, user)

            # Redirect to profile page or another success page
            return redirect('profile')

        except Exception as e:
            # In production, log the error
            messages.error(request, f"Unable to create account. {e}")

    # Display the empty form for GET request
    return render(request, 'accounts/signup.html')




def logout_view(request):
    
    logout(request)
    
    
    return redirect('login')  


# views.py
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .forms import CustomPasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required



# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Note
from .forms import NoteForm

@login_required
def notes(request):
    user = request.user
    notes = Note.objects.filter(user=user)

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = user
            note.save()
            return redirect('notes')
    else:
        form = NoteForm()

    return render(request, 'accounts/notes.html', {'form': form, 'notes': notes})


# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def user_info(request):
    user = request.user
    return render(request, 'accounts/user_info.html', {'user': user})
