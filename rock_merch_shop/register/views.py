from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ContactForm


def register(request):
    """
    Handles user registration

    This view handles both GET and POST requests. For a GET request, it displays the registration form.
    For a POST request, it processes the form data, creating a new user if the form data is valid.
    Upon successful registration, the user is authenticated and redirected to the home page.

    :param request: The HttpRequest object used to generate this response
    :return:  A response object containing the rendered registration form template
              for GET requests or a redirect to the home page for successful POST requests.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user to the database
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # Authenticate the newly created user
            login(request, user)  # Log in the newly created user
            return redirect(reverse('home'))  # Redirect the user to the home page after successful registration
    else:
        form = UserCreationForm()  # Instantiate a new registration form for a GET request
    return render(request, "register/register.html", {"form": form})


@login_required
def profile(request):
    """
    Display and process the user profile and password change forms.

    This view function is accessible only to authenticated users due to the @login_required decorator.
    It handles both GET and POST requests. For a GET request, it displays forms for updating user information
    and changing the password. For a POST request, it processes the submitted forms. If the forms are valid,
    the user's information or password is updated, and a success message is displayed. The user is then
    redirected to the home page.

    :param request: The HttpRequest object used to generate this response
    :return: A response object containing the rendered profile template for GET requests,
             or a redirect to the home page for successful POST requests.
    """
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)
        if 'update_profile' in request.POST and user_form.is_valid():
            user_form.save() # Save the updated user information
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('home')  # Redirect the user to the home page after updating the profile
        elif 'change_password' in request.POST and password_form.is_valid():
            user = password_form.save() # Save the updated password
            update_session_auth_hash(request, user)  # Update session to prevent logout
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')  # Redirect the user to the home page after updating the password

        # Reload the forms for any other POST operations
        user_form = UserUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)
    else:
        # Load forms for GET request
        user_form = UserUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    context = {
        'user_form': user_form,
        'password_form': password_form,
    }
    return render(request, "register/profile.html", context)

def contact(request):
    """
    Handles the contact form submission.

    This view function supports both GET and POST methods. For a GET request, it displays an empty contact form.
    For a POST request, it processes the submitted contact form. If the form is valid, it displays a success message
    and redirects the user to the home page. This function uses Django's messaging framework to display a confirmation
    message to the user after submitting the form.

    :param request: # The HttpRequest object used to generate this response
    :return: A response object containing the rendered contact form template for GET requests,
             or a redirect to the home page for successful POST requests.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
            return redirect('home')  # Redirect the user to the home page after submitting the form
    else:
        form = ContactForm() # Load an empty form for a GET request

    return render(request, 'register/contact.html', {'form': form})