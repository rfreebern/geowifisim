# From http://seewah.blogspot.com/2009/11/gpolyline-decoding-in-python.html
# By See Wah Cheng

def decode_line(encoded):
    """Decodes a polyline that was encoded using the Google Maps method.

    See http://code.google.com/apis/maps/documentation/polylinealgorithm.html

    This is a Python port of Mark McClure's JavaScript polyline decoder
    (http://facstaff.unca.edu/mcmcclur/GoogleMaps/EncodePolyline/decode.js)
    and Peter Chng's PHP polyline decode
    (http://unitstep.net/blog/2008/08/02/decoding-google-maps-encoded-polylines-using-php/)
    """

    encoded_len = len(encoded)
    index, array, lat, lng = 0, [], 0, 0

    while index < encoded_len:
        b, shift, result = 0, 0, 0

        while True:
            b = ord(encoded[index]) - 63
            index += 1
            result |= (b & 0x1f) << shift
            shift += 5
            if b < 0x20:
                break

        dlat = ~(result >> 1) if result & 1 else result >> 1
        lat += dlat
        shift, result = 0, 0

        while True:
            b = ord(encoded[index]) - 63
            index += 1
            result |= (b & 0x1f) << shift
            shift += 5
            if b < 0x20:
                break

        dlng = ~(result >> 1) if result & 1 else result >> 1
        lng += dlng

        array.append((lat * 1e-5, lng * 1e-5))
    return array

if __name__ == "__main__":
    latlngs = decode_line("grkyHhpc@B[[_IYiLiEgj@a@q@yEoAGi@bEyH_@aHj@m@^qAB{@IkHi@cHcAkPSiMJqEj@s@CkFp@sDfB}Ex@iBj@S_AyIkCcUWgAaA_JUyAFk@{D_]~KiLwAeCsHqJmBlAmFuXe@{DcByIZIYiBxBwAc@eCcAl@y@aEdCcBVJpHsEyAeE")
    for latlng in latlngs:
        print str(latlng[0]) + "," + str(latlng[1])
