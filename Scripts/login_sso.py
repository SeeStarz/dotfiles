#!/bin/python3
"""
Revision Log:
- XX/XX/XX - Many unlogged revisions
- 23/11/24 - Fixed CLI main program
"""

import os
import re
import getpass
from argparse import ArgumentParser
from typing import Literal

import requests
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.exceptions import InvalidKey, InvalidTag


CREDENTIALS_FILE = os.path.join(os.path.expanduser("~"), ".ssologin")
LOGIN_FORM_URL = "http://gw-hotspot.ui.ac.id"
REDIRECTED_URL = "https://sso.ui.ac.id"


class REGEX:
    ACTION_URL = re.compile(r'<form.*?action="(?P<action_url>.*?)".*?>', re.DOTALL)
    LT_VALUE = re.compile(
        r'<input.*?name="lt" value="(?P<lt_value>.*?)".*?>', re.DOTALL
    )
    EXECUTION = re.compile(
        r'<input.*?name="execution" value="(?P<execution_value>.*?)".*?>', re.DOTALL
    )
    _EVENT_ID = re.compile(
        r'<input.*?name="_eventId" value="(?P<eventId_value>.*?)".*?>', re.DOTALL
    )
    SUCCESSFUL_AUTH = re.compile(r"Otorisasi berhasil!", re.DOTALL)


class Credentials:
    @classmethod
    def derive_key(cls, password: str, salt: bytes) -> bytes:
        """Derives a 32-byte key from the password and salt using Scrypt."""
        kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1, backend=default_backend())
        return kdf.derive(password.encode())

    @classmethod
    def load(cls, filename, key):
        with open(filename, "rb") as f:
            salt = f.read(16)
            iv = f.read(12)  # Read the IV
            tag = f.read(16)  # Read the tag
            ciphertext = f.read()  # Read the ciphertext

        derived_key = cls.derive_key(key, salt)

        decryptor = Cipher(
            algorithms.AES(derived_key),
            modes.GCM(iv, tag),  # Provide the tag
            backend=default_backend(),
        ).decryptor()
        decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
        return decrypted_data.decode().split(";")

    @classmethod
    def dump(cls, filename, key, username, password):
        salt = os.urandom(16)

        # Derive a 32-byte encryption key from the password
        derived_key = cls.derive_key(key, salt)

        iv = os.urandom(12)
        # Encrypt and save credentials
        cipher = Cipher(
            algorithms.AES(derived_key),
            modes.GCM(iv),  # generate a new IV for each encryption
            backend=default_backend(),
        )
        encryptor = cipher.encryptor()
        encoded_str = (username + ";" + password).encode()
        ciphertext = encryptor.update(encoded_str) + encryptor.finalize()
        tag = encryptor.tag  # Capture the authentication tag

        with open(filename, "wb") as f:
            f.write(salt)
            f.write(iv)  # Save IV
            f.write(tag)  # Save tag
            f.write(ciphertext)  # Save ciphertext


