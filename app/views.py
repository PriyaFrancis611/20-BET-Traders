import random
from datetime import datetime

import pandas as pd

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from app.models import Profile, Main_page, Summary, Full_report, Payment_history
from project import settings


# Create your views here.

def index(request):
    return render(request, 'index.html')


def f404(request):
    return render(request, 'f404.html')


def faq(request):
    return render(request, 'faq.html')


# def register1(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         first_name = request.POST['firstname']
#         last_name = request.POST['lastname']
#         email = request.POST['email']
#         confirm_email = request.POST['confirmemail']
#         password = request.POST['password']
#         confirm_password = request.POST['confirmpassword']
#         if password == confirm_password and email == confirm_email:
#             if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
#                 return redirect('register1')
#             else:
#                 user = User.objects.create_user(
#                     username=username, first_name=first_name, last_name=last_name, email=email, password=password
#                 )
#                 x = Profile()
#                 x.user = user
#                 x.phone = request.POST['phone']
#                 x.skype = request.POST['skype']
#                 x.country = request.POST['country']
#                 x.preferred_payment_method = request.POST['player']
#                 x.user_account = request.POST['user']
#                 x.website = request.POST['website']
#                 x.additional_info = request.POST['info']
#                 x.save()
#
#                 uid = urlsafe_base64_encode(force_bytes(user.pk))
#                 approval_link = request.build_absolute_uri(reverse('approve_user', args=[uid]))
#
#                 # Send email to admin with user details and approval link
#                 send_mail(
#                     subject='New User Registration Approval Needed',
#                     message=f"A new user, {username}, has registered. Please approve their account.",
#                     from_email=settings.DEFAULT_FROM_EMAIL,
#                     recipient_list=[settings.ADMIN_EMAIL],
#                     html_message=render_to_string('admin.html', {
#                         'username': username,
#                         'first_name': first_name,
#                         'last_name': last_name,
#                         'email': email,
#                         'phone': request.POST['phone'],
#                         'skype': request.POST['skype'],
#                         'country': request.POST['country'],
#                         'preferred_payment_method': request.POST['player'],
#                         'user_account': request.POST['user'],
#                         'website': request.POST['website'],
#                         'additional_info': request.POST['info'],
#                         'approval_link': approval_link,
#                     })
#                 )
#                 messages.success(
#                     request,
#                     "An email has been sent to the admin for approval. After approval, you will receive a "
#                     "confirmation email and will be able to log in."
#                 )
#
#                 return redirect("register1")
#         else:
#             return render(request, 'register1.html')
#     else:
#         return render(request, 'register1.html')

def register1(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        confirm_email = request.POST.get('confirmemail')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')
        phone = request.POST.get('phone')
        telegram = request.POST.get('telegram')
        country = request.POST.get('country')
        preferred_payment_method = request.POST.get('player')
        user_account = request.POST.get('user')
        website = request.POST.get('website')
        additional_info = request.POST.get('info')

        # Check if passwords and emails match
        if password == confirm_password and email == confirm_email:
            # Check if username or email already exists
            if Profile.objects.filter(username=username).exists() or Profile.objects.filter(email=email).exists():
                messages.error(request, "Username or email already exists.")
                return redirect('register1')
            else:
                # Create a new profile and store the password as plain text
                user = Profile(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    confirm_email=confirm_email,
                    phone=phone,
                    telegram=telegram,
                    country=country,
                    preferred_payment_method=preferred_payment_method,
                    user_account=user_account,
                    website=website,
                    additional_info=additional_info,
                    password=password,
                    confirm_password=confirm_password
                )
                user.save()
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                approval_link = request.build_absolute_uri(reverse('approve_user', args=[uid]))

                # Send email to admin with user details and approval link
                send_mail(
                    subject='New User Registration Approval Needed',
                    message=f"A new user, {username}, has registered. Please approve their account.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    html_message=render_to_string('admin.html', {
                        'username': username,
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                        'phone': request.POST['phone'],
                        'telegram': request.POST['telegram'],
                        'country': request.POST['country'],
                        'preferred_payment_method': request.POST['player'],
                        'user_account': request.POST['user'],
                        'website': request.POST['website'],
                        'additional_info': request.POST['info'],
                        'approval_link': approval_link,
                    })
                )
                messages.success(
                    request,
                    "An email has been sent to the admin for approval. After approval, you will receive a "
                    "confirmation email and will be able to log in."
                )
                try:
                    df = pd.read_excel('user_data.xlsx')
                except FileNotFoundError:
                    df = pd.DataFrame(columns=['Username', 'Firstname', 'Lastname', 'Email',
                                               'Phone', 'Telegram', 'Country', 'Preferred Payment Method',
                                               'User Account', 'Website'
                                               ])

                new_data = pd.DataFrame({
                    'Username': [username],
                    'Firstname': [first_name],
                    'Lastname': [last_name],
                    'Email': [email],
                    'Phone': [phone],
                    'Telegram': [telegram],
                    'Country': [country],
                    'Preferred Payment Method': [preferred_payment_method],
                    'User Account': [user_account],
                    'Website': [website]

                })
                df = pd.concat([df, new_data], ignore_index=True)

                df.to_excel('user_data.xlsx', index=False)

                return redirect("register1")
        else:
            return render(request, 'register1.html')
    else:
        return render(request, 'register1.html')


