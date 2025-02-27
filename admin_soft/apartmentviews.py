from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.views import *
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from admin_soft.forms import *
from .apartmentmodels import *
from django.utils import timezone
from datetime import date
from .apartmentforms import *
from django.views.generic import DetailView
class ApartmentLoginViewAdmin(View):
    template_name = 'apartment/admin/apartment_admin_login.html'
    form_class = ApartmentLoginFormAdmin
    
    def get(self, request, *args, **kwargs):
        """If already logged in, redirect to dashboard."""
        if request.session.get("apartment_id"):  # Check if apartment admin is logged in
            return redirect("apartment_admin_dashboard")
        
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        """Handle login authentication."""
        if request.session.get("apartment_id"):  # If already logged in, redirect to dashboard
            return redirect("apartment_admin_dashboard")

        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            try:
                # Assuming 'name' is used as the username field.
                apartment = Apartment.objects.get(name=username)
                
                if check_password(password, apartment.password):  # Check hashed password
                    request.session["apartment_id"] = apartment.id  # Store apartment admin details in session
                    request.session["apartment_name"] = apartment.apartment_name
                    messages.success(request, "Login successful.")
                    return redirect("apartment_admin_dashboard")
                else:
                    messages.error(request, "Invalid password.")
            except Apartment.DoesNotExist:
                messages.error(request, "Apartment admin does not exist.")

        return render(request, self.template_name, {"form": form})

def apartment_admin_dashboard(request):
    """Apartment admin dashboard view."""
    if not request.session.get("apartment_id"):  # Check if apartment admin is logged in
        return redirect("apartment_admin_login")
    apartment_id = request.session.get("apartment_id")
    apartment = Apartment.objects.get(id=apartment_id)
    return render(request, 'apartment/admin/apartment_admin_dashboard.html', {"apartment": apartment})

def apartment_admin_logout(request):
    """Apartment admin logout view."""
    logout(request)
    return redirect("apartment_admin_login")
 


def list_flats(request):
    apartment_id = request.session.get("apartment_id")
    apartment = Apartment.objects.get(id=apartment_id)
    flats = ApartmentFlat.objects.filter(apartment_name=apartment)
    return render(request, 'apartment/admin/flat/apartment_flat_dashboard.html', {'flats': flats, 'apartment': apartment})

def add_flat(request):
    apartment_id = request.session.get("apartment_id")
    apartment = Apartment.objects.get(id=apartment_id)
    if request.method == 'POST':
        print("hai")
        form = ApartmentFlatFormAdmin(request.POST)
        if form.is_valid():
            print("form valide")
            flat=form.save(commit=False)
            flat.apartment_name = apartment
            flat.save()
            return redirect('list_flats')
    else:
        form = ApartmentFlatFormAdmin()
    return render(request, 'apartment/admin/flat/apartment_flat_add.html', {'form': form, 'apartment':'apartment'})

class ApartmentFlatDetailView(DetailView):
    model = ApartmentFlat
    template_name = 'apartment/admin/flat/apartment_flat_detail.html'
    context_object_name = 'flat'

def edit_flat(request, pk):
    flat = get_object_or_404(ApartmentFlat, pk=pk)
    if request.method == 'POST':
        form = ApartmentFlatFormAdmin(request.POST, instance=flat)
        if form.is_valid():
            form.save()
            return redirect('list_flats')
    else:
        form = ApartmentFlatFormAdmin(instance=flat)
    return render(request, 'apartment/admin/flat/apartment_flat_edit.html', {'form': form, 'flat': flat})

def delete_flat(request, pk):
    flat = get_object_or_404(ApartmentFlat, pk=pk)
    if request.method == 'POST':
        flat.delete()
        return redirect('list_flats')
    return render(request, 'apartment/admin/flat/apartment_flat_delete.html', {'flat': flat})
from datetime import datetime
from django.db.models import Q
from django.shortcuts import render