class Authenticator:
    def __init__(self):
        self.session = requests.Session()
        self.debug_files: dict[str, bytes] = {}
        self.action_url_path = ""
        self.login_data = {}
        self.logged_in = False

    def prompt_password(
        self, prompt, confirm_prompt="", wrong_password_msg="", once=False
    ):
        if once:
            return getpass.getpass(prompt)
        pwd = None
        while pwd is None:
            tmp = getpass.getpass(prompt)
            if tmp == getpass.getpass(confirm_prompt):
                pwd = tmp
                break
            print(wrong_password_msg)
        return pwd

    def prompt_subtitute_password_interactive(self):
        print("Fetching credentials...")
        key = self.prompt_password(
            "Enter your substitute password (enter '~' to reset password): ", once=True
        )
        if key == "~":
            print("Deleting existing credentials....")
            os.remove(CREDENTIALS_FILE)
            return None
        return key

    def prompt_setup(self):
        username = input("Enter your SSO Username: ")
        password = self.prompt_password(
            "Enter your SSO Password: ",
            "Reenter password: ",
            "The passwords are inconsistent. Please try again",
        )
        key = self.prompt_password(
            "Enter a substitute password for login: ",
            "Reenter substitute password: ",
            "The passwords are different.",
        )
        return dict(username=username, password=password, key=key)

    def setup_creds(self, interactive=False, data=None):
        if interactive:
            print("Starting setup [Interactive]...")
            Credentials.dump(filename=CREDENTIALS_FILE, **self.prompt_setup())
        else:
            print("Starting setup [Non interactive]...")
            Credentials.dump(
                filename=CREDENTIALS_FILE,
                key=data["key"],
                username=data["username"],
                password=data["password"],
            )
        print(
            "Successfully saved your credentials! (Saved at {})".format(
                CREDENTIALS_FILE
            )
        )

    def fetch_login_form(self):
        print("Loading login form and scraping data...")

        login_form_resp = self.session.get(LOGIN_FORM_URL, timeout=5)

        self.debug_files["login_form_page"] = login_form_resp.content
        self.action_url_path = REGEX.ACTION_URL.search(login_form_resp.text).groups()[0]
        self.login_data.update(
            {
                "lt": REGEX.LT_VALUE.search(login_form_resp.text).groups()[0],
                "execution": REGEX.EXECUTION.search(login_form_resp.text).groups()[0],
                "_eventId": REGEX._EVENT_ID.search(login_form_resp.text).groups()[0],
            }
        )

    def attempt_login(self):
        print("Logging you in...")
        login_resp = self.session.post(
            REDIRECTED_URL + self.action_url_path, data=self.login_data, timeout=5
        )
        successful_login = len(REGEX.SUCCESSFUL_AUTH.findall(login_resp.text)) > 0
        if login_resp.ok and successful_login:
            print("Successfully logged you in!")
            self.logged_in = True
            return
        print("Failed to log you in...")
        exit(1)

    def write_debugging_files(self):
        print("Writing fetched files for debugging...")
        for entry_name, content in self.debug_files:
            with open(entry_name + ".html", "wb") as f:
                f.write(content)

    def main_interactive(self):
        while not self.logged_in:
            try:
                if not os.path.exists(CREDENTIALS_FILE):
                    print("Credentials not found, running setup...")
                    self.setup_creds(interactive=True)
                key = self.prompt_subtitute_password_interactive()
                if key is None:
                    continue
                credentials = Credentials.load(filename=CREDENTIALS_FILE, key=key)
                self.login_data.update(
                    {"username": credentials[0], "password": credentials[1]}
                )
                self.fetch_login_form()
                self.attempt_login()
            except (InvalidKey, InvalidTag):
                print("Invalid password!")
            except Exception as e:
                print(f"Error: {type(e)} {e}")

            if self.logged_in:
                continue
            retry = input("Would you like to try again (Y/n)? ")
            credentials = None
            if retry.lower()[:1] != "n":
                continue
            return

    def main_cli(
        self,
        args: dict[
            Literal["username", "password", "sub_password", "run_setup"],
            str | bool | None,
        ],
    ):
        if args["run_setup"]:
            args.update({"key": args["sub_password"]})
            try:
                self.setup_creds(interactive=False, data=args)
            except Exception:
                print("Failed to parse credentials from arguments.")
                exit(1)
            return

        if not args["sub_password"] and not (args["username"] and args["password"]):
            print(
                "Invalid CLI operation.\nTo run setup, pass --setup and optionally, credentials to command line\nTo login without saving your credentials, pass --username and --password\nTo login using saved credentials, pass --subtitute-password\n"
            )
            exit(1)

        try:
            credentials = [args["username"], args["password"]]
            if args["sub_password"]:
                if not os.path.exists(CREDENTIALS_FILE):
                    print("Credentials not found")
                    exit(1)
                credentials = Credentials.load(
                    filename=CREDENTIALS_FILE, key=args["sub_password"]
                )
            self.login_data.update(
                {"username": credentials[0], "password": credentials[1]}
            )
            self.fetch_login_form()
            self.attempt_login()
        except (InvalidKey, InvalidTag):
            print("Invalid password!")
            exit(1)
        except Exception as e:
            print(f"Error: {type(e)} {e}")
            exit(1)

    def run(self):
        parser = ArgumentParser(
            usage="Pass -u and -p to automatically login with given sso username and password or pass -sp to automatically login with given subtitute password without CLI interaction, otherwise defaults to cli interaction."
        )
        parser.add_argument(
            "-u",
            "--user",
            "--username",
            dest="username",
            default=None,
            help="Login using given username and password or run setup credentials.",
        )
        parser.add_argument(
            "-p",
            "--pass",
            "--password",
            dest="password",
            default=None,
            help="Login using given username and password or run setup credentials.",
        )
        parser.add_argument(
            "-sp",
            "--subpass",
            "--sub-password",
            "--subtitute-password",
            dest="sub_password",
            default=None,
            help="Login using subtitute password or setup using subtitute password.",
        )
        parser.add_argument(
            "-r",
            "-s",
            "--reset",
            "--setup",
            action="store_true",
            dest="run_setup",
            default=False,
            help="Runs the credentials setup, pass the user, password, and subtitute password through arguments, otherwise it will defaults to the interactive setup.",
        )
        args = parser.parse_args()
        if args.username or args.password or args.sub_password or args.run_setup:
            self.main_cli(dict(args.__dict__))
        else:
            self.main_interactive()


if __name__ == "__main__":
    authenticator = Authenticator()
    authenticator.run()
