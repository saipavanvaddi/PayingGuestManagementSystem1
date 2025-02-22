from django.urls import path
from admin_soft import views
from admin_soft import pgviews
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('pg/owner-login', pgviews.PGLoginViewOwner.as_view(), name='pg_owner_login'),
    path('pg/owner_dashboard', pgviews.dashboard_view, name='pg_owner_dashboard'),
    path("pg/owner-logout/", pgviews.pg_owner_logout, name="pg_owner_logout"),
    path('manage-pg/', pgviews.manage_pg, name='manage_pg'),    
    path('rooms/', pgviews.room_dashboard, name='room_dashboard'),
    path('rooms/add/', pgviews.add_room, name='add_room'),
    path('rooms/edit/<int:room_id>/', pgviews.edit_room, name='edit_room'),
    path('rooms/delete/<int:room_id>/', pgviews.delete_room, name='delete_room'),
    path('pg-owner/', pgviews.pg_owner_profile, name='pg_owner_profile'),
    path('tenants/', pgviews.pg_owner_tenant_dashboard, name='pg_owner_tenant_dashboard'),
    path('pg-owner/edit/', pgviews.pg_owner_profile_edit, name='pg_owner_profile_edit'),
    
    path("edit-room/<int:room_id>/", pgviews.edit_room, name="edit_room"),
    path('edit-tenant/<int:tenant_id>/', pgviews.edit_tenant, name='edit_tenant'),
    path('delete-tenant/<int:tenant_id>/',pgviews.delete_tenant, name='delete_tenant'),
    path('pg/tenant/login/', pgviews.TenantLoginView.as_view(), name='pg_tenant_login'),
    path('pg/tenant/dashboard', pgviews.tenant_dashboard, name='pg_tenant_dashboard'),
    path("pg/tenants/profile/", pgviews.pg_tenant_profile, name="pg_tenant_profile"),
    path("pg/tenants/profile/edit/", pgviews.pg_tenant_edit_profile, name="pg_tenant_profile_edit"),
    path("pg/tenants/complaints/", pgviews.pg_tenant_complaints, name="pg_tenant_complaints"),
    path("pg/tenants/payments/", pgviews.pg_tenant_payments, name="pg_tenant_payments"),
    path("pg/tenants/logout/", pgviews.pg_tenant_logout, name="pg_tenant_logout"),
    path('payments/', pgviews.pg_tenant_payments, name='pg_tenant_payments'),
    path('make_payment/', pgviews.pg_tenant_make_payment, name='pg_tenant_make_payment'),

    path('owner/payments/', pgviews.owner_payments, name='owner_payments'),
    # path('owner/payment/update/<int:payment_id>/', pgviews.update_payment_status, name='update_payment_status'),

    # Complaints
    path('owner/complaints/', pgviews.owner_complaints, name='owner_complaints'),
    path('owner/complaint/resolve/<int:complaint_id>/', pgviews.resolve_complaint, name='resolve_complaint'),
    path('owner/payment/complete/<int:payment_id>/', pgviews.mark_payment_completed, name='mark_payment_completed'),
    path('owner/payment/failed/<int:payment_id>/', pgviews.mark_payment_failed, name='mark_payment_failed'),


    
    path('', views.index, name='index'),
    path('billing/', views.billing, name='billing'),
    path('tables/', views.tables, name='tables'),
    path('vr/', views.vr, name='vr'),
    path('rtl/', views.rtl, name='rtl'),
    path('profile/', views.profile, name='profile'),
    # Authentication
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name="password_change_done"),
    path('accounts/password-reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', 
        views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
        path('', views.hospital_owner_login, name='hospital_owner_login'),
    path('hospital_owner_logout/', views.hospital_owner_logout, name='hospital_owner_logout'),
    path('hospital_dashboard/', views.hospital_dashboard, name='hospital_dashboard'),
    path("add_patient/", views.add_patient, name="add_patient"),
    path('patients/', views.patient_list, name='patient_list'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path("add_doctor/", views.add_doctor, name="add_doctor"),
    path('edit_patient/<int:pk>/', views.edit_patient, name='edit_patient'),
    path('delete_patient/<int:pk>/', views.delete_patient, name='delete_patient'),
    path('edit_doctor/<int:doctor_id>/', views.edit_doctor, name='edit_doctor'),
    path('delete_doctor/<int:doctor_id>/', views.delete_doctor, name='delete_doctor'),
    path('medicine/add/', views.manage_medicine, name='add_medicine'),
    path('medicine/edit/<int:pk>/', views.manage_medicine, name='edit_medicine'),
    path('medicine/delete/<int:pk>/', views.delete_medicine, name='delete_medicine'),
    path('create_user/', views.create_user, name='create_user'),
    path("hospital_user_login/", views.hospital_user_login, name="hospital_user_login"),
    path("hospital_user_dashboard/", views.hospital_user_dashboard_view, name="hospital_user_dashboard"),
    path("hospital_user_logout/", views.hospital_user_logout, name="hospital_user_logout"),
    path('user_profile/<int:user_id>/', views.hospital_user_profile_view, name='hospital_user_profile'),
    path('add_slot/', views.add_available_slot, name='add_available_slot'),
    path('view_slots/', views.view_available_slots, name='view_available_slots'),
    path('book_appointment/', views.book_appointment, name='book_appointment'),
    path('check_slots/', views.check_available_slots, name='check_available_slots'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('update_appointment_status/<int:appointment_id>/', views.update_appointment_status, name='update_appointment_status'),
    path('user-hospital-list/', views.user_hospital_list, name='user_hospital_list'),
    # path('fun/', views.hospital_sample, name='index'),
    path('logout/', views.hospital_owner_logout, name='admin_logout'),  # Ensure this is present
    path('logout/', views.hospital_owner_logout, name='logout'),  # Ensure this is present
]
