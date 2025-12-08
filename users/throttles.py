# users/throttles.py
from rest_framework.throttling import SimpleRateThrottle

class IPRateThrottle(SimpleRateThrottle):
    scope = 'ip'
    def get_cache_key(self, request, view):
        ident = self.get_ident(request)
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }

class EmailRateThrottle(SimpleRateThrottle):
    scope = 'email'
    def get_cache_key(self, request, view):
        # only apply when an email is present (registration views)
        email = request.data.get('email')
        if not email:
            return None
        return self.cache_format % {
            'scope': self.scope,
            'ident': email.lower()
        }
