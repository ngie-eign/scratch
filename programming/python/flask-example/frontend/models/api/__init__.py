import inspect


VALID_API_VERSIONS = (1,)


def valid_api_version(version):
    return version in VALID_API_VERSIONS
