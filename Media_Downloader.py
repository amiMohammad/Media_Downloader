#! /usr/bin/env python3

import csv
import shutil
import sys
import time
import os
import logging

# http client configuration
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/63.0.3239.84 Chrome/63.0.3239.84 Safari/537.36'

# logging configuration
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

python_version = sys.version_info.major
logging.info("executed by python %d" % python_version)

# compatability with python 2
if python_version == 3:
    import urllib.parse
    import urllib.request
    urljoin = urllib.parse.urljoin
    urlretrieve = urllib.request.urlretrieve
    quote = urllib.parse.quote

    # configure headers
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', user_agent)]
    urllib.request.install_opener(opener)
else:
    import urlparse
    import urllib
    urljoin = urlparse.urljoin
    urlretrieve = urllib.urlretrieve
    quote = urllib.quote

    # configure headers
    class AppURLopener(urllib.FancyURLopener):
        version = user_agent
    urllib._urlopener = AppURLopener()

def fix_url(url):
    url = quote(url, safe="%/:=&?~#+!$,;'@()*[]")
    return url


def get_file_extension(content_type):
    """
    Maps MIME types to file extensions.
    Supports images, audio, and video formats.
    """
    mime_to_ext = {
        # Image formats
        'image/jpeg': 'jpg',
        'image/jpg': 'jpg',
        'image/png': 'png',
        'image/gif': 'gif',
        'image/webp': 'webp',
        
        # Audio formats
        'audio/mpeg': 'mp3',
        'audio/mp3': 'mp3',
        'audio/mp4': 'm4a',
        'audio/x-m4a': 'm4a',
        'audio/x-wav': 'wav',
        'audio/wav': 'wav',
        'audio/midi': 'midi',
        'audio/x-midi': 'midi',
        
        # Video formats
        'video/mp4': 'mp4',
        'video/x-msvideo': 'avi',
        'video/avi': 'avi',
        'video/x-matroska': 'mkv',
        'video/quicktime': 'mkv',
        'video/mp2t': 'ts',
        'video/x-mpts': 'ts',
    }
    
    return mime_to_ext.get(content_type, None)


def download_csv_row_images(row, dest_dir):
    for key in row:
        start_url = row.get('web-scraper-start-url', '')
        id = row.get('web-scraper-order', '')

        if key.endswith("-src"):
            file_url = row[key]
            file_url = urljoin(start_url, file_url)

            original_filename = os.path.basename(file_url)
            file_filename = os.path.splitext(original_filename)[0]
            download_file(file_url, dest_dir, file_filename)


def download_file(file_url, dest_dir, file_filename):
    """
    Downloads media files (images, audio, and video).
    Supports jpg, jpeg, png, webp, gif, mp3, m4a, midi, wav, mp4, mkv, avi, ts.
    """
    file_url = fix_url(file_url)

    try:
        logging.info("downloading file %s" % file_url)
        tmp_file_name, headers = urlretrieve(file_url)
        content_type = headers.get("Content-Type")

        # Get extension based on content type
        ext = get_file_extension(content_type)
        
        if ext is None:
            logging.warning("unknown file content type %s" % content_type)
            return

        file_path = os.path.join(dest_dir, file_filename + "." + ext)
        shutil.move(tmp_file_name, file_path)
        logging.info("successfully downloaded %s" % file_path)
        
    except Exception as e:
        logging.warning("File download error. %s" % e)


# Keep the old function name for backward compatibility
def download_image(image_url, dest_dir, image_filename):
    download_file(image_url, dest_dir, image_filename)


def get_csv_image_dir(csv_filename):

    base = os.path.basename(csv_filename)
    dir = os.path.splitext(base)[0]

    if not os.path.exists(dir):
        os.makedirs(dir)

    return dir

def download_csv_file_images(filename):

    logging.info("importing data from %s" % filename)

    dest_dir = get_csv_image_dir(filename)

    #check whether csv file has utf-8 bom char at the beginning
    skip_utf8_seek = 0
    with open(filename, "rb") as csvfile:
        csv_start = csvfile.read(3)
        if csv_start == b'\xef\xbb\xbf':
            skip_utf8_seek = 3


    with open(filename, "r", encoding="utf8", newline="") as csvfile:

        # remove ut-8 bon sig
        csvfile.seek(skip_utf8_seek)

        csvreader = csv.DictReader(csvfile)
        fieldnames = csvreader.fieldnames or []

        if fieldnames and (
            'web-scraper-start-url' in fieldnames or any(key.endswith('-src') for key in fieldnames)
        ):
            rows = csvreader
        else:
            csvfile.seek(skip_utf8_seek)
            rows = []
            for index, line in enumerate(csvfile, start=1):
                url = line.strip()
                if not url:
                    continue
                rows.append({
                    'web-scraper-start-url': url,
                    'web-scraper-order': str(index).zfill(4),
                    'image-src': url,
                })

        for row in rows:
            download_csv_row_images(row, dest_dir)

def main(args):
    csv_filename = None

    # Accept full Windows paths such as C:\Windows\python.exe and file paths
    # passed via drag-and-drop or a command line invocation.
    for arg in args[1:]:
        if os.path.isfile(arg) and arg.lower().endswith('.csv'):
            csv_filename = arg
            break

    if csv_filename:
        download_csv_file_images(csv_filename)
        logging.info("media download completed")
    else:
        logging.warning("no valid input file found")

    time.sleep(10)


if __name__ == "__main__":
    main(sys.argv)
