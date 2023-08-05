try:
    from pkg_resources import get_distribution
    version = get_distribution("ontosrv").version
    del get_distribution
except:
    version = "unknown"
