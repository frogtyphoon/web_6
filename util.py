def get_object_size(geo_object):
    lower_corner = list(map(float, geo_object['boundedBy']['Envelope']['lowerCorner'].split()))
    upper_corner = list(map(float, geo_object['boundedBy']['Envelope']['upperCorner'].split()))
    return (str(abs(lower_corner[0] - upper_corner[0]) / 2),
            str(abs(lower_corner[1] - upper_corner[1]) / 2))
