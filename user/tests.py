from django.test import TestCase

# Create your tests here.


import requests

resp = requests.post(url='http://127.0.0.1:8798/register', data=dict(name='temp',
                                                                password='Yhsjhsn123', email='abc@qq.com',
                                                                csrf='PDg0cJFy9tCn0HDYBy7X8AcVVjICxVBkwRw30iCL3HwvUWWwpytNibXLvsxGPFeB'),
                                                                # csrftoken='PDg0cJFy9tCn0HDYBy7X8AcVVjICxVBkwRw30iCL3HwvUWWwpytNibXLvsxGPFeB'),
              headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
                       'Cookie': '_xsrf=2|661b2606|1611b8d2200ef7c2ee286b3988e3fdcb|1586415231; username-localhost-8888="2|1:0|10:1586422347|23:username-localhost-8888|44:NmQ3NDE5MzRmYWU3NGNiN2FlMTY3NTgxZmJhNDJhZTI=|8831c31e06624e1461e2650a0291390e135632a531ef0a58337c04dfe0357d4a"; csrftoken=PDg0cJFy9tCn0HDYBy7X8AcVVjICxVBkwRw30iCL3HwvUWWwpytNibXLvsxGPFeB'})


print(resp.text)