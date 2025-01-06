def safe_find(element, method, *args, **kwargs):
    try:
        return getattr(element, method)(*args, **kwargs)
    except AttributeError:
        return None

