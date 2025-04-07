from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Sum
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import SalesData
from decimal import Decimal, InvalidOperation
from datetime import datetime



def home(request):
    return render(request, 'index.html')

def navbar(request):
    return render(request, 'navbar.html')

def signin(request):
    if request.user.is_authenticated:
        return render(request, "signin.html")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")  # Redirect to the same page after login
        else:
            return render(request, "signin.html", {"error": "Invalid username or password"})

    return render(request, "signin.html")

@login_required
def signout(request):
    logout(request)
    return redirect("signin")

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created! Please wait for admin approval.")
            return redirect("signin")  # Redirect to login page
    else:
        form = SignUpForm()
    
    return render(request, "signup.html", {"form": form})

@login_required(login_url='signin')  # Redirects if not logged in
def profile(request):
    return render(request, 'profile.html')


@login_required(login_url='signin')
def dashboard(request):
    user_profile = Profile.objects.get(user=request.user)

    # Get all sales from approved agents
    sales = Sale.objects.filter(agent__is_approved=True).order_by('-price')

    # Get all approved agents with their total sales volume
    agents = Profile.objects.filter(is_approved=True).annotate(
        sales_volume=Sum('sales__price')
    ).order_by('-sales_volume')

    form = SaleForm(request.POST or None)  # Initialize form

    if request.method == 'POST':
        if form.is_valid():
            form.save()  # ✅ Save directly since 'agent' is now included
            return redirect('dashboard')  # Refresh the page
        else:
            print("Form errors:", form.errors)  # Debugging

    return render(request, 'dashboard.html', {
        'sales': sales,
        'agents': agents,
        'form': form,
        'user_profile': user_profile
    })


@login_required(login_url='signin')
def approve(request):
    accounts = Profile.objects.filter(is_approved=False)  # Get only unapproved users
    context = {
        'accounts': accounts,
    }
    return render(request, 'approve.html', context)

def approve_user(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    profile.is_approved = True
    profile.save()
    messages.success(request, f"{profile.user.username} has been approved!")
    return redirect('approve')

def reject_user(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    profile.user.delete()  # Deletes the user and profile
    messages.error(request, f"User {profile.user.username} has been declined.")
    return redirect('approve')

def developers(request):
    # Example data for sales_data
    sales_data = [
        {'active_sales': 1500.75, 'cancelled_sales': 200.50, 'developer': 'John Doe'},
        {'active_sales': 2500.00, 'cancelled_sales': 300.00, 'developer': 'Jane Smith'},
        {'active_sales': 1800.25, 'cancelled_sales': 150.75, 'developer': 'Alice Johnson'},
    ]
    return render(request, 'developers.html', {'sales_data': sales_data})

sales_data = []


def sales_report_view(request):
    selected_month = request.GET.get("month")  # Get the selected month from the dropdown
    selected_developer = request.GET.get("developer")  # Get the selected developer from the dropdown
    sales_data = SalesData.objects.all()

    if selected_month and selected_month.isdigit():  # Check if a specific month is selected
        sales_data = sales_data.filter(date__month=int(selected_month))

    if selected_developer:
        sales_data = sales_data.filter(developer=selected_developer)
       
    # Calculate monthly sales for the graph
    monthly_sales = SalesData.objects.values('date__month').annotate(
        total_active_sales=Sum('active_sales'),
        total_cancelled_sales=Sum('cancelled_sales')
    ).order_by('date__month')  # Include all months with data and order them

    # Prepare data for the graph
    months_with_data = [entry['date__month'] for entry in monthly_sales]
    active_sales_data = [entry['total_active_sales'] for entry in monthly_sales]
    cancelled_sales_data = [entry['total_cancelled_sales'] for entry in monthly_sales]
    
    if request.method == "POST":
        if "input_data" in request.POST:
            try:
                # Validate and convert input data
                active_sales = Decimal(request.POST.get("active_sales", "0").replace(",", "").strip())
                cancelled_sales = Decimal(request.POST.get("cancelled_sales", "0").replace(",", "").strip())
                developer = request.POST.get("developer", "").strip()
                date_str = request.POST.get("date", "").strip()

                # Validate and parse the date
                if not date_str:
                    raise ValueError("Date is required.")
                date = datetime.strptime(date_str, "%Y-%m-%d").date()

                # Save to the database
                SalesData.objects.create(
                    active_sales=active_sales,
                    cancelled_sales=cancelled_sales,
                    developer=developer,
                    date=date,
                )
                messages.success(request, "Sales data has been successfully saved.")
                return redirect(f"{reverse('sales_report')}?month={selected_month}")
            except (InvalidOperation, ValueError) as e:
                messages.error(request, f"Invalid input: {e}")
                return redirect(f"{reverse('sales_report')}?month={selected_month}")

        elif "edit_data" in request.POST:
            edit_id = int(request.POST.get("edit_id"))
            request.session["edit_id"] = edit_id
            return redirect(f"{reverse('sales_report')}?month={selected_month}")

        elif "save_edit" in request.POST:
            try:
                edit_id = request.session.get("edit_id")
                if edit_id is not None:
                    sales_data = SalesData.objects.get(id=edit_id)
                    sales_data.active_sales = Decimal(request.POST.get("active_sales", "0").replace(",", "").strip())
                    sales_data.cancelled_sales = Decimal(request.POST.get("cancelled_sales", "0").strip())
                    sales_data.developer = request.POST.get("developer", "").strip()
                    date_str = request.POST.get("date", "").strip()

                    # Validate and parse the date
                    if not date_str:
                        raise ValueError("Date is required.")
                    sales_data.date = datetime.strptime(date_str, "%Y-%m-%d").date()

                    sales_data.save()
                    del request.session["edit_id"]
                messages.success(request, "Sales data has been successfully updated.")
                return redirect(f"{reverse('sales_report')}?month={selected_month}")
            except (InvalidOperation, ValueError) as e:
                messages.error(request, f"Invalid input: {e}")
                return redirect(f"{reverse('sales_report')}?month={selected_month}")

        elif "delete_data" in request.POST:
            delete_id = int(request.POST.get("delete_id"))
            SalesData.objects.filter(id=delete_id).delete()
            messages.success(request, "Sales data has been successfully deleted.")
            return redirect(f"{reverse('sales_report')}?month={selected_month}")

    # Check if editing mode is active
    edit_id = request.session.get("edit_id")
    edit_data = SalesData.objects.filter(id=edit_id).first() if edit_id else None

    developers = SalesData.objects.values_list('developer', flat=True).distinct()

    return render(request, "sales_report.html", {
        "sales_data": sales_data,
        "edit_data": edit_data,
        "selected_month": selected_month,
        "selected_developer": selected_developer,
        "months_with_data": months_with_data,  # Pass months with data to the template
        "active_sales_data": active_sales_data,  # Pass active sales data to the template
        "cancelled_sales_data": cancelled_sales_data,  # Pass cancelled sales data to the template
        "developers": developers,
    })

def commission(request):
    # Add your logic for the commission view here
    return render(request, 'commission.html')