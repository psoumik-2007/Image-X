import requests
from bs4 import BeautifulSoup
import urllib.parse
import random
import string
import magic
import os
import json
from src.postimages.headers import PostImagesHeader
from src.postimages.routes import PostImageRoute


class PostImages:
    def __init__(self, email: str, password: str, cookies: str = None) -> None:
        self.email = email
        self.password = password
        self.cookies = cookies
        self.working_gallery = False

    def _form_data(self, data_dict: dict) -> str:
        data = ""
        data_keys = data_dict.keys()
        length = len(data_keys)
        for index, item in enumerate(data_keys):
            data += f"{item}={urllib.parse.quote(data_dict[item])}"
            if not index == length - 1:
                data += '&'
        return data

    def _get_csrf(self) -> str:
        login_page_response = requests.get(PostImageRoute.login_page, headers=PostImagesHeader.login_page)
        soup = BeautifulSoup(login_page_response.text, "lxml")
        self.csrf = soup.find('input', {'name': 'csrf_hash'}).get('value')
        return self.csrf

    def is_loged_in(self):
        if self.session_key:
            return True
        return False

    def login(self) -> dict:
        self._get_csrf()
        data = self._form_data({
            'csrf_hash': self.csrf,
            'email': self.email,
            'password': self.password,
        })

        login_post_response = requests.post(PostImageRoute.login_page, headers=PostImagesHeader.login_post, data=data, allow_redirects=False)
        self.cookies = login_post_response.cookies.get_dict()
        valid_token_response = requests.get(login_post_response.headers["Location"], cookies=self.cookies, headers=PostImagesHeader.token_validator, allow_redirects=False)
        self.cookies = valid_token_response.cookies.get_dict()
        return self.cookies

    def get_galleries(self):
        pass

    def set_working_gallery(self, gallery_name: str):
        pass

    def upload_image(self, image_path: str):
        pass
