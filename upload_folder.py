import os
import argparse
from pathlib import Path
import upload
import imghdr


def parse_args(arg_input=None):
    parser = argparse.ArgumentParser(description='Upload photos to Google Photos.')
    parser.add_argument('--auth ', metavar='auth_file', dest='auth_file',
                    help='file for reading/storing user authentication tokens')
    parser.add_argument('--log', metavar='log_file', dest='log_file',
                    help='name of output file for log messages')
    parser.add_argument('photo_folder', metavar='folder',type=str,
                    help='folder with other folders representing albums to upload')
    return parser.parse_args(arg_input)


def main():

    args = parse_args()

    session = upload.get_authorized_session(args.auth_file)

    photos_to_upload = []
    album = None

    if Path(args.photo_folder).is_dir():

        for root, dirs, files in os.walk(args.photo_folder):
            if len(files) > 0:
                path_root = Path(root)
                photos_to_upload.clear()
                for file in files:
                    full_path = Path(root) / file
                    if imghdr.what(full_path) is not None:
                        photos_to_upload.append(full_path)
                if len(photos_to_upload) > 0:
                    upload.upload_photos(session, photos_to_upload, Path(root).name)

        # As a quick status check, dump the albums and their key attributes

        print("{:<50} | {:>8} | {} ".format("PHOTO ALBUM","# PHOTOS", "IS WRITEABLE?"))

        for a in upload.getAlbums(session):
            print("{:<50} | {:>8} | {} ".format(a["title"],a.get("mediaItemsCount", "0"), str(a.get("isWriteable", False))))
    else:
        print(f"Given path {args.photo_folder} is not a folder.")


if __name__ == '__main__':
    main()