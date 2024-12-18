import random
import string
from datetime import datetime, date, timedelta

import pandas as pd

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum, Max
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
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
                send_mail(
                    subject='Welcome to 20Bet Partners!',
                    message='Thank you for registering with us. Please wait for the admin to approve your registration.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email]
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


def account(request):
    # Fetch the first profile (or remove this if not needed)
    x = Profile.objects.all()[:1]
    y = Id.objects.all()

    if 'username' not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect('login1')

    username = request.session['username']
    try:
        profile = Profile.objects.get(username=username)
    except Profile.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect('login1')

    if request.method == 'POST' and 'change_password' in request.POST:
        old_password = request.POST.get('Old_pass')
        new_password = request.POST.get('New_pass')
        repeat_password = request.POST.get('repeat')

        # Debugging the incoming data
        print("Old Password:", old_password)  # Print the old password for debugging
        print("New Password:", new_password)  # Print the new password
        print("Repeat Password:", repeat_password)  # Print repeat password

        if not old_password or not new_password or not repeat_password:
            messages.error(request, "All fields are required.")
        else:
            old_password = old_password.strip()
            new_password = new_password.strip()
            repeat_password = repeat_password.strip()

            if not old_password:  # Check if it is empty even after strip()
                messages.error(request, "Old password is required.")
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

    return render(request, 'account.html', {'x': x, 'y': y, 'profile': profile})


def aff_links(request):
    x = Profile.objects.all()
    y = Id.objects.all()
    z = Website.objects.all()
    profiles = Profile.objects.values('website').distinct()
    return render(request, 'aff_links.html', {'x': x, 'y': y, 'profiles': profiles, 'z': z})


def commission_structure(request):
    y = Id.objects.all()

    # Fetch today's data for Commission_structure
    today = date.today()
    x = Commission_structure.objects.filter(date=today)

    if not x.exists():
        # If no data exists for today, find the most recent date with data
        most_recent_date = Commission_structure.objects.filter(date__lte=today).aggregate(Max('date'))['date__max']
        if most_recent_date:
            x = Commission_structure.objects.filter(date=most_recent_date)

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
    # Initialize variables
    payments = Payment_history.objects.none()
    payments2 = Payment_history2.objects.all()
    x = Payment_history.objects.filter(date=date.today())
    z = Payment_history2.objects.filter(time_interval=date.today())
    y = Id.objects.all()
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
            payments = Payment_history.objects.filter(date__range=[start_date, end_date])


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
    profiles = Profile.objects.values('website').distinct()
    y = Id.objects.all()
    x = Commission_structure.objects.filter(date=datetime.today().date())
    z = Website.objects.select_related('user').all()
    a = Player_report.objects.select_related('user').all()
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
            payments = Summary.objects.filter(date__range=[start_date, end_date])

        # Aggregate data for current and total summaries
    current_summary = payments.aggregate(
        sum_of_all_deposits=Sum('sum_of_all_deposits'),
        revenue=Sum('revenue')
    )

    total_summary = Summary.objects.aggregate(
        sum_of_all_deposits=Sum('sum_of_all_deposits'),
        revenue=Sum('revenue')
    )

    # Group payments by date
    grouped_payments = {}
    for payment in payments:
        grouped_payments.setdefault(payment.date, []).append(payment)

    # Format dates for template rendering
    start_date_str = start_date.strftime('%Y-%m-%d') if isinstance(start_date, datetime) or isinstance(start_date,
                                                                                                       date) else ''
    end_date_str = end_date.strftime('%Y-%m-%d') if isinstance(end_date, datetime) or isinstance(end_date, date) else ''

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
    profiles = Profile.objects.values('website').distinct()
    x = Promo_code.objects.all()
    y = Id.objects.all()
    return render(request, 'promocode.html', {'y': y, 'profiles': profiles, 'x': x})


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

    # Fetch data for Main_page
    main_page_data = Main_page.objects.filter(date=today)

    if not main_page_data.exists():
        # If no data exists for today, find the most recent date with data
        most_recent_date = Main_page.objects.filter(date__lte=today).aggregate(Max('date'))['date__max']
        if most_recent_date:
            main_page_data = Main_page.objects.filter(date=most_recent_date)

    # Fetch data for Summary
    z = Summary.objects.filter(date=today)

    if not z.exists():
        # If no data exists for today, find the most recent date with data
        most_recent_summary_date = Summary.objects.filter(date__lte=today).aggregate(Max('date'))['date__max']
        if most_recent_summary_date:
            z = Summary.objects.filter(date=most_recent_summary_date)

    # Debugging logs for date ranges and data
    print(f"Start Date: {start_date}, Today: {today}")
    print(f"Main Page Query: {main_page_data.query}")
    print(f"Main Page Data: {list(main_page_data)}")
    print(f"Summary Data: {list(z)}")

    if main_page_data.exists():
        y = Id.objects.all()
        a = Summary.objects.filter(date__gte=start_date)

        # Prepare data for the bar chart
        conversion_data = {
            "views": a.aggregate(Sum('views'))['views__sum'] or 0,
            "clicks": a.aggregate(Sum('clicks'))['clicks__sum'] or 0,
            "direct_links": a.aggregate(Sum('direct_links'))['direct_links__sum'] or 0,
            "active_players": a.aggregate(Sum('active_players'))['active_players__sum'] or 0,
            "new_depositors": a.aggregate(Sum('new_depositors'))['new_depositors__sum'] or 0,
        }

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
    # Fetch initial data for the context
    x = Summary.objects.all()
    y = Id.objects.all()
    z = Profile.objects.all()
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
            # Parse custom start_date and end_date if provided
            try:
                if start_date:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                if end_date:
                    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                # Handle invalid date format
                start_date = end_date = None

        # Apply filters if valid dates are provided
        if start_date and end_date:
            payments = Summary.objects.filter(date__range=[start_date, end_date])

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
        'dates': dates
    })


