# broadlink_rm_pro
Python script utilizing Broadlink RM Pro device to learn/emit IR/RF frequencies (for controlling TV, fan, etc.)

## Interactive Control Mode
Once the script has recorded various frequencies, you can use interactive control mode so that you can effectively use the command line as a remote.
```
Interactive control mode. Press enter to send the entered keyword. Press Ctrl-D to exit.
Use `$learn <keyword>` to learn a new command. Use `$display` to display existing commands.
>> power
>> r
>> r
>> enter
>> play
>> paxse
Keyword 'paxse' not found in config file.
>> pause
>> $learn new_keyword
Waiting for frequency...
Frequency saved to keyword 'new_keyword'.
>> $learn new_keyword
Keyword 'new_keyword' already taken. Would you like to overwrite? [y/n]: n
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
usage: control_rm.py [-h] [-l KEYWORD] [-s KEYWORD] [-c CONFIG_FILE] [-d]
                     [-p PREFIX]

CLI to learn/send IR/RF frequencies from a Broadlink RM Pro device. Run with
no arguments (except -c/--config and -p/--prefix) to enter the interactive
control mode.

optional arguments:
  -h, --help            show this help message and exit
  -l KEYWORD, --learn KEYWORD
                        learn new frequency
  -s KEYWORD, --send KEYWORD
                        send frequency
  -c CONFIG_FILE, --config CONFIG_FILE
                        specify config file
  -d, --display         display available keywords
  -p PREFIX, --prefix PREFIX
                        prefix for interactive control mode input
```
