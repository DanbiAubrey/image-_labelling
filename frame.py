import cv2
from pathlib import Path # instead of os


def extract_frames(video_file_path:Path, output_dir:Path, duration:int=5) -> None:

    cap = cv2.VideoCapture(video_file_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    print(f"{fps = }")

    output_dir.mkdir(exist_ok=True)

    frame_cnt = 0
    success, image = cap.read()

    while success:
        if frame_cnt % fps == 0: # every one second
            frame_time = frame_cnt // fps
            frame_file_name = output_dir / f"frame_{frame_time}.jpg"
            print(f"{frame_file_name = }")
            cv2.imwrite(frame_file_name, image)

            if frame_time >= duration:
                break
        success, image = cap.read()
        frame_cnt += 1

if __name__=='__main__':
    video_file = Path('video.mp4')
    output_dir = Path('frames')
    extract_frames(video_file, output_dir)
