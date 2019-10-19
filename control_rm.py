#!/usr/bin/env python3

import broadlink
import json
import argparse
import threading
import base64
import os

parser = argparse.ArgumentParser(description='CLI to learn/send IR/RF frequencies from a Broadlink RM Pro device. Run with no arguments (except -c/--config and -p/--prefix) to enter the interactive control mode.')
parser.add_argument('-l', '--learn', help='learn new frequency', metavar='KEYWORD')
parser.add_argument('-f', '--force', help='force overwrite learning frequency keyword', action='store_true')
parser.add_argument('-s', '--send', help='send frequency', metavar='KEYWORD')
parser.add_argument('-c', '--config', help='specify config file', default='tv_remote.json', metavar='CONFIG_FILE')
parser.add_argument('-d', '--display', help='display available keywords', action='store_true')
parser.add_argument('-p', '--prefix', help='prefix for interactive control mode input', default='>>')
args = parser.parse_args()

if not os.path.exists(args.config):
  with open(args.config, 'w'): pass # create file

data = {}
with open(args.config, 'r') as f:
  try:
    data = json.load(f)
  except:
    pass # if fails, just continue because file might be empty

device = broadlink.discover(local_ip_address='0.0.0.0')
if not device:
  print('Could not find device')
  exit(1)

device.auth()

learned_frequency = False
def learn():
  global learned_frequency
  device.enter_learning()
  print('Waiting for frequency...')
  while not learned_frequency:
    learned_frequency = device.check_data()

def send(keyword):
  if not keyword in data:
    print("Keyword '{0}' not found in config file.".format(keyword))
    return

  try:
    decoded = base64.decodebytes(data[keyword].encode('ascii'))
  except:
    print("Could not decode data for keyword '{0}'.".format(keyword))
    return

  device.send_data(decoded)

def control_mode():
    keyword = input('{0} '.format(args.prefix))
    send(keyword)
    control_mode()

if args.learn:
  if args.learn in data and not args.force:
    print("Not overwriting learned frequency with keyword '{0}', use -f (--force) to overwrite.".format(args.learn))
    exit(1)

  thread = threading.Thread(target=learn)
  thread.start()
  thread.join()

  try:
    encoded = base64.encodebytes(learned_frequency).decode('ascii')
  except:
    print("Could not encode data for keyword '{0}'.".format(args.learn))
    exit(1)

  data[args.learn] = encoded

  with open(args.config, 'w') as f:
    data = json.dump(data, f)

  print("Frequency saved to keyword '{0}'.".format(args.learn))

elif args.send:
  send(args.send)

elif args.display:
  print(', '.join(data.keys()))

else:
  print('Interactive control mode. Press enter to send the entered keyword. Press Ctrl-D to exit.')

  try:
    control_mode()
  except EOFError:
    print('\nExiting control mode.')
