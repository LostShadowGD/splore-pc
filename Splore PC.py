import os
import re
import requests
import json
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence
import sys

download_dir = "PICO-8 Roms"  # Change this to your desired directory

newCarts = "https://www.lexaloffle.com/bbs/?cat=7&carts_tab=1#sub=2&mode=carts&orderby=ts"
featuredCarts = "https://www.lexaloffle.com/bbs/?cat=7&carts_tab=1#sub=2&mode=carts&orderby=featured"
randomCarts = "https://www.lexaloffle.com/bbs/?cat=7&carts_tab=1#sub=2&mode=carts&orderby=lucky"

def main():
    print("""
█▀▀ ▄▀▄ █▀█ ▀█▀    █▀▄ ▀█▀ █▀▀ █▀▀ █▀█ █ █ █▀▀ █▀█ ▀▄▀ 
█▄▄ █▀█ █▀▄  █     █▄▀ ▄█▄ ▄██ █▄▄ █▄█ ▀▄▀ ██▄ █▀▄  █  """)
    print("")
    print("--- INSTRUCTIONS ---")
    print("You will be send to the appropriate Carts Page on Lexaloffle.")
    print("""Right click the game's cartridge preview, and click "copy link address".""")
    print("""Enter the copied URL into the "URL" text field, and press Enter.""")
    print("")
    print("[1] New Carts")
    print("[2] Featured Carts")
    print("[3] Lucky Draw")

    pageType = int(input())

    if pageType == 2:
        siteURL = featuredCarts
        windowTitle = "Featured Carts. Copy the cart URL."
    elif pageType == 3:
        siteURL = randomCarts
        windowTitle = "Lucky Draw. Copy the cart URL."
    else:
        siteURL = newCarts
        windowTitle = "New Carts. Copy the cart URL."

    app = QApplication(sys.argv)
    browser = QWebEngineView()
    browser.load(QUrl(siteURL))
    browser.setWindowTitle(windowTitle)

    back_shortcut = QShortcut(QKeySequence("Alt+Left"), browser)
    back_shortcut.activated.connect(browser.back)
    
    browser.setWindowFlag(Qt.WindowStaysOnTopHint, True)
    browser.show()
    browser.raise_()
    browser.activateWindow()
    browser.setFocus()
    app.processEvents()
    browser.show()

    # Single Game

    url = input("URL: ")

    html_doc = requests.get(url)
    soup = BeautifulSoup(html_doc.text, 'html.parser')

    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.endswith('.p8.png'):
            downloadURL = "https://www.lexaloffle.com" + href
            print(f"Found cart: {downloadURL}")
            result = requests.get(downloadURL)
            if result.status_code == 200:
                os.makedirs(download_dir, exist_ok=True)
                filename = os.path.basename(href)
                filepath = os.path.join(download_dir, filename)
                with open(filepath, 'wb') as f:
                    f.write(result.content)
                print(f"Downloaded to {filepath}")
            else:
                print(f"Failed to download: {result.status_code}")
            return
    print("No .p8.png cart found on this page.")


main()