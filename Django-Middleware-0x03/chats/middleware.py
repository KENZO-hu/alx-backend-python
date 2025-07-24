import time
from datetime import datetime
from django.http import HttpResponseForbidden
from collections import defaultdict
from threading import Lock

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.lock = Lock()
        self.log_file = 'requests.log'

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}\\n"
        with self.lock:
            with open(self.log_file, 'a') as f:
                f.write(log_message)
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Deny access if outside 9PM (21) to 6PM (18)
        if current_hour < 18 or current_hour >= 21:
            return HttpResponseForbidden("Access to chat is restricted during this time.")
        response = self.get_response(request)
        return response

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_counts = defaultdict(list)  # IP -> list of timestamps
        self.lock = Lock()
        self.limit = 5  # messages
        self.time_window = 60  # seconds

    def __call__(self, request):
        if request.method == 'POST':
            ip = self.get_client_ip(request)
            now = time.time()
            with self.lock:
                timestamps = self.message_counts[ip]
                # Remove timestamps older than time_window
                timestamps = [t for t in timestamps if now - t < self.time_window]
                if len(timestamps) >= self.limit:
                    return HttpResponseForbidden("Message limit exceeded. Please wait before sending more messages.")
                timestamps.append(now)
                self.message_counts[ip] = timestamps
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if not user.is_authenticated:
            return HttpResponseForbidden("You must be logged in to access this resource.")
        # Assuming user has a 'role' attribute
        if not hasattr(user, 'role') or user.role not in ['admin', 'moderator']:
            return HttpResponseForbidden("You do not have permission to access this resource.")
        response = self.get_response(request)
        return response
