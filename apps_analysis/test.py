import requests

headers = {
    'X-CleverTap-Account-Id': '675-RK6-RR6Z',
    'X-CleverTap-Passcode': 'f387422e-f5ff-4fef-9dcf-7cba34e67c27',
    'Content-Type': 'application/json',
}

response = requests.get('https://api.clevertap.com/1/events.json?cursor=CURSOR', headers=headers)
print(response.json())