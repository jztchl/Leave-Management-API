from django.shortcuts import render
from app.serializers import usersSerializers, leaveSerializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from app.models import users, leaveRequest, leavelist
from django.http import HttpResponseForbidden
from functools import wraps
from django.db import transaction

def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("You need to be logged in to access this page.")
            
            if request.user.role not in roles:
                return HttpResponseForbidden("You do not have permission to access this page.")
            
            return view_func(self, request, *args, **kwargs)
        return _wrapped_view
    return decorator


class UserRegistrationAPI(APIView):
    def post(self, request):
        user = request.data
        serializer = usersSerializers(data=user)
        if serializer.is_valid():
            serializer.save()
            msg = {"status": "success", "data": serializer.data}
            return Response(msg, status=status.HTTP_200_OK)
        else:
            msg = {"status": "error", "data": serializer.errors}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

class LeaveRequest(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        leave_data = request.data
        manager_id = leave_data.get('AssignedManager')
        
        if not manager_id:
            msg = {"status": "error", "message": "Manager ID is required."}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        try:
            manager = users.objects.get(id=manager_id)
        except users.DoesNotExist:
            msg = {"status": "error", "message": "Invalid Manager ID."}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = leaveSerializers(data=leave_data, partial=True)
        if serializer.is_valid():
            serializer.save(employee=request.user, AssignedManager=manager)
            msg = {"status": "success", "data": serializer.data}
            return Response(msg, status=status.HTTP_200_OK)
        else:
            msg = {"status": "error", "data": serializer.errors}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

class ManagerList(APIView):
    permission_classes = (IsAuthenticated,)  
    def get(self, request):
        selected_users = users.objects.filter(role='MANAGER')
        serializer = usersSerializers(selected_users, many=True)
        msg = {"status": "success", "data": serializer.data}
        return Response(msg, status=status.HTTP_200_OK)

class HRlistleaves(APIView):
    permission_classes = (IsAuthenticated,) 
    @role_required('HR')  
    def get(self, request):
        LeaveList = leaveRequest.objects.all()
        serializer = leaveSerializers(LeaveList, many=True)
        msg = {"status": "success", "data": serializer.data}
        return Response(msg, status=status.HTTP_200_OK)

class Managerlistleaves(APIView):
    permission_classes = (IsAuthenticated,)  
    @role_required('MANAGER')   
    def get(self, request):
        LeaveList = leaveRequest.objects.filter(AssignedManager=request.user)
        serializer = leaveSerializers(LeaveList, many=True)
        msg = {"status": "success", "data": serializer.data}
        return Response(msg, status=status.HTTP_200_OK)
    

class ManagerApprove(APIView):
    permission_classes = (IsAuthenticated,)

    @role_required('MANAGER')
    def patch(self, request, id=None):
        try:
            with transaction.atomic():
                # Lock the leave request row to prevent concurrent modifications
                selected_leave = leaveRequest.objects.select_for_update().get(id=id)
                selected_leave.ManagerApproval = True
                selected_leave.save()

                selected_user = users.objects.select_for_update().get(id=selected_leave.employee.id)

                # Lock and ensure the user has a related leavelist
                user_leavelist, created = leavelist.objects.select_for_update().get_or_create(employee=selected_user)

                # Update leave balance with safety check
                if user_leavelist.paidleave < 2:
                    user_leavelist.paidleave += 1
                else:
                    user_leavelist.unpaidleave += 1

                user_leavelist.save()

            msg = {"status": "success"}
            return Response(msg, status=status.HTTP_200_OK)

        except leaveRequest.DoesNotExist:
            msg = {"status": "error", "message": "Leave request not found"}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)

        except users.DoesNotExist:
            msg = {"status": "error", "message": "User not found"}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            msg = {"status": "error", "message": str(e)}
            return Response(msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)