import random
from rest_framework.throttling import BaseThrottle
from rest_framework.throttling import SimpleRateThrottle

class RandomRateThrottle(BaseThrottle):

    def allow_request(self, request, view):
        return random.randint(1, 2) != 1

    def wait(self):
        return 60
    

class IPBasedThrottle(SimpleRateThrottle):
    scope = 'ip'  # This name links to settings.py throttle rate

    def get_cache_key(self, request, view):
        ip_addr = self.get_ident(request)  # Get client IP
        return self.cache_format % {
            'scope': self.scope,
            'ident': ip_addr
        }

    # To white list some ips
    WHITELISTED_IPS = ['192.168.1.1', '172.18.0.1']  # Add your IPs here
    def allow_request(self, request, view):
        ip = self.get_ident(request)
        print("ip.................",ip)
        # Bypass throttling for whitelisted IPs
        if ip in self.WHITELISTED_IPS:
            return True
        return super().allow_request(request, view)    

	# need to override if we are not getting correct ip address by get_ident() .
    # def get_ident(self, request):
    #     """
    #     Identify the machine making the request by IP address.
    #     Handles proxy servers by checking X-Forwarded-For header.
    #     """
    #     xff = request.META.get('HTTP_X_FORWARDED_FOR')
    #     if xff:
    #         # For requests behind proxies, get the first IP
    #         ip = xff.split(',')[0].strip()
    #     else:
    #         ip = request.META.get('REMOTE_ADDR')
    #     return ip
    
    
