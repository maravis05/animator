import os
import tkinter.filedialog
import shutil
from datetime import datetime


# currently hardcoded to use jpg as input file type
# ffmpeg MUST be installed and in the system environment variables (PATH)
# output resolution is matched to first frame


def main():
    os.system("clear")
    print("......IMAGE ANIMATOR......")
    source_files, source_dir = get_sfiles()
    output_dir = get_odir()
    fps = get_fps(len(source_files))

    print("..........................")
    print(".........SUMMARY..........")
    print(
        f"Encoding {len(source_files)} files at {round(fps,2)} fps. This will create a video {int(len(source_files)/fps)} seconds long at:\n{output_dir}"
    )
    choice = input("Enter [y] to continue\n")
    if choice.casefold() == "y":
        temp_files(source_files, source_dir, output_dir)
        create_mkv(output_dir, fps)
        print("\n\n\nClip successfully created!")


def temp_files(source_files, source_dir, outdir):
    os.makedirs(f"{outdir}/temp", exist_ok=True)
    a = 1
    for filename in source_files:
        shutil.copy2(f"{source_dir}/{filename}", f"{outdir}/temp/frame.{a:06}.jpg")
        a += 1


def create_mkv(working_dir, fps):

    # -video_size {resolution}

    os.system(
        f"ffmpeg -framerate {fps} -i {working_dir}/temp/frame.%06d.jpg {working_dir}/clip_{datetime.now().timestamp()}.mkv"
    )
    shutil.rmtree(f"{working_dir}/temp", ignore_errors=True)


def get_fps(frames):
    duration = input(
        "How many seconds to display each image? (the resulting fps will be 1/this#) \nThis should probably be less than one. Get creative!\n"
    )
    try:
        duration = float(duration)
    except:
        print("That's weird. Try to put in a number. (Can be float value.)")
        get_fps(frames)
    return 1 / duration


def get_odir():
    print("Select *output* directory for images.\n")
    output_dir = tkinter.filedialog.askdirectory()
    try:
        with open(f"{output_dir}/test", mode="x") as fp:
         print('directory writable...')
    except:
        print("Having trouble writing to that directory.")
        get_odir()

    os.remove(f"{output_dir}/test")
    return output_dir


def get_sfiles():
    print("Select *source* directory for images.\n")
    source_dir = tkinter.filedialog.askdirectory()
    frames = []

    print("Scanning directory for image files...")
    supported_types = ['.jpg', '.jpeg', '.png']
    for entry in os.scandir(source_dir):
        if entry.is_file():
            if any([ext in entry.name.casefold() for ext in supported_types]):
                frames.append(entry.name)

    if len(frames) < 1:
        print("That's a short video! Try a directory that has at least one jpg file.")
        get_sfiles()

    frames.sort()
    print(f"Found {len(frames)} images.")
    return frames, source_dir


if __name__ == "__main__":
    main()
