from django.contrib.gis.geoip2 import GeoIP2

# Get user location and ip
def get_client_ip(request):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        location, err = get_user_location(ip)
        if err != None:
            raise Exception(str(err))
        return ip, location, err
    except Exception as e:
        return None, None, str(e)


def get_user_location(ip):
    try:
        g = GeoIP2()
        location = g.city(ip)
        return location, None
    except Exception as e:
        return None, str(e)
