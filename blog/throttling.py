import random
from rest_framework.throttling import BaseThrottle

class RandomRateThrottle(BaseThrottle):

    def allow_request(self, request, view):
        return random.randint(1, 2) != 1

    def wait(self):
        return 60