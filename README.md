# Stocks: Future to Future Trading

Assists in trading of Futures. Mails the user whenever some Future of some stock (scrip) seems profitable to purchase. 
# Prerequisites

> python3.7 or higher
<br>

> pip3

## Installation

* Linux
<br>

> If you don't have Mozilla firefox
```bash
sudo apt install firefox
```

> Create virtual environment

```bash
$ source build.sh
```
> Enter virtual environment
```bash
$ source env/bin/activate
```
> Rename _env.text to .env after filling email & password of your email bot (gmail account necessary) and the your account
<br>

> Run the code
```bash
python3 stox_ftf
```
* Windows

Due to some features not being supported by windows, you would require WSL2

1. Install WSL2
2. Follow [Firefox-Setup](https://blog.henrypoon.com/blog/2020/09/27/running-selenium-webdriver-on-wsl2/) to make firefox work in WSL2
3. Follow the steps required in installation for Linux