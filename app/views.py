import random
import string
from datetime import datetime, date, timedelta

import pandas as pd

from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum, Max
from django.db.models.functions import TruncMonth
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from app.models import Profile, Main_page, Summary, Full_report, Payment_history, Id, Commission_structure, Website, \
    Player_report, Payment_history2, Promo_code
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
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')
        phone = request.POST.get('phone')
        messenger = request.POST.get('messenger')
        messengerusername = request.POST.get('messengerusername')
        country = request.POST.get('country')
        preferred_payment_method = request.POST.get('player')
        user_account = request.POST.get('user')
        website = request.POST.get('website')
        site_category = request.POST.get('site')

        # Check if passwords and emails match
        if password == confirm_password:
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
                    phone=phone,
                    messenger=messenger,
                    country=country,
                    preferred_payment_method=preferred_payment_method,
                    user_account=user_account,
                    website=website,
                    password=password,
                    confirm_password=confirm_password,
                    messengerusername=messengerusername,
                    site_category=site_category
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
                        'messenger': request.POST['messenger'],
                        'messengerusername': request.POST['messengerusername'],
                        'country': request.POST['country'],
                        'preferred_payment_method': request.POST['player'],
                        'user_account': request.POST['user'],
                        'website': request.POST['website'],
                        'site_category': request.POST['site'],
                        'approval_link': approval_link,
                    })
                )
                send_mail(
                    subject='Welcome to 20Bet Partners!',
                    message='Thank you for registering with us. Please wait for the admin to approve your registration.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email]
                )
                messages.success(
                    request,
                    "Thanks for registering!\n"
                    "Your request has been received and is being reviewed.\n"
                    "You will receive an email about the status of your request within 48 hours."
                )
                try:
                    df = pd.read_excel('user_data.xlsx')
                except FileNotFoundError:
                    df = pd.DataFrame(columns=['Username', 'Firstname', 'Lastname', 'Email',
                                               'Phone', 'Messenger', 'Messenger Username' 'Country',
                                               'Preferred Payment Method',
                                               'User Account', 'Website', 'Site Category'
                                               ])

                new_data = pd.DataFrame({
                    'Username': [username],
                    'Firstname': [first_name],
                    'Lastname': [last_name],
                    'Email': [email],
                    'Phone': [phone],
                    'Messenger': [messenger],
                    'Messenger Username': [messengerusername],
                    'Country': 'India',
                    'Site Category': [site_category],
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

        return HttpResponse("User approved successfully!")
    except Profile.DoesNotExist:
        return HttpResponse("User not found.")
    except Exception as e:
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
                request.session['username'] = username
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


# def login1(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         # Check if the user exists in the database
#         if Profile.objects.filter(username=username).exists():
#             user = Profile.objects.get(username=username)
#
#             # Compare plain-text password
#             if user.password == password:
#                 # Store username in session to track logged-in user
#                 request.session['username'] = username
#                 messages.success(request, "Login successful.")
#                 # Redirect to the statistics page for this user
#                 return redirect('statistics')
#             else:
#                 messages.error(request, "Invalid password.")
#                 return render(request, 'login1.html')
#         else:
#             messages.error(request, "Invalid username.")
#             return render(request, 'login1.html')
#
#     return render(request, 'login1.html')


def account(request):
    # Check if the user is logged in
    if 'username' not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect('login1')

    username = request.session['username']
    try:
        # Get the profile of the logged-in user
        profile = Profile.objects.get(username=username)
    except Profile.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect('login1')

    # Filter x and y variables by the logged-in user
    x = Profile.objects.filter(username=username)
    y = Id.objects.filter(user=profile)

    if request.method == 'POST' and 'change_password' in request.POST:
        old_password = request.POST.get('Old_pass').strip()
        new_password = request.POST.get('New_pass').strip()
        repeat_password = request.POST.get('repeat').strip()

        # Debugging the incoming data
        print("Old Password:", old_password)  # Print the old password for debugging
        print("New Password:", new_password)  # Print the new password
        print("Repeat Password:", repeat_password)  # Print repeat password

        # Validation checks
        if not old_password or not new_password or not repeat_password:
            messages.error(request, "All fields are required.")
        else:
            if profile.password != old_password:
                messages.error(request, "Old password is incorrect.")
            elif new_password != repeat_password:
                messages.error(request, "New passwords do not match.")
            elif len(new_password) < 8:
                messages.error(request, "New password must be at least 8 characters long.")
            else:
                # Update the password
                profile.password = new_password
                profile.save()
                messages.success(request, "Password changed successfully.")
                return redirect('account')

    return render(request, 'account.html', {
        'x': x,
        'y': y,
        'profile': profile,
    })


def aff_links(request):
    if 'username' not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect('login1')

    username = request.session['username']
    try:
        # Get the profile of the logged-in user
        profile = Profile.objects.get(username=username)
    except Profile.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect('login1')

    # Filter x, y, and z variables based on the logged-in user
    x = Profile.objects.filter(username=username)
    y = Id.objects.filter(user=profile)
    z = Website.objects.filter(user=profile)  # Assuming the Website model has a relation with the user
    profiles = Profile.objects.filter(username=username).values('website').distinct()

    return render(request, 'aff_links.html', {
        'x': x,
        'y': y,
        'profiles': profiles,
        'z': z,
    })


def commission_structure(request):
    # Fetch the user associated with the session
    username = request.session.get('username')

    try:
        user = Profile.objects.get(username=username)
    except Profile.DoesNotExist:
        messages.error(request, "Invalid session data.")
        return render(request, 'commission_structure.html', {
            'message': "Invalid session data.",
        })

    # Fetch all IDs for the user
    y = Id.objects.filter(user=user)

    # Fetch today's data for Commission_structure
    today = date.today()
    x = Commission_structure.objects.filter(user=user, date=today)

    if not x.exists():
        # If no data exists for today, find the most recent date with data
        most_recent_date = Commission_structure.objects.filter(user=user, date__lte=today).aggregate(Max('date'))[
            'date__max']
        if most_recent_date:
            x = Commission_structure.objects.filter(user=user, date=most_recent_date)

    return render(request, 'commission_structure.html', {
        'y': y,
        'x': x,
        'message': "No data available for today. Showing the most recent data." if not x.exists() else ""
    })


def contacts(request):
    y = Id.objects.all()
    return render(request, 'contacts.html', {'y': y})


def media(request):
    return render(request, 'media.html')


def payment_history(request):
    # Fetch the user associated with the session
    username = request.session.get('username')

    try:
        user = Profile.objects.get(username=username)
    except Profile.DoesNotExist:
        messages.error(request, "Invalid session data.")
        return render(request, 'payment_history.html', {
            'message': "Invalid session data.",
        })

    # Initialize variables
    payments = Payment_history.objects.none()
    payments2 = Payment_history2.objects.filter(user=user)
    x = Payment_history.objects.filter(user=user, date=date.today())
    z = Payment_history2.objects.filter(user=user, time_interval=date.today())
    y = Id.objects.filter(user=user)  # Filter IDs associated with the user
    start_date = None
    end_date = None
    time_interval = request.GET.get('time_interval', 'exact')

    today = date.today()  # No need to call .date()

    # Check if "Generate" button was clicked
    if 'generate' in request.GET:
        if time_interval == 'today':
            start_date = end_date = today
        elif time_interval == 'yesterday':
            start_date = end_date = today - timedelta(days=1)
        elif time_interval == 'currentmonth':
            start_date = today.replace(day=1)
            next_month = today.replace(day=28) + timedelta(days=4)
            end_date = next_month - timedelta(days=next_month.day)
        elif time_interval == 'lastmonth':
            first_of_this_month = today.replace(day=1)
            end_date = first_of_this_month - timedelta(days=1)
            start_date = end_date.replace(day=1)
        elif time_interval == 'currentyear':
            start_date = today.replace(month=1, day=1)
            end_date = today.replace(month=12, day=31)
        elif time_interval == 'lastyear':
            start_date = today.replace(year=today.year - 1, month=1, day=1)
            end_date = today.replace(year=today.year - 1, month=12, day=31)
        elif time_interval == 'exact':
            try:
                start_date = datetime.strptime(request.GET.get('start_date', ''), '%Y-%m-%d').date()
                end_date = datetime.strptime(request.GET.get('end_date', ''), '%Y-%m-%d').date()
            except (ValueError, TypeError):
                start_date = end_date = None
        else:
            try:
                if request.GET.get('start_date'):
                    start_date = datetime.strptime(request.GET.get('start_date'), '%Y-%m-%d').date()
                if request.GET.get('end_date'):
                    end_date = datetime.strptime(request.GET.get('end_date'), '%Y-%m-%d').date()
            except ValueError:
                start_date = end_date = None

        # Apply filters to payments if dates are valid
        if start_date and end_date:
            payments = Payment_history.objects.filter(user=user, date__range=[start_date, end_date])

    # Safely convert dates for context
    start_date_str = start_date.strftime('%Y-%m-%d') if isinstance(start_date, date) else ''
    end_date_str = end_date.strftime('%Y-%m-%d') if isinstance(end_date, date) else ''

    # Prepare record_text safely
    total_records = payments.count()
    start_record = payments.first().id if total_records > 0 else 0
    end_record = payments.last().id if total_records > 0 else 0
    record_text = (
        f"Records from {start_record} to {end_record} ({total_records} record{'s' if total_records != 1 else ''})"
        if total_records > 0
        else "No records found"
    )

    return render(request, 'payment_history.html', {
        'payments': payments,
        'payments2': payments2,
        'start_date': start_date_str,
        'end_date': end_date_str,
        'time_interval': time_interval,
        'x': x,
        'y': y,
        'z': z,
        'record_text': record_text,
    })


# def playerreport(request):
#     profiles = Profile.objects.values('website').distinct()
#     y = Id.objects.all()
#     x = Commission_structure.objects.filter(date=date.today())
#     return render(request, 'playerreport.html', {'y': y, 'profiles': profiles, 'x': x})


def playerreport(request):
    # Check if the user is logged in
    if 'username' not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect('login1')

    username = request.session['username']
    try:
        # Fetch the logged-in user's profile
        profile = Profile.objects.get(username=username)
    except Profile.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect('login1')

    # Fetch data filtered by the logged-in user
    profiles = Profile.objects.filter(username=username).values('website').distinct()
    y = Id.objects.filter(user=profile)
    x = Commission_structure.objects.filter(user=profile, date=datetime.today().date())
    z = Website.objects.select_related('user').filter(user=profile)
    a = Player_report.objects.select_related('user').filter(user=profile)

    # Initialize variables
    payments = Summary.objects.none()  # Default to no results
    start_date = None
    end_date = None
    time_interval = request.GET.get('time_interval', '')

    # Check if "Generate" button was clicked
    if 'generate' in request.GET or time_interval:
        # Get input dates from the form
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        today = datetime.today()

        # Handle time_interval values
        if time_interval == 'exact':
            # Use user-provided dates
            try:
                if start_date:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                if end_date:
                    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                # Handle invalid date input
                start_date = end_date = None
        elif time_interval == 'today':
            start_date = end_date = today.date()
        elif time_interval == 'yesterday':
            start_date = end_date = today.date() - timedelta(days=1)
        elif time_interval == 'currentmonth':
            start_date = today.replace(day=1).date()
            end_date = (today.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
        elif time_interval == 'lastmonth':
            first_of_this_month = today.replace(day=1)
            end_date = (first_of_this_month - timedelta(days=1)).date()
            start_date = end_date.replace(day=1)
        elif time_interval == 'currentyear':
            start_date = today.replace(month=1, day=1).date()
            end_date = today.replace(month=12, day=31).date()
        elif time_interval == 'lastyear':
            start_date = today.replace(year=today.year - 1, month=1, day=1).date()
            end_date = today.replace(year=today.year - 1, month=12, day=31).date()

        # Apply filters if valid dates are provided
        if start_date and end_date:
            payments = Summary.objects.filter(user=profile, date__range=[start_date, end_date])

    # Aggregate data for current and total summaries
    current_summary = payments.aggregate(
        sum_of_all_deposits=Sum('sum_of_all_deposits'),
        revenue=Sum('revenue')
    )

    total_summary = Summary.objects.filter(user=profile).aggregate(
        sum_of_all_deposits=Sum('sum_of_all_deposits'),
        revenue=Sum('revenue')
    )

    # Group payments by date
    grouped_payments = {}
    for payment in payments:
        grouped_payments.setdefault(payment.date, []).append(payment)

    # Format dates for template rendering
    start_date_str = start_date.strftime('%Y-%m-%d') if isinstance(start_date, (datetime, date)) else ''
    end_date_str = end_date.strftime('%Y-%m-%d') if isinstance(end_date, (datetime, date)) else ''

    return render(request, 'playerreport.html', {
        'y': y,
        'profiles': profiles,
        'x': x,
        'grouped_payments': grouped_payments,
        'start_date': start_date_str,
        'end_date': end_date_str,
        'time_interval': time_interval,
        'z': z,
        'a': a,
        'current_summary': current_summary,
        'total_summary': total_summary
    })


def promocode(request):
    if 'username' not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect('login1')

    username = request.session['username']
    try:
        # Get the profile of the logged-in user
        profile = Profile.objects.get(username=username)
    except Profile.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect('login1')

    # Filter data based on the logged-in user
    profiles = Profile.objects.filter(username=username).values('website').distinct()
    x = Promo_code.objects.filter(user=profile)  # Assuming Promo_code has a relation with the user
    y = Id.objects.filter(user=profile)

    return render(request, 'promocode.html', {
        'y': y,
        'profiles': profiles,
        'x': x,
    })


def statistics(request):
    time_interval = request.GET.get('time_interval', '7 days')  # Default to '7 days'

    today = date.today()
    start_date = None

    # Calculate the start date based on the selected time interval
    if time_interval == '7 days':
        start_date = today - timedelta(days=7)
    elif time_interval == '1 month':
        start_date = today.replace(day=1)  # First day of the current month
    elif time_interval == '6 months':
        start_date = (today.replace(day=1) - timedelta(days=180)).replace(day=1)
    elif time_interval == '1 year':
        start_date = today.replace(year=today.year - 1, month=1, day=1)

    # Get the username from the session
    username = request.session.get('username')

    # Fetch the user associated with the session
    try:
        user = Profile.objects.get(username=username)
    except Profile.DoesNotExist:
        messages.error(request, "Invalid session data.")
        return render(request, 'statistics.html', {
            'time_interval': time_interval,
            'message': "No data available for today. Showing most recent data."
        })

    # Fetch data for Main_page filtered by user and date
    main_page_data = Main_page.objects.filter(user=user, date=today)

    if not main_page_data.exists():
        # If no data exists for today, find the most recent date with data for this user
        most_recent_date = Main_page.objects.filter(user=user, date__lte=today).aggregate(Max('date'))['date__max']
        if most_recent_date:
            main_page_data = Main_page.objects.filter(user=user, date=most_recent_date)

    # Fetch data for Summary filtered by user and date
    z = Summary.objects.filter(user=user, date=today)

    if not z.exists():
        # If no data exists for today, find the most recent date with data for this user
        most_recent_summary_date = Summary.objects.filter(user=user, date__lte=today).aggregate(Max('date'))[
            'date__max']
        if most_recent_summary_date:
            z = Summary.objects.filter(user=user, date=most_recent_summary_date)

    # Debugging logs for date ranges and data
    print(f"Start Date: {start_date}, Today: {today}")
    print(f"Main Page Query: {main_page_data.query}")
    print(f"Main Page Data: {list(main_page_data)}")
    print(f"Summary Data: {list(z)}")

    if main_page_data.exists():
        # Fetch only the Ids associated with this user
        y = Id.objects.filter(user=user)

        # Fetch summary data for the user from the start date onwards
        a = Summary.objects.filter(date__gte=start_date, user=user)

        # Prepare data for the bar chart
        conversion_data = {
            "views": a.aggregate(Sum('views'))['views__sum'] or 0,
            "clicks": a.aggregate(Sum('clicks'))['clicks__sum'] or 0,
            "direct_links": a.aggregate(Sum('direct_links'))['direct_links__sum'] or 0,
            "active_players": a.aggregate(Sum('active_players'))['active_players__sum'] or 0,
            "new_depositors": a.aggregate(Sum('new_depositors'))['new_depositors__sum'] or 0,
        }

        # Group by month for annotations in the area chart
        a = a.annotate(month=TruncMonth('date')).values('month').annotate(
            registrations_sum=Sum('registrations'),
            commission_sum=Sum('overall_commission')
        ).order_by('month')

        # Convert data to a suitable format for JavaScript
        bar_chart_data = [
            conversion_data["views"],
            conversion_data["clicks"],
            conversion_data["direct_links"],
            conversion_data["active_players"],
            conversion_data["new_depositors"],
        ]

        bar_chart_categories = ['Views', 'Clicks', 'Direct Links', 'Active Players', 'New Depositors']

        area_chart_months = [entry['month'].strftime("%b") for entry in a]  # Extract month as 'Jan', 'Feb', etc.
        area_chart_registrations = [entry['registrations_sum'] for entry in a]  # Sum of registrations
        area_chart_commissions = [entry['commission_sum'] for entry in a]

        # Render the data to the template
        return render(request, 'statistics.html', {
            'x': main_page_data,  # Updated to show filtered data
            'y': y,
            'z': z,
            'bar_chart_data': bar_chart_data,
            'bar_chart_categories': bar_chart_categories,
            'area_chart_months': area_chart_months,
            'area_chart_registrations': area_chart_registrations,
            'area_chart_commissions': area_chart_commissions,
            'a': a,
            'time_interval': time_interval
        })
    else:
        # No data available for today, show message
        return render(request, 'statistics.html', {
            'x': main_page_data,
            'y': Id.objects.all(),
            'z': Summary.objects.filter(date__gte=start_date),
            'time_interval': time_interval,
            'message': "No data available for today. Showing most recent data."
        })


def summary(request):
    # Check if the user is logged in
    if 'username' not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect('login1')

    username = request.session['username']
    try:
        # Fetch the logged-in user's profile
        profile = Profile.objects.get(username=username)
    except Profile.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect('login1')

    # Fetch initial data for the context
    x = Summary.objects.filter(user=profile)  # Filter Summary by the logged-in user
    y = Id.objects.filter(user=profile)  # Filter Id by the logged-in user
    z = Profile.objects.filter(username=username)  # Get the profile for the logged-in user
    dates = x.values_list('date', flat=True).distinct()

    # Initialize variables
    payments = Summary.objects.none()  # Start with no results
    start_date = None
    end_date = None
    time_interval = request.GET.get('time_interval', '')

    # Check if "Generate" button was clicked
    if 'generate' in request.GET:
        # Get input dates from the form
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        today = datetime.today()

        # Handle time_interval values and set start_date and end_date
        if time_interval == 'exact':
            try:
                if start_date:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                if end_date:
                    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                start_date = end_date = None
        elif time_interval == 'today':
            start_date = end_date = today.date()
        elif time_interval == 'yesterday':
            start_date = end_date = today.date() - timedelta(days=1)
        elif time_interval == 'currentmonth':
            start_date = today.replace(day=1)
            next_month = today.replace(day=28) + timedelta(days=4)
            end_date = next_month - timedelta(days=next_month.day)
        elif time_interval == 'lastmonth':
            first_of_this_month = today.replace(day=1)
            end_date = first_of_this_month - timedelta(days=1)
            start_date = end_date.replace(day=1)
        elif time_interval == 'currentyear':
            start_date = today.replace(month=1, day=1)
            end_date = today.replace(month=12, day=31)
        elif time_interval == 'lastyear':
            start_date = today.replace(year=today.year - 1, month=1, day=1)
            end_date = today.replace(year=today.year - 1, month=12, day=31)
        else:
            try:
                if start_date:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                if end_date:
                    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                start_date = end_date = None

        # Apply filters if valid dates are provided
        if start_date and end_date:
            payments = Summary.objects.filter(user=profile, date__range=[start_date, end_date])

    # Aggregate data for the filtered payments (sum of fields)
    total_summary = payments.aggregate(
        views=Sum('views'),
        clicks=Sum('clicks'),
        direct_links=Sum('direct_links'),
        clicks_views=Sum('clicks_views'),
        registrations=Sum('registrations'),
        registration_with_deposits_registration_ratio=Sum('registration_with_deposits_registration_ratio'),
        total_new_deposit_amount=Sum('total_new_deposit_amount'),
        new_depositors=Sum('new_depositors'),
        accounts_with_deposits=Sum('accounts_with_deposits'),
        sum_of_all_deposits=Sum('sum_of_all_deposits'),
        revenue=Sum('revenue'),
        number_of_deposits=Sum('number_of_deposits'),
        active_players=Sum('active_players'),
        average_profit_per_player=Sum('average_profit_per_player'),
        bonus_amount=Sum('bonus_amount'),
        total_rs_commission=Sum('total_rs_commission'),
        cpa=Sum('cpa'),
        referral_commission=Sum('referral_commission'),
        overall_commission=Sum('overall_commission')
    )

    # Group payments by date for display
    grouped_payments = {}
    for payment in payments:
        grouped_payments.setdefault(payment.date, []).append(payment)

    # Format dates for template rendering
    start_date_str = start_date.strftime('%Y-%m-%d') if start_date else ''
    end_date_str = end_date.strftime('%Y-%m-%d') if end_date else ''

    # Render the template with context data
    return render(request, 'summary.html', {
        'x': x,
        'y': y,
        'z': z,
        'grouped_payments': grouped_payments,
        'total_summary': total_summary,
        'start_date': start_date_str,
        'end_date': end_date_str,
        'time_interval': time_interval,
        'dates': dates,
    })


def test(request):
    return render(request, 'test.html')


def webpages(request):
    # Fetch all profiles and related objects for the logged-in user
    username = request.session.get('username')

    # Fetch the user associated with the session
    try:
        user = Profile.objects.get(username=username)
    except Profile.DoesNotExist:
        messages.error(request, "Invalid session data.")
        return render(request, 'webpages.html', {
            'message': "No profiles available for the logged-in user.",
        })

    # Fetch profiles filtered by the user's website
    profiles = Profile.objects.values('website').distinct()  # Get unique websites only
    y = Id.objects.filter(user=user)  # Filter related IDs based on the user
    z = Website.objects.filter(user=user)  # Fetch all websites as before

    # Get the total number of records (unique websites)
    total_records = profiles.count()

    # Determine records per page
    records_per_page = request.GET.get('records_per_page', total_records)  # Default to total records if not specified
    try:
        records_per_page = int(records_per_page)
    except ValueError:
        records_per_page = total_records  # Default to total records on invalid input

    # Pagination logic
    page_number = request.GET.get('page', 1)
    paginator = Paginator(profiles, records_per_page)
    try:
        current_page = paginator.get_page(page_number)
    except PageNotAnInteger:
        current_page = paginator.get_page(1)
    except EmptyPage:
        current_page = paginator.get_page(1 if int(page_number) < 1 else paginator.num_pages)

    # Calculate record range
    start_record = (current_page.number - 1) * paginator.per_page + 1
    end_record = min(start_record + current_page.object_list.count() - 1, total_records)

    return render(request, 'webpages.html', {
        'x': user,  # Include the logged-in user's profile
        'profiles': current_page,
        'y': y,
        'z': z,
        'records_per_page': records_per_page,
        'total_records': total_records,
        'start_record': start_record,
        'end_record': end_record,
    })


def full_report(request):
    # Check if the user is logged in via session
    if 'username' not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect('login1')

    username = request.session['username']
    try:
        # Fetch the logged-in user's profile
        profile = Profile.objects.get(username=username)
    except Profile.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect('login1')

    # Fetch data based on the logged-in user
    x = Summary.objects.filter(user=profile)  # Filter Summary by the logged-in user
    y = Id.objects.filter(user=profile)  # Filter Id by the logged-in user
    z = Profile.objects.filter(username=username)  # Get the profile for the logged-in user
    dates = x.values_list('date', flat=True).distinct()

    # Initialize variables
    payments = Summary.objects.none()  # Start with no results
    start_date = None
    end_date = None
    time_interval = request.GET.get('time_interval', '')

    # Handle time interval and date range for "Generate" functionality
    if 'generate' in request.GET:
        # Get input dates from the form
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        today = datetime.today()

        # Determine start_date and end_date based on time_interval
        if time_interval == 'exact':
            try:
                if start_date:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                if end_date:
                    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                start_date = end_date = None
        elif time_interval == 'today':
            start_date = end_date = today.date()
        elif time_interval == 'yesterday':
            start_date = end_date = today.date() - timedelta(days=1)
        elif time_interval == 'currentmonth':
            start_date = today.replace(day=1)
            next_month = today.replace(day=28) + timedelta(days=4)
            end_date = next_month - timedelta(days=next_month.day)
        elif time_interval == 'lastmonth':
            first_of_this_month = today.replace(day=1)
            end_date = first_of_this_month - timedelta(days=1)
            start_date = end_date.replace(day=1)
        elif time_interval == 'currentyear':
            start_date = today.replace(month=1, day=1)
            end_date = today.replace(month=12, day=31)
        elif time_interval == 'lastyear':
            start_date = today.replace(year=today.year - 1, month=1, day=1)
            end_date = today.replace(year=today.year - 1, month=12, day=31)
        else:
            try:
                if start_date:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                if end_date:
                    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                start_date = end_date = None

        # Apply filters if valid dates are provided
        if start_date and end_date:
            payments = Summary.objects.filter(user=profile, date__range=[start_date, end_date])

    # Aggregate data for the filtered payments
    total_summary = payments.aggregate(
        views=Sum('views'),
        clicks=Sum('clicks'),
        direct_links=Sum('direct_links'),
        clicks_views=Sum('clicks_views'),
        registrations=Sum('registrations'),
        registration_with_deposits_registration_ratio=Sum('registration_with_deposits_registration_ratio'),
        total_new_deposit_amount=Sum('total_new_deposit_amount'),
        new_depositors=Sum('new_depositors'),
        accounts_with_deposits=Sum('accounts_with_deposits'),
        sum_of_all_deposits=Sum('sum_of_all_deposits'),
        revenue=Sum('revenue'),
        number_of_deposits=Sum('number_of_deposits'),
        active_players=Sum('active_players'),
        average_profit_per_player=Sum('average_profit_per_player'),
        bonus_amount=Sum('bonus_amount'),
        total_rs_commission=Sum('total_rs_commission'),
        cpa=Sum('cpa'),
        referral_commission=Sum('referral_commission'),
        overall_commission=Sum('overall_commission')
    )

    # Group payments by date for display
    grouped_payments = {}
    for payment in payments:
        grouped_payments.setdefault(payment.date, []).append(payment)

    # Format dates for template rendering
    start_date_str = start_date.strftime('%Y-%m-%d') if start_date else ''
    end_date_str = end_date.strftime('%Y-%m-%d') if end_date else ''

    # Render the template with combined data
    return render(request, 'full_report.html', {
        'x': x,
        'y': y,
        'z': z,
        'grouped_payments': grouped_payments,
        'total_summary': total_summary,
        'start_date': start_date_str,
        'end_date': end_date_str,
        'time_interval': time_interval,
        'dates': dates,
    })


def cookies(request):
    return render(request, 'cookies.html')


def news(request):
    return render(request, 'news.html')


def privacy_policy(request):
    return render(request, 'privacy_policy.html')


# def reset(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#
#         try:
#             profile = Profile.objects.get(username=username, email=email)
#             token = get_random_string(20)
#             uid = urlsafe_base64_encode(force_bytes(profile.pk))
#             reset_link = request.build_absolute_uri(reverse('reset_password', args=[uid, token]))
#
#             send_mail(
#                 'Password Reset Request',
#                 f'Click the link to reset your password: {reset_link}',
#                 'admin@example.com',
#                 [email],
#                 fail_silently=False,
#             )
#             messages.success(request, "Password reset link has been sent to your email.")
#         except Profile.DoesNotExist:
#             messages.error(request, "Invalid username or email.")
#
#     return render(request, 'reset.html')


# def reset_password(request, uid, token):
#     if request.method == 'POST':
#             try:
#                 # Decode the UID to get the profile ID
#                 profile_id = urlsafe_base64_decode(uid).decode()
#                 profile = Profile.objects.get(pk=profile_id)
#
#                 # Get new passwords from the form
#                 new_password = request.POST.get('newpassword')
#                 re_enter_new_password = request.POST.get('renewpassword')
#
#                 if new_password == re_enter_new_password:
#                     # Save the plain text password
#                     profile.password = new_password
#                     profile.save()
#
#                     messages.success(request, "Password has been reset successfully.")
#                     return redirect(reverse('login1'))  # Redirect to the login page
#                 else:
#                     messages.error(request, "Passwords do not match.")
#             except (Profile.DoesNotExist, ValidationError):
#                 messages.error(request, "Invalid reset link.")
#     return render(request, 'reset_password.html')

def reset(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        try:
            profile = Profile.objects.get(username=username,
                                          email=email)  # Adjust this to match your Profile model fields
            token = get_random_string(20)  # Using random token since passwords are not hashed
            uid = urlsafe_base64_encode(force_bytes(profile.pk))
            reset_link = request.build_absolute_uri(reverse('reset_password', args=[uid, token]))

            # Store the token temporarily in the profile or use another mechanism
            profile.reset_token = token
            profile.save()

            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                'admin@example.com',
                [email],
                fail_silently=False,
            )
            messages.success(request, "Password reset link has been sent to your email.")
        except Profile.DoesNotExist:
            messages.error(request, "Invalid username or email.")

    return render(request, 'reset.html')


def reset_password(request, uidb64, token):
    try:
        # Decode the user ID and fetch the profile
        uid = urlsafe_base64_decode(uidb64).decode()
        profile = Profile.objects.get(pk=uid)

        # Validate the reset token
        if profile.reset_token != token:
            messages.error(request, "Invalid or expired token.")
            return render(request, 'reset_password.html')

        if request.method == "POST":
            # Get passwords from the form
            password1 = request.POST.get('newpassword')
            password2 = request.POST.get('renewpassword')

            # Check if both passwords are provided
            if not password1 or not password2:
                return render(request, 'reset_password.html', {'error_message': "Please provide both passwords."})

            # Check if passwords match
            if password1 != password2:
                return render(request, 'reset_password.html', {'error_message': "Passwords do not match."})

            # Store the password as plain text (not recommended in production)
            profile.password = password1  # Note: This is insecure; use hashed passwords in production.
            profile.reset_token = None  # Clear the reset token after use
            profile.save()

            messages.success(request, "Password updated successfully.")
            return redirect('login1')

    except (Profile.DoesNotExist, ValueError, TypeError):
        messages.error(request, "Invalid user.")
        return render(request, 'reset_password.html', {'error_message': "Invalid user."})

    # Render the reset password form
    return render(request, 'reset_password.html', {'uidb64': uidb64, 'token': token})


def logout_view(request):
    logout(request)
    return redirect('login1')
