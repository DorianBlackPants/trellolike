from datetime import datetime

from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin


class AdminUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_superuser:
            now = datetime.now()
            last_action_not_decoded = request.session.get('last_action')
            if last_action_not_decoded:
                last_action = datetime.strptime(last_action_not_decoded, '%H-%M-%S %d/%m/%y')
                if (now - last_action).seconds > 5 * 60:
                    logout(request)
            request.session['last_action'] = datetime.now().strftime('%H-%M-%S %d/%m/%y')
