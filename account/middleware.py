from datetime import datetime
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect


class UserAutoLogoutMiddleware:
    """
    auto sends all anonimous users to login page
    auto logouts user (not staff) if no actions longer than 1 min
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_anonymous:
            return redirect('account:login')
        if not request.user.is_staff:
            time_now = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
            last_time_active = request.session.get('last_time_active')
            if last_time_active:
                last_time_active = datetime.strptime(last_time_active, "%Y-%m-%d %H:%M:%S")
                time_passed_since_last_request = datetime.strptime(time_now, "%Y-%m-%d %H:%M:%S") - last_time_active
                if time_passed_since_last_request.seconds > settings.FORCE_LOGOUT_USER:
                    logout(request)
                    messages.add_message(request, messages.INFO, 'you have been auto logged off due to inactivity')
                    return redirect('account:login')
            request.session['last_time_active'] = time_now
        response = self.get_response(request)
        return response
