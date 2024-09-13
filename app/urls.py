from django.urls import path
from app import views

urlpatterns = [
    path('register/', views.UserRegistrationAPI.as_view(), name='registration'),
    path('leave_request/', views.LeaveRequest.as_view(), name='request_leave'),
    path('managers_list/', views.ManagerList.as_view(), name='list_managers'),
    path('hr_view_leaves/', views.HRlistleaves.as_view(), name='list_leaves_hr'),
    path('manager_view_leaves/', views.Managerlistleaves.as_view(), name='list_leaves_manager'),
    path('manager_approve_leave/<int:id>/', views.ManagerApprove.as_view(), name='approve_leave'),

    
]
