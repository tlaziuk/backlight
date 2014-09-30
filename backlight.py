#! /usr/bin/env python3
import argparse
import os
import sys
parser = argparse.ArgumentParser(description="Change brightness of your displays.", prog="backlight")
parser.add_argument("percentage", metavar="N%", help="change brightness to given percentage value", type=int)
group1 = parser.add_mutually_exclusive_group()
group1.add_argument("-d", "--dec", help="decrease value by given percentage value", action="store_true")
group1.add_argument("-i", "--inc", help="increase value by given percentage value", action="store_true")
parser.add_argument("-v", "--verbose", help="enable verbose output", action="store_true")
parser.add_argument("--directory", metavar="DIR", help="change directory of display devices", default="/sys/class/backlight/")
args = parser.parse_args()
operator = str()
path = dict()
max_brightness = dict()
brightness = dict()
if (not os.path.exists(args.directory)):
	print("devices path not found ("+args.directory+")", file=sys.stderr)
	exit(1)
for i in os.listdir(args.directory):
	path[i] = os.path.join(args.directory, i)
	if (args.verbose):
		print("found", i)
if (len(path) <= 0):
	print("there are no display devices in given directory", file=sys.stderr)
	exit(2)
for i in path.keys():
	f = open(os.path.join(path[i], "max_brightness"), "r")
	max_brightness[i] = int(f.readline()[:-1])
	f.close()
	f = open(os.path.join(path[i], "brightness"), "r")
	brightness[i] = int(f.readline()[:-1])
	f.close()
	if (args.verbose):
		print(i, brightness[i]/max_brightness[i]*100)
for i in path.keys():
	value = brightness[i]
	if (args.inc):
		value = brightness[i]+(max_brightness[i]/100*args.percentage)
	elif (args.dec):
		value = brightness[i]-(max_brightness[i]/100*args.percentage)
	else:
		value = max_brightness[i]/100*args.percentage
	if (value > max_brightness[i]):
		value = max_brightness[i]
	elif (value < 0):
		value = 0
	else:
		value = int(value)
	f = open(os.path.join(path[i], "brightness"), "w")
	f.write(str(value)+"\n")
	f.close()
	if (args.verbose):
		print(i, value)
exit(0)
