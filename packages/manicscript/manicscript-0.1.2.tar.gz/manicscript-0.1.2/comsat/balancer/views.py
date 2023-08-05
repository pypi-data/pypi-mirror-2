from django.conf import settings
from django import http
from random import choice, randint

def _rand_host():
        return ''.join([choice('abcdefghijklmnopqrstuvwxyz1234567890') for i in range(16)])

def _rand_id():
        max_id = settings.BALANCER['max_id']
        min_id = settings.BALANCER['min_id']

        return randint( min_id, max_id )

def choose_host(request, suffix):
        host_string = _rand_host()
        host_id = _rand_id()
        url = settings.BALANCER['host_template'] % (host_string, host_id, suffix)
        return http.HttpResponseRedirect(url)
