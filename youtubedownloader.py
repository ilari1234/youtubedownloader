"""***** YouTube video downloader *****"""

from pytube import YouTube
from pytube.cli import on_progress
from pytube import exceptions
import argparse
import click
import validators
from urllib.parse import urlparse
import sys


def download_video(yt):
    stream = yt.streams.get_highest_resolution()
    print(f"Title: {yt.title}")
    print(f"Author: {yt.author}")
    print(f"Video size is {stream.filesize_mb} mb.")
    if click.confirm("Continue?"):
        stream.download()
        print("\n")
        print("Video downloaded!")

def url_validator(url):
    if validators.url(url):
        result = urlparse(url)
        if result.scheme != 'https':
            print("Invalid protocol. Use https instead. Exiting...")
            sys.exit()
        if result.hostname != "www.youtube.com":
            print("Only YouTube is allowed. Exiting...")
            sys.exit()
        if result.path != "/watch":
            print("Not a video url. Exiting...")
            sys.exit()
    else:
        print(f"Invalid url: {url}. Exiting...")
        sys.exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("link", help="Link to the video")
    args = parser.parse_args()

    url_validator(args.link)

    try:
        yt = YouTube(args.link, on_progress_callback=on_progress)     
    except exceptions.AgeRestrictedError as e:
        print(e)
    except exceptions.VideoUnavailable as e:
        print(e)
    except exceptions.PytubeError as e:
        print(e)
    except Exception as e:
        print(e)
    else:
        download_video(yt)
