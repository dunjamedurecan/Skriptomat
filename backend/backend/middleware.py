import logging
from django.http import HttpResponseForbidden

logger = logging.getLogger(__name__)

class SecurityMonitoringMiddleware:
    """
    Middleware za detekciju sumnjivih zahtjeva i pokušaja exploit-ovanja.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Sumnjivi paterni koji ukazuju na Next.js exploit pokušaje
        self.suspicious_patterns = [
            '/_next/',
            '/api/_next/',
            '/__nextjs_',
            'RSC',  # React Server Components
            'flight',  # RSC flight protocol
        ]
        
    def __call__(self, request):
        # Provjeri sumnjive paterne u path-u
        path = request.path.lower()
        for pattern in self.suspicious_patterns:
            if pattern.lower() in path:
                logger.warning(
                    f"[SECURITY] Suspiciozni zahtjev detektiran! "
                    f"IP: {self.get_client_ip(request)}, "
                    f"Path: {request.path}, "
                    f"User-Agent: {request.META.get('HTTP_USER_AGENT', 'N/A')}, "
                    f"Pattern: {pattern}"
                )
                # Opciono: blokiraj zahtjev
                # return HttpResponseForbidden("Forbidden")
        
        # Provjeri sumnjive headere
        content_type = request.META.get('CONTENT_TYPE', '')
        if 'rsc' in content_type.lower():
            logger.warning(
                f"[SECURITY] RSC Content-Type detektiran! "
                f"IP: {self.get_client_ip(request)}, "
                f"Content-Type: {content_type}"
            )
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """Dohvati pravu IP adresu klijenta (uzimajući u obzir proxy)."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
