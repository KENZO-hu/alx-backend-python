from django.contrib.auth.models import User
from django.views import View
from django.shortcuts import redirect
from django.contrib import messages

class DeleteUserView(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            user.delete()
            messages.success(request, "Your account and all related data have been deleted.")
            return redirect('home')
        messages.error(request, "You must be logged in to delete your account.")
        return redirect('login')
