import time

import requests

RETRYING_ATTEMPS = 3
def getHTTPJsonResponse(url, retryingAttemps=RETRYING_ATTEMPS):
    response = requests.get(url)
    status_code = response.status_code
    if status_code == 200:
        return response.json()
    if status_code == 404:
        return None

    print(f'got {status_code} status Code, retrying attemps = {retryingAttemps}')
    if retryingAttemps < 1:
        raise TimeoutError(f'Tried to retry the request to avoid {status_code} but failed')
    print(f'sleeping for {RETRYING_ATTEMPS - retryingAttemps + 1} seconds then will retry')
    time.sleep(RETRYING_ATTEMPS - retryingAttemps + 1)
    return getHTTPJsonResponse(url, retryingAttemps - 1)