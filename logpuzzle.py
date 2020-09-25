#!/usr/bin/env python2
"""
Log Puzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Given an Apache logfile, find the puzzle URLs and download the images.

Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

import os
import re
import sys
import urllib.request
import argparse

__author__ = "Jasmyne Ford with help from John and Micheal Trainer"

def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """
    urls = []
    path = "http://" + "".join(filename.replace("animal_", ""))
    print(path)
    with open(filename, "r") as f:
        for line in f:
            matches=re.findall(r'GET (\S+) HTTP', line)
            for match in matches:
                if match not in urls and 'puzzle' in match:
                    urls.append(match)
    urls.sort(key= lambda x:x[-9:-4])
    # print(urls)                
    urls = list(map(lambda tag:path + tag, urls))
    print(urls)
    return urls
        
def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """
    results = []
    if not (os.path.isdir(dest_dir)):
        os.makedirs(dest_dir)

    for i, each in enumerate(img_urls):
        img_name="img" + str(i) + '.jpeg'
        img_link=os.path.join(dest_dir, img_name)
        print("Retrieving" + img_name + "...")
        urllib.request.urlretrieve(each, img_link)
        results.append(img_name)
    index=open(os.path.join(dest_dir, 'index.html'), 'w+')
    index.write('<html>\n<body>\n')
    for url in results:
        index.write(f'<img src={url}>')
    index.write("\n</body>\n<html>")
    index.close()

def create_parser():
    """Creates an argument parser object."""
    parser=argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')
    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
