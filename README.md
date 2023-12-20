# Medusa - DoS Attack Script to bypass Cloudflare

This Python script is designed for conducting a Distributed Denial of Service (DDoS) attack. It utilizes Selenium with undetected_chromedriver to open multiple browser instances and tabs, flooding a target website with requests.

> **Note:** You may need to have access to multiple devices on different networks to effectively conduct a DDoS attack using Medusa. (**_Educational purposes only!_**)

## Usage

### Prerequisites

- Python
- Chrome browser
- undetected_chromedriver
- termcolor
- selenium

### Installation

First of all, make sure you have Python installed on your system. If not, you can download it from [here](https://www.python.org/downloads/).

Next, you'll need [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json), visit this link to download version 114.x.x.x for your device.

Unzip the file in this directory (where Medusa is located).

Move `ALL FILES` to the root directory, the same directory where `install.sh` is located.

After that, simply run the following command in your terminal:

```bash
chmod +x install.sh && ./install.sh
```
