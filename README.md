# broadlink_rm_pro
Python script utilizing Broadlink RM Pro device to learn/emit IR/RF frequencies (for controlling TV, fan, etc.)

---

## Setup

```
pip3 install broadlink
```

## Usage

```
usage: tv.py [-h] [-l KEYWORD] [-f] [-s KEYWORD] [-c CONFIG_FILE] [-d]

optional arguments:
  -h, --help            show this help message and exit
  -l KEYWORD, --learn KEYWORD
                        learn new frequency
  -f, --force           force overwrite learning frequency keyword
  -s KEYWORD, --send KEYWORD
                        send frequency
  -c CONFIG_FILE, --config CONFIG_FILE
                        specify config file
  -d, --display         display available keywords
```
