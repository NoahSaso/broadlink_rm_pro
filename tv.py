#!/usr/bin/env python3

import broadlink
import json
import argparse
import threading
import base64
import os

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--learn', help='learn new frequency', metavar='KEYWORD')
parser.add_argument('-f', '--force', help='force overwrite learning frequency keyword', action='store_true')
parser.add_argument('-s', '--send', help='send frequency', metavar='KEYWORD')
parser.add_argument('-c', '--config', help='specify config file', default='tv_remote.json', metavar='CONFIG_FILE')
parser.add_argument('-d', '--display', help='display available keywords', action='store_true')
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
def learn(d):
  global learned_frequency
  d.enter_learning()
  print('Waiting for frequency...')
  while not learned_frequency:
    learned_frequency = d.check_data()

if args.learn:
  if args.learn in data and not args.force:
    print("Not overwriting learned frequency with keyword '{0}', use -f (--force) to overwrite.".format(args.learn))
    exit(1)

  thread = threading.Thread(target=learn, args=(device,))
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
  if not args.send in data:
    print("Keyword '{0}' not found in config file.".format(args.send))
    exit(1)

  try:
    decoded = base64.decodebytes(data[args.send].encode('ascii'))
  except:
    print("Could not decode data for keyword '{0}'.".format(args.send))
    exit(1)

  device.send_data(decoded)

elif args.display:
  print(','.join(data.keys()))
