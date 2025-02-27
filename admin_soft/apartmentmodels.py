from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import RegexValidator

class Apartment(models.Model):  #apartment admin model
    apartment_name = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=150, unique=True)
    contact_number = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', 'Enter a valid 10-digit contact number')]
    )
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)
    password = models.CharField(max_length=128)  # Secure password storage
    role = models.CharField(max_length=128, default='admin')

    def set_password(self, raw_password):
        """Hashes and stores the password securely using Django's make_password."""
        self.password = make_password(raw_password)
        self.save(update_fields=["password"])

    def check_password(self, raw_password):
        """Checks if the given password matches the stored hash."""
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.name


class ApartmentFlat(models.Model):   #flat owner model
    PURPOSE_CHOICES = [
        ('Rental', 'Rental'),
        ('Owned', 'Owned'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Occupied', 'Occupied'),
        ('Maintenance', 'Maintenance'),
    ]

    FLAT_TYPES = [
        ('1BHK', '1 BHK'),
        ('2BHK', '2 BHK'),
        ('2.5BHK', '2.5 BHK'),
        ('3BHK', '3 BHK'),
        ('3.5BHK', '3.5 BHK'),
        ('4BHK', '4 BHK'),
        ('Studio', 'Studio'),
    ]

    flat_number = models.CharField(max_length=10, unique=True)
    flat_type = models.CharField(max_length=10, choices=FLAT_TYPES)
    apartment_name = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    owner_name = models.CharField(max_length=100)
    owner_contact = models.CharField(max_length=15)
    owner_email = models.EmailField()
    flat_size = models.CharField(max_length=10)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Available')
    purpose = models.CharField(max_length=10, choices=PURPOSE_CHOICES, default='Rental')
    proof_document = models.FileField(upload_to='flat_proofs/', blank=True, null=True)
    password = models.CharField(max_length=255, default='Pavan@123')
    role = models.CharField(max_length=128, default='owner')

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Flat {self.flat_number} - {self.purpose} ({self.status})"

class ApartmentPayment(models.Model):  #payment model
    PAYMENT_MODES = [
        ('CASH', 'Cash'),
        ('ONLINE', 'Online'),
        ('CHEQUE', 'Cheque'),
        ('BANK_TRANSFER', 'Bank Transfer'),
    ]
    
    PAYMENT_STATUS = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    
    flat = models.ForeignKey('ApartmentFlat', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    transaction_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODES)
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='PENDING')
    
    def __str__(self):
        return f"Payment of {self.amount} for Flat {self.flat.flat_number} on {self.payment_date} - {self.get_status_display()}"

from django.utils.timezone import now

class ApartmentComplaint(models.Model):
    owner = models.ForeignKey(ApartmentFlat, on_delete=models.CASCADE, related_name='complaints')
    subject = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(default=now)
    status = models.CharField(
        max_length=20, 
        choices=[('Pending', 'Pending'), ('solved', 'solved')], 
        default='Pending'
    )

    def __str__(self):
        return f"Complaint {self.id} - {self.subject} ({self.status})"


class ApartmentComplaintReply(models.Model):
    complaint = models.ForeignKey(ApartmentComplaint, on_delete=models.CASCADE, related_name='replies')
    sender = models.CharField(max_length=50, choices=[('Owner', 'Owner'), ('Admin', 'Admin')])
    message = models.TextField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"Reply by {self.sender} - {self.timestamp}"

from django.db import models
from django.utils.timezone import now

class ApartmentAnnouncement(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(default=now)
    
    def __str__(self):
        return f"Announcement: {self.title} ({self.created_at})"


class ApartmentAnnouncementReply(models.Model):
    announcement = models.ForeignKey(ApartmentAnnouncement, on_delete=models.CASCADE, related_name='replies')
    sender = models.CharField(max_length=50, choices=[('Owner', 'Owner'), ('Admin', 'Admin')])
    message = models.TextField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"Reply by {self.sender} - {self.timestamp}"
 