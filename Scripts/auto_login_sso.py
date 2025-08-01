#!/bin/python3
import requests
import subprocess
import time
import logging
import traceback
from subprocess import call
from systemd.journal import JournalHandler


# Configure logging with loglevel
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(message)s",
    handlers=[JournalHandler()],
)


def check_connectivity():
    logging.debug("Running check_connectivity")
    try:
        response = requests.get("https://www.google.com/generate_204", timeout=2)
        logging.debug(f"Server responded with status code: {response.status_code}")
        return response.status_code == 204  # True if connected, False if behind portal
    except requests.RequestException:
        logging.info("Failed to connect to google")
        return False  # Network error or no connection


def check_network_name():
    logging.debug("Running check_network_name")
    logging.debug("Checking for connection")

    try:
        result = subprocess.run(
            ["nmcli", "-g", "GENERAL.CONNECTION", "device", "show", "wlp2s0"],
            capture_output=True,
            text=True,
            check=True,
            timeout=5,
        )

        text = result.stdout.strip()
        if text:
            logging.debug(f"Got result: {text}")
            return text
        logging.debug("Got no result")

    except Exception:
        logging.warning("Failed to check for network name")
        logging.warning(traceback.format_exc())

    return None


if __name__ == "__main__":
    first_time = True
    fail_count = 0

    while True:
        if not first_time:
            logging.debug("Sleeping...")
            time.sleep(5)
        first_time = False

        if fail_count >= 5:
            logging.error(
                "Failed to login a fifth time, is password correct? Shutting off."
            )
            call(
                "notify-send Failed to login a fifth time, is password correct? Shutting off.",
                shell=True,
            )

        if check_network_name() != "HotSpot - UI":
            logging.debug("Not connected to HotSpot - UI, skipping")
            continue
        if check_connectivity():
            logging.debug("Already connected, skipping")
            continue

        logging.info("Trying to log in")

        try:
            result = subprocess.run(
                [
                    "login_sso.py",
                    "-sp",
                    "pleasestoploggingmeoutfromthewifi",
                ],
                capture_output=True,
            )

            if result.returncode == 0:
                logging.info("Logged in successfully")
                logging.debug(f"Stdout: {result.stdout}")
                logging.debug(f"Stderr: {result.stderr}")
                fail_count = 0
            else:
                logging.warn("Program exited with exit code: " + str(result.returncode))
                logging.debug(f"Stdout: {result.stdout}")
                logging.debug(f"Stderr: {result.stderr}")
                fail_count += 1
        except:
            logging.error("Failed to log in")
            logging.error(traceback.format_exc())
            fail_count += 1