def test(request):
    return render(request, 'test.html')


def webpages(request):
    # Fetch all profiles and related objects
    x = Profile.objects.all()
    profiles = Profile.objects.values('website').distinct()  # Get unique websites only
    y = Id.objects.all()
    z = Website.objects.all()

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
        'x': x,
        'profiles': current_page,
        'y': y,
        'z': z,
        'records_per_page': records_per_page,
        'total_records': total_records,
        'start_record': start_record,
        'end_record': end_record,
    })


def full_report(request):
    profiles = Profile.objects.values('website').distinct()
    y = Id.objects.all()
    x = Summary.objects.filter(date=date.today())  # Data for today's date
    z = Full_report.objects.all()

    # Initialize variables
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    time_interval = request.GET.get('time_interval', '')
    summaries = Summary.objects.none()  # Default to no data

    # Check if "Generate" button was clicked or time interval is selected
    if 'generate' in request.GET or time_interval:
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        today = datetime.today()

        # Handle time_interval values and set start_date and end_date
        if time_interval == 'exact':
            # Use provided start_date and end_date for Exact period
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date() if start_date else None
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else None
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
            # Parse custom start_date and end_date if provided
            try:
                if start_date:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                if end_date:
                    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                # Handle invalid date format
                start_date = end_date = None

        # Apply filters if valid dates are provided
        if start_date and end_date:
            summaries = Summary.objects.filter(date__range=[start_date, end_date])

    # Aggregate data for current and total summaries
    current_summary = summaries.aggregate(
        registrations=Sum('registrations'),
        new_depositors=Sum('new_depositors'),
        sum_of_all_deposits=Sum('sum_of_all_deposits'),
        revenue=Sum('revenue'),
        bonus_amount=Sum('bonus_amount'),
        overall_commission=Sum('overall_commission')
    )

    total_summary = Summary.objects.aggregate(
        registrations=Sum('registrations'),
        new_depositors=Sum('new_depositors'),
        sum_of_all_deposits=Sum('sum_of_all_deposits'),
        revenue=Sum('revenue'),
        bonus_amount=Sum('bonus_amount'),
        overall_commission=Sum('overall_commission')
    )

    # Format dates for template rendering
    start_date_str = start_date.strftime('%Y-%m-%d') if start_date else ''
    end_date_str = end_date.strftime('%Y-%m-%d') if end_date else ''

    # Render the template with filtered data
    return render(request, 'full_report.html', {
        'transactions': summaries,
        'start_date': start_date_str,
        'end_date': end_date_str,
        'current_summary': current_summary,
        'total_summary': total_summary,
        'y': y,
        'profiles': profiles,
        'x': x,
        'time_interval': time_interval,
        'z': z
    })


def cookies(request):
    return render(request, 'cookies.html')


def news(request):
    return render(request, 'news.html')


def privacy_policy(request):
    return render(request, 'privacy_policy')
