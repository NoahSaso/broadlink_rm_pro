#!/usr/bin/env python3

import broadlink
import json
import argparse
import threading
import base64
import os
import sys
import threading

parser = argparse.ArgumentParser(description='CLI to learn/send IR/RF frequencies from a Broadlink RM Pro device. Run with no arguments (except -c/--config, -p/--prefix, and -a/--auto) to enter the interactive control mode.')
parser.add_argument('-l', '--learn', help='learn new frequency', metavar='KEYWORD')
parser.add_argument('-s', '--send', help='send frequency', metavar='KEYWORD')
parser.add_argument('-c', '--config', help='specify config file', default='tv_remote.json', metavar='CONFIG_FILE')
parser.add_argument('-d', '--display', help='display available keywords', action='store_true')
parser.add_argument('-p', '--prefix', help='prefix for interactive control mode input', default='>>')
parser.add_argument('-a', '--auto', help='enter interactive auto mode which presses enter after each keypress', action='store_true')
args = parser.parse_args()

if not os.path.exists(args.config):
  with open(args.config, 'w'): pass # create file

data = {}
with open(args.config, 'r') as f:
  try:
    data = json.load(f)
  except:
    pass # if fails, just continue because file might be empty

if not args.display:
  print('Connecting to device...')
  device = broadlink.discover(local_ip_address='0.0.0.0')
  if not device:
    print('Could not find device')
    exit(1)

  device.auth()
  print('Connected.')

done = False

learned_frequency = False
def learn():
  global learned_frequency

  device.enter_learning()
  print('Waiting for frequency...')
  while not learned_frequency and not done:
    learned_frequency = device.check_data()

def start_learn(keyword):
  global data
  global learned_frequency
  global done

  if keyword in data:
    force = input("Keyword '{0}' already taken. Would you like to overwrite? [y/n]: ".format(keyword))
    if force.lower() != 'y':
      return

  thread = threading.Thread(target=learn)
  thread.start()

  try:
    thread.join()
  except KeyboardInterrupt: pass

  if not learned_frequency:
    print('\nCancelled.')
    done = True
    return

  try:
    encoded = base64.encodebytes(learned_frequency).decode('ascii')
    learned_frequency = False
  except:
    print("Could not encode data for keyword '{0}'.".format(keyword))
    done = True
    return

  data[keyword] = encoded

  with open(args.config, 'w') as f:
    json.dump(data, f)

  print("Frequency saved to keyword '{0}'.".format(keyword))

def send(keyword):
  if not keyword in data:
    print("Keyword '{0}' not found in config file.".format(keyword))
    return

  try:
    decoded = base64.decodebytes(data[keyword].encode('ascii'))
  except:
    print("Could not decode data for keyword '{0}'.".format(keyword))
    return

  # Send data in another thread so we don't block the console interface
  t = threading.Thread(target=device.send_data, args=(decoded,))
  t.start()
  # device.send_data(decoded)

def display():
  print(', '.join(data.keys()))

prev_input = False

# https://stackoverflow.com/a/28143542
def getch():
  import termios
  import tty
  def _getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
      tty.setraw(fd)
      ch = sys.stdin.read(1)
    finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
  return _getch()

def control_mode():
  global args
  global prev_input

  if args.auto:
    input_args = getch()
    # ESC
    if ord(input_args) == 27:
      raise KeyboardInterrupt
    # Return, rerun last input, empty
    elif ord(input_args) == 13:
      input_args = ""
    else:
      sys.stdout.write(input_args)
      sys.stdout.flush()
      print()
  else:
    input_args = input('{0} '.format(args.prefix))

  if not len(input_args) and prev_input:
    input_args = prev_input
    print("Rerunning input '{0}'".format(input_args))
  else:
    prev_input = input_args

  split_input_args = input_args.split(' ')
  if not args.auto and len(split_input_args) and split_input_args[0].startswith('$'):
    cmd = split_input_args[0][1:].lower()
    if cmd == 'learn':
      start_learn(split_input_args[1])
    elif cmd == 'display':
      display()
    else:
      send(input_args)
  else:
    send(input_args)

  control_mode()

# RUN

if args.learn:
  start_learn(args.learn)

elif args.send:
  send(args.send)
  print('Sent.')

elif args.display:
  display()

else:
  if args.auto:
    print('Auto interactive control mode. The first letter typed will be sent. Pressing enter will repeat the previous input.')
    print('Press ESC to exit.')
  else:
    print('Interactive control mode. Press enter to send the entered keyword. Press enter with an empty input to repeat the previous input.')
    print('Use `$learn <keyword>` to learn a new command. Use `$display` to display existing commands.')
    print('Press Ctrl-D to exit.')

  try:
    control_mode()
  except (EOFError, KeyboardInterrupt):
    done = True
    print('\nExiting interactive control mode.')
