from django.contrib.gis.geoip2 import GeoIP2


def get_client_ip(request):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        location = get_user_location(ip)

        return ip, location
    except Exception as e:
        return str(e)


def get_user_location(ip):
    try:
        g = GeoIP2()
        location = g.city(ip)
        return location
    except Exception as e:
        return str(e)