def list_payments(request):
    payments = ApartmentPayment.objects.all().select_related('flat')

    # Get the current month and year
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Handle the 'search' filter: searches transaction_id, remarks, and flat number.
    search_query = request.GET.get('search', '').strip()
    if search_query:
        payments = payments.filter(
            Q(transaction_id__icontains=search_query) |
            Q(remarks__icontains=search_query) |
            Q(flat__flat_number__icontains=search_query)
        )

    # Handle the 'status' filter.
    status = request.GET.get('status', '').strip()
    if status:
        payments = payments.filter(status=status)

    # Handle the 'month' filter (default: current month)
    month = request.GET.get('month', '').strip()
    if not month or not month.isdigit():  # Default to current month if not provided
        month = str(current_month)
    payments = payments.filter(payment_date__month=int(month))

    # Handle the 'year' filter (default: current year)
    year = request.GET.get('year', '').strip()
    if not year or not year.isdigit():  # Default to current year if not provided
        year = str(current_year)
    payments = payments.filter(payment_date__year=int(year))

    # Generate the list of years from 2024 to the current year.
    years = range(2024, current_year + 1)

    # Dictionary of months for dropdown
    months = {
        "1": "January", "2": "February", "3": "March",
        "4": "April", "5": "May", "6": "June",
        "7": "July", "8": "August", "9": "September",
        "10": "October", "11": "November", "12": "December"
    }

    context = {
        'payments': payments.order_by('-payment_date'),
        'years': years,
        'months': months,
        'selected_month': month,
        'selected_year': year,
    }

    # For AJAX requests, return only the payments table partial.
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'apartment/admin/payment/partials/payments_table.html', context)

    return render(request, 'apartment/admin/payment/apartment_admin_payment.html', context)

def update_payment_status(request):
    payment_id = request.POST.get('payment_id')
    new_status = request.POST.get('status')
    remarks = request.POST.get('remarks', '')

    payment = get_object_or_404(ApartmentPayment, pk=payment_id)
    payment.status = new_status
    payment.remarks = remarks
    payment.save()
    
    return redirect('apartment_payments')




def apartment_flat_login(request):
    """Handles apartment owner login."""
    if request.method == "POST":
        form = ApartmentFlatLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            try:
                owner = ApartmentFlat.objects.get(owner_name=username)
                if check_password(password, owner.password):
                    request.session["owner_id"] = owner.id
                    messages.success(request, "Login successful!")
                    return redirect("apartment_flat_dashboard")
                else:
                    messages.error(request, "Invalid password.")
            except Apartment.DoesNotExist:
                messages.error(request, "Owner not found.")

    else:
        form = ApartmentFlatLoginForm()

    return render(request, "apartment/owner/flat_login.html", {"form": form})

def apartment_flat_logout(request):
    """Handles apartment owner logout."""
    request.session.flush()
    messages.success(request, "Logged out successfully!")
    return redirect("apartment_flat_login")

def apartment_flat_dashboard(request):
    """Owner's dashboard after login."""
    return render(request, "apartment/owner/flat_dashboard.html")


def apartment_flat_complaints(request):
    """Handles complaint creation and listing for apartment owners."""
    owner_id = request.session.get("owner_id")
    if not owner_id:
        messages.error(request, "You must be logged in to access this page.")
        return redirect("apartment_flat_login")

    owner = get_object_or_404(ApartmentFlat, id=owner_id)
    complaints = ApartmentComplaint.objects.filter(owner=owner).order_by("-created_at")

    if request.method == "POST":
        form = ApartmentComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.owner = owner
            complaint.save()
            messages.success(request, "Complaint submitted successfully.")
            return redirect("apartment_flat_complaints")
        else:
            messages.error(request, "There was an error submitting the complaint.")
    else:
        form = ApartmentComplaintForm()

    return render(request, "apartment/owner/complaint/complaints.html", {"form": form, "complaints": complaints})



def apartment_flat_complaint_replies(request, complaint_id):
    """View and reply to complaints for an owner."""
    
    owner_id = request.session.get("owner_id")
    if not owner_id:
        messages.error(request, "You must be logged in to access this page.")
        return redirect("apartment_flat_login")

    complaint = get_object_or_404(ApartmentComplaint, id=complaint_id, owner_id=owner_id)
    replies = complaint.replies.all()
    owner = ApartmentFlat.objects.get(id=owner_id)

    if request.method == "POST":
        message = request.POST.get("message")
        if message:
            ApartmentComplaintReply.objects.create(
                complaint=complaint,
                sender=owner.owner_name, # Ensure the role is set for filtering
                message=message,
            )
            messages.success(request, "Your reply has been posted.")
            return redirect("apartment_flat_complaint_replies", complaint_id=complaint.id)

    return render(
        request,
        "apartment/owner/complaint/complaint_replies.html",
        {"complaint": complaint, "replies": replies},
    )


