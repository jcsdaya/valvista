from .models import Visitor

class VisitorTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the visitor's IP address
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip() or request.META.get('REMOTE_ADDR', None)
        user_agent = request.META.get('HTTP_USER_AGENT', None)

        # Check if the visitor has already been registered based on IP address and user agent
        previous_visits = Visitor.objects.filter(ip_address=ip_address, user_agent=user_agent)

        # If no visitor is found, create a new visitor record
        if not previous_visits.exists():
            Visitor.objects.create(
                ip_address=ip_address,
                user_agent=user_agent
            )

        # Process the response
        response = self.get_response(request)
        return response