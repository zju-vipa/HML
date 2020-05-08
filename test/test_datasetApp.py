import requests

"""
test
"""


def test_add():
    dataset_info = {
        'dataset_name': '1231',
        'if_public': True,
        "dataset_id": "0546357a51c147fcbd4ba1f7f5816253",
        "tmp_file_path": "../Data/tmp_dataset/0546357a51c147fcbd4ba1f7f5816253.txt"
    }
    headers = {
        'Authorization': "eyJhbGciOiJIUzUxMiIsImlhdCI6MTU4MzY3MDI5MSwiZXhwIjoxNTg0Mjc1MDkxfQ.eyJpZCI6IjhhMDY0Yzk0MTQ2ZTQ0MjdhMTZlYjYzZDNlZjgyMDkzIn0.4-vi_SYImah0pBZP9BFEAsZZelPXihUhVg8WfyRpwNnYE7bF8XncoDWe9rHkvOiaI7MPxeqSB_UaOC7D4NRhmw"
    }

    result = requests.post("http://0.0.0.0:8021/api/private/v1/dataset/add", data=dataset_info, headers=headers)
    print("------start to print-------")
    print(result.text)
    print("------finish to print-------")


def test_query():
    headers = {
        # 'Authorization': '1yJleHAiOjE1ODM5OTUyMDUsImlhdCI6MTU4MzM5MDQwNSwiYWxnIjoiSFM1MTIifQ.eyJpZCI6IjAxYTVjOGQ1YjhkYTQzMWViMjAyNDFlNWZkY2M5MGViIn0.xrGZsMVQlIn7IBYUwVVGlTXodTnn-OMMHGP3PZbN0QqPLOh-WehrcrO5Jp29Y5d4GxKQ-i46XSWQRSu5ek7_JQ'
        'Authorization': "eyJhbGciOiJIUzUxMiIsImlhdCI6MTU4MzM4OTM1OSwiZXhwIjoxNTgzOTk0MTU5fQ.eyJpZCI6ImZkMDBkMjNmMDIzNjQwY2JhNGFjZTJjODJhNzEwYTYxIn0.9r0gis3hVkxhdf1cZ-NqaoENwGreYQHVRGaIQ2NdYCV20A4A6OE-YVyjJjwsgM6Z76qLXPWKRFrO5aFFxnvR5Q"
    }
    result = requests.get("http://10.214.211.205:8021/api/private/v1/dataset/query", headers=headers)
    print("------start to print-------")
    print(result.headers)
    print("------finish to print-------")


def test_download():
    headers = {
        'Authorization': "eyJhbGciOiJIUzUxMiIsImlhdCI6MTU4MzM4OTM1OSwiZXhwIjoxNTgzOTk0MTU5fQ.eyJpZCI6ImZkMDBkMjNmMDIzNjQwY2JhNGFjZTJjODJhNzEwYTYxIn0.9r0gis3hVkxhdf1cZ-NqaoENwGreYQHVRGaIQ2NdYCV20A4A6OE-YVyjJjwsgM6Z76qLXPWKRFrO5aFFxnvR5Q"
    }
    dataset_id = '37786bff768f4f398096d88a01f76084'
    result = requests.get("http://0.0.0.0:8021/api/private/v1/dataset/download?dataset_id=" + dataset_id, headers=headers)
    print("------start to print-------")
    print(result.headers)
    print("------finish to print-------")