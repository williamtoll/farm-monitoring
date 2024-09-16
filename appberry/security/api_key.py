import os
api_keys = {
    '6c05f016-6ca2-466b-8fac-778e2fae7ad8',
    os.getenv("API_KEY")
}

def check_api_key(api_key: str):
    return api_key in api_keys