def admin_complaint_list(request):
    """Admin Complaint List with Filters."""
    complaints = ApartmentComplaint.objects.all()
    owners = ApartmentFlat.objects.all()  # Get all owners for dropdown
    STATUS_CHOICES = ApartmentComplaint._meta.get_field("status").choices
    # Filtering based on user input
    search_query = request.GET.get("search", "")
    status_filter = request.GET.get("status", "")
    owner_filter = request.GET.get("owner", "")

    if search_query:
        complaints = complaints.filter(subject__icontains=search_query)

    if status_filter:
        complaints = complaints.filter(status=status_filter)

    if owner_filter:
        complaints = complaints.filter(owner_id=owner_filter)

    return render(
        request,
        "apartment/admin/complaint/complaint_list.html",
        {"complaints": complaints, "owners": owners, "status_choices": STATUS_CHOICES},
    )

def admin_complaint_reply(request, complaint_id):
    """Admin can view and reply to complaints."""
    complaint = get_object_or_404(ApartmentComplaint, id=complaint_id)
    apartment_id = request.session.get("apartment_id")
    apartment = Apartment.objects.get(id=apartment_id)

    if not apartment_id:
        messages.error(request, "You must be logged in as an admin to access this page.")
        return redirect("apartment_admin_login")

    apartment = Apartment.objects.get(id=apartment_id)

    # Fetch all replies related to this complaint
    replies = ApartmentComplaintReply.objects.filter(complaint=complaint).order_by("timestamp")

    if request.method == "POST":
        form = ApartmentComplaintReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.complaint = complaint
            reply.sender = apartment.name  # Ensure sender is properly stored
            # reply.role = "Admin"  # Assign role explicitly
            reply.save()
            messages.success(request, "Reply sent successfully.")
            return redirect("apartment_admin_complaint_reply", complaint_id=complaint.id)
        else:
            messages.error(request, "There was an error sending the reply.")
    else:
        form = ApartmentComplaintReplyForm()

    return render(
        request,
        "apartment/admin/complaint/complaint_reply.html",
        {"form": form, "complaint": complaint, "replies": replies},
    )

def apartment_mark_complaint_solved(request, complaint_id):
    """Marks the complaint as solved."""
    complaint = get_object_or_404(ApartmentComplaint, id=complaint_id)
    complaint.status = 'solved'
    complaint.save()
    messages.success(request, "Complaint marked as solved!")
    return redirect("apartment_flat_complaints") 

import uuid

def make_payment(request):
    if request.method == "POST":
        form = ApartmentPaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            # payment.transaction_id =  # str(uuid.uuid4())  # Generate a unique transaction ID
            payment.status = "PENDING"  # Default status
            payment.save()
            messages.success(request, "Payment submitted successfully!")
            return redirect("owner_payments_view")
    else:
        form = ApartmentPaymentForm()
    return render(request, "apartment/owner/payment/make_payment.html", {"form": form})


def view_payments(request):
    flat_id= request.session.get("owner_id")
    flat = ApartmentFlat.objects.get(id=flat_id)
    payments = ApartmentPayment.objects.filter(flat_id=flat_id)  # Assuming `owner` is linked to `User`
    return render(request, "apartment/owner/payment/view_payments.html", {"payments": payments})



def send_announcement(request):
    apartment_id = request.session.get("apartment_id")
    apartment = get_object_or_404(Apartment, id=apartment_id)

    if request.method == 'POST':
        form = ApartmentAnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.apartment = apartment  # Assign the apartment
            announcement.save()
            return redirect('list_announcements')  # Redirect to a page showing announcements
    else:
        form = ApartmentAnnouncementForm()
    
    return render(request, 'apartment/admin/announcement/announcement_send.html', {'form': form})

def owner_announcements(request):
    apartment_id = request.session.get("apartment_id")
    announcements = ApartmentAnnouncement.objects.filter(apartment_id=apartment_id).order_by('-created_at')
    
    return render(request, 'apartment/owner/announcement/announcement_list.html', {'announcements': announcements})