def approve_user(request, uid):
    try:
        # Decode the user id
        user_id = urlsafe_base64_decode(uid).decode()
        user = get_object_or_404(Profile, pk=user_id)

        # Approve the user by setting is_approved to True
        user.is_approved = True
        user.save()

        # Send activation email to the user
        send_mail(
            subject="Your Account Has Been Activated",
            message="Congratulations! Your account has been approved and activated. You can now log in.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        # Display success message
        messages.success(request, "User approved successfully.")
        return HttpResponse("User approved successfully!")
    except Profile.DoesNotExist:
        messages.error(request, "User not found.")
        return HttpResponse("User not found.")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return HttpResponse("Error occurred.")


def terms(request):
    return render(request, 'terms.html')


def admin(request):
    return render(request, 'admin.html')


# def login1(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         if username and password:
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 profile = Profile.objects.get(user=user)
#                 if profile.is_approved:
#                     login(request, user)
#                     return redirect('index')  # Replace with your home page
#                 else:
#                     messages.error(request, "Your account is not approved yet. Please wait for admin approval.")
#                     return redirect('login1')
#             else:
#                 messages.error(request, "Invalid username or password.")
#                 return redirect('login1')
#         else:
#             messages.error(request, "Both username and password are required.")
#             return redirect('login1')
#     else:
#         return render(request, 'login1.html')


def login1(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Fetch the user by username
            user = Profile.objects.get(username=username)

            # Check if the user has been approved
            if not user.is_approved:
                messages.error(request, "Your account has not been approved by the admin. Please wait for approval.")
                return render(request, 'login1.html')

            # Check if the password matches the stored one
            if user.password == password:
                # User is authenticated, proceed with login
                messages.success(request, "Login successful.")
                return redirect('statistics')  # Redirect to home page or dashboard
            else:
                messages.error(request, "Invalid password.")
                return render(request, 'login1.html')

        except Profile.DoesNotExist:
            messages.error(request, "Invalid username.")
            return render(request, 'login1.html')

    return render(request, 'login1.html')


def account(request):
    x = Profile.objects.all()
    return render(request, 'account.html', {'x': x})


def aff_links(request):
    return render(request, 'aff_links.html')


def commission_structure(request):
    return render(request, 'commission_structure.html')


def contacts(request):
    return render(request, 'contacts.html')


def media(request):
    return render(request, 'media.html')


def payment_history(request):
    x = Payment_history.objects.all()
    return render(request, 'payment_history.html',{'x':x})


def playerreport(request):
    return render(request, 'playerreport.html')


def promocode(request):
    return render(request, 'promocode.html')


def statistics(request):
    x = Main_page.objects.all()
    return render(request, 'statistics.html', {'x': x})


def summary(request):
    x = Summary.objects.all()
    return render(request, 'summary.html', {'x': x})


def test(request):
    return render(request, 'test.html')


def webpages(request):
    x = Profile.objects.all()
    return render(request, 'webpages.html', {'x': x})


def full_report(request):
    # Initialize variables
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    transactions = Full_report.objects.all()  # Default to all transactions

    # Validate and filter by date range if both dates are provided
    if start_date and end_date:
        try:
            # Convert date strings to datetime.date objects
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            # Filter transactions by the date range
            transactions = Full_report.objects.filter(date__range=[start_date, end_date])
        except ValueError:
            # Optional: Handle invalid date formats
            error_message = "Invalid date format. Please use YYYY-MM-DD."
            return render(request, 'full_report.html', {
                'transactions': transactions,
                'error_message': error_message,
            })

    # Render the template with filtered transactions
    return render(request, 'full_report.html', {
        'transactions': transactions,
        'start_date': start_date,
        'end_date': end_date,
    })
