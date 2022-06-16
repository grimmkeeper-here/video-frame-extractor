# Import lib
import cv2 # type:ignore
from typing import Generator,Any,Tuple

# Global var
VIDEOS_LOAD_PATH = "./videos"
IMAGES_SAVE_PATH = "./images"
FRAME_THRESHOLD = 500

# Func
def load_videos_from_path()->Generator[Tuple[str,cv2.VideoCapture],Any,Any]:
    from os import listdir
    from os.path import isfile, join
    for _file in listdir(VIDEOS_LOAD_PATH):
        if isfile(join(VIDEOS_LOAD_PATH, _file)):
            yield _file,cv2.VideoCapture(join(VIDEOS_LOAD_PATH, _file))

def store_frames_to_images(vid_name:str,vidcap:cv2.VideoCapture)->None:
    import os
    img_store_path = f"{IMAGES_SAVE_PATH}/{vid_name.split('.')[0]}"
    if not os.path.isdir(img_store_path):
        os.mkdir(img_store_path)
    success,image = vidcap.read()
    count = 0
    while success:
        vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*FRAME_THRESHOLD))
        success,image = vidcap.read()
        cv2.imwrite(f"{img_store_path}/frame-{count}.jpg", image)
        print(f'{vid_name} - frame {count} saved: ', success)
        count += 1

# Main
if __name__ == "__main__":
    import argparse
    a = argparse.ArgumentParser()
    a.add_argument("--videos", help="path to place load your videos")
    a.add_argument("--images", help="path to place save your images")
    a.add_argument("--thresh", help="thresh second per frame", default=FRAME_THRESHOLD)
    args = a.parse_args()
    VIDEOS_LOAD_PATH = args.videos
    IMAGES_SAVE_PATH = args.images
    FRAME_THRESHOLD = int(args.thresh) if isinstance(args.thresh,str) else args.thresh
    for vid_name,vidcap in load_videos_from_path():
        print(f"Video name: {vid_name}")
        try:
            store_frames_to_images(vid_name=vid_name,vidcap=vidcap)
        except cv2.error:
            continue
        finally:
            print("#####################################################")
