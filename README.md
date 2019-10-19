# broadlink_rm_pro
Python script utilizing Broadlink RM Pro device to learn/emit IR/RF frequencies (for controlling TV, fan, etc.)

## Interactive Control Mode
Once the script has recorded various frequencies, you can use interactive control mode so that you can effectively use the command line as a remote.
```
Interactive control mode. Press enter to send the entered keyword. Press Ctrl-D to exit.
>> power
>> r
>> r
>> enter
>> play
>> paxse
Keyword 'paxse' not found in config file.
>> pause
>> ^D
Exiting control mode.
```

---

## Setup

```
pip3 install broadlink
```

## Usage

```
usage: control_rm.py [-h] [-l KEYWORD] [-f] [-s KEYWORD] [-c CONFIG_FILE] [-d]

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