def list_announcements(request):
    apartment_id = request.session.get("apartment_id")
    announcements = ApartmentAnnouncement.objects.filter(apartment_id=apartment_id).order_by('-created_at')
    
    return render(request, 'apartment/admin/announcement/announcement_list.html', {'announcements': announcements})



def flat_owner_profile(request):
    owner_id = request.session.get("owner_id")
    owner = ApartmentFlat.objects.get(id=owner_id)
    return render(request, 'apartment/owner/profile.html', {'owner': owner})

def flat_edit_owner_profile(request):
    owner_id = request.session.get("owner_id")
    owner = ApartmentFlat.objects.get(id=owner_id)  # Assuming email authentication
    if request.method == 'POST':
        form = OwnerProfileForm(request.POST, instance=owner)
        if form.is_valid():
            form.save()
            return redirect('flat_owner_profile')  # Redirect to profile after saving
    else:
        form = OwnerProfileForm(instance=owner)
    
    return render(request, 'apartment/owner/edit_profile.html', {'form': form})


def send_announcement(request):
    apartment_id = request.session.get("apartment_id")
    apartment = get_object_or_404(Apartment, id=apartment_id)

    if request.method == 'POST':
        form = ApartmentAnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.apartment = apartment  # Assign the apartment
            announcement.save()
            return redirect('list_announcements')  # Redirect to a page showing announcements
    else:
        form = ApartmentAnnouncementForm()
    
    return render(request, 'apartment/admin/announcement/announcement_send.html', {'form': form})

def owner_announcements(request):
    apartment_id = request.session.get("apartment_id")
    announcements = ApartmentAnnouncement.objects.filter(apartment_id=apartment_id).order_by('-created_at')
    
    return render(request, 'apartment/owner/announcement/announcement_list.html', {'announcements': announcements})
def list_announcements(request):
    apartment_id = request.session.get("apartment_id")
    announcements = ApartmentAnnouncement.objects.filter(apartment_id=apartment_id).order_by('-created_at')
    
    return render(request, 'apartment/admin/announcement/announcement_list.html', {'announcements': announcements})



# ------------------ ANNOUNCEMENT CONVERSATION (Replies) ------------------ #
def admin_announcement_conversation(request, announcement_id):
    """Admin: View and reply to an announcement."""
    
    apartment_id = request.session.get("apartment_id")
    if not apartment_id:
        messages.error(request, "You must be logged in as an admin to access this page.")
        return redirect("apartment_admin_login")

    apartment = get_object_or_404(Apartment, id=apartment_id)
    announcement = get_object_or_404(ApartmentAnnouncement, id=announcement_id, apartment=apartment)
    replies = announcement.replies.all()

    if request.method == "POST":
        message = request.POST.get("message")
        if message:
            ApartmentAnnouncementReply.objects.create(
                announcement=announcement,
                sender=apartment.name,
                message=message,
            )
            messages.success(request, "Your reply has been posted.")
            return redirect("admin_announcement_conversation", announcement_id=announcement.id)

    return render(
        request,
        "apartment/admin/announcement/announcement_conversation.html",
        {"announcement": announcement, "replies": replies},
    )

def owner_announcement_conversation(request, announcement_id):
    """Owner: View and reply to an announcement."""
    
    owner_id = request.session.get("owner_id")
    if not owner_id:
        messages.error(request, "You must be logged in as an owner to access this page.")
        return redirect("apartment_flat_login")

    owner = get_object_or_404(ApartmentFlat, id=owner_id)
    announcement = get_object_or_404(ApartmentAnnouncement, id=announcement_id, apartment=owner.apartment_name)
    replies = announcement.replies.all()

    if request.method == "POST":
        message = request.POST.get("message")
        if message:
            ApartmentAnnouncementReply.objects.create(
                announcement=announcement,
                sender=owner.owner_name,
                message=message,
            )
            messages.success(request, "Your reply has been posted.")
            return redirect("owner_announcement_conversation", announcement_id=announcement.id)

    return render(
        request,
        "apartment/owner/announcement/announcement_conversation.html",
        {"announcement": announcement, "replies": replies},
    )
