import dataclasses
import os.path
import re
import subprocess
import typing


@dataclasses.dataclass
class SourceFile:
    source_video_name: str
    target_name: str
    first_frame: int
    last_frame: int
    first_frame_adjustment: int = 0
    last_frame_adjustment: int = 0
    opening_frame: int = 150
    opening_frame_is_telecined: bool = False


SOURCES = (
    # SourceFile("VHS 10.avi", "OP1", 132716, 135473),
    # SourceFile("VHS 10.avi", "OP2", 135534, 138295),
    # SourceFile("VHS 10.avi", "ED", 138356, 140783),
    # SourceFile("VHS 10.avi", "GAV", 140784, 147645),
    # SourceFile("VHS 10.avi", "BH", 147646, 153429),
    SourceFile("VHS 01 - 01.avi", "01", 285, 0),
    SourceFile("VHS 01 - 02.avi", "02", 0, 0, opening_frame=142),
    SourceFile("VHS 01 - 03.avi", "03", 0, 0, opening_frame=143),
    SourceFile("VHS 01 - 04.avi", "04", 0, 44206, opening_frame=145),
    SourceFile("VHS 02.avi", "05", 839, 45048),
    SourceFile("VHS 02.avi", "06", 45049, 89260),
    SourceFile("VHS 02.avi", "07", 89261, 133470),
    SourceFile("VHS 02.avi", "08", 133471, 177680),
    SourceFile("VHS 03.avi", "09", 359, 44570),
    SourceFile("VHS 03.avi", "10", 44571, 88782),
    SourceFile("VHS 03.avi", "11", 88783, 132992),
    SourceFile("VHS 03.avi", "12", 132993, 177204),
    SourceFile("VHS 04 - 13.avi", "13", 26, 0),
    SourceFile("VHS 04 - 14.avi", "14", 0, 0, opening_frame=145),
    SourceFile("VHS 04 - 15.avi", "15", 0, 0, opening_frame=146),
    SourceFile("VHS 04 - 16.avi", "16", 0, 44207, opening_frame=146),
    SourceFile("VHS 05 - 17.avi", "17", 307, 0),
    SourceFile("VHS 05 - 18.avi", "18", 0, 0, opening_frame=143),
    SourceFile("VHS 05 - 19.avi", "19", 0, 0, opening_frame=146),
    SourceFile("VHS 05 - 20.avi", "20", 0, 44206, opening_frame=149),
    SourceFile("VHS 06.avi", "21", 853, 45064, -1, -2),  # extaud
    SourceFile("VHS 06.avi", "22", 45065, 89276, -2, -3),  # extaud
    SourceFile("VHS 06.avi", "23", 89277, 133491, -3, -4),  # extaud
    SourceFile("VHS 06.avi", "24", 133492, 177703, -4, -5),  # extaud
    SourceFile("VHS 07 - 25.avi", "25", 401, 0, opening_frame=149, opening_frame_is_telecined=True),
    SourceFile("VHS 07 - 26.avi", "26", 0, 0, opening_frame=145, opening_frame_is_telecined=True),
    SourceFile("VHS 07 - 27.avi", "27", 0, 0, opening_frame=149),
    SourceFile("VHS 07 - 28.avi", "28", 0, 44210, opening_frame=149),
    SourceFile("VHS 08 - 29.avi", "29", 300, 0),
    SourceFile("VHS 08 - 30.avi", "30", 0, 0, opening_frame=144),
    SourceFile("VHS 08 - 31.avi", "31", 0, 0, opening_frame=146),
    SourceFile("VHS 08 - 32.avi", "32", 0, 44205, opening_frame=146),
    SourceFile("VHS 09.avi", "33", 847, 45056, -1, -2, opening_frame=149, opening_frame_is_telecined=True),  # extaud

    # OP2
    SourceFile("VHS 09.avi", "34", 45057, 89128, -2, -3, opening_frame=151, opening_frame_is_telecined=True),  # extaud
    SourceFile("VHS 09.avi", "35", 89129, 133338, -3, -4, opening_frame=151, opening_frame_is_telecined=True),  # extaud
    SourceFile("VHS 09.avi", "36", 133339, 177546, -4, -5, opening_frame=151, opening_frame_is_telecined=True),
    # extaud
    SourceFile("VHS 10.avi", "37", 836, 45044, opening_frame=152),
    SourceFile("VHS 10.avi", "38", 45044, 89254, opening_frame=152),
    SourceFile("VHS 10.avi", "39", 89254, 132408, opening_frame=0),
)


def extract_avis():
    for sf in SOURCES:
        if os.path.exists(fr"src\{sf.target_name}.avi"):
            continue
        cmdline = [
            "ffmpeg",
            "-hide_banner",
            "-i", fr"vhs\{sf.source_video_name}",
        ]
        if sf.first_frame != 0:
            cmdline += ["-ss", str((sf.first_frame + sf.first_frame_adjustment) * 1001 / 30000)]
        if sf.last_frame != 0:
            cmdline += ["-to", str((sf.last_frame + sf.last_frame_adjustment + 1) * 1001 / 30000)]
        cmdline += ["-c", "copy"]
        cmdline.append(fr"src\{sf.target_name}.avi")
        print(cmdline)
        with subprocess.Popen(cmdline) as subproc:
            subproc.communicate()
    return 0


def extract_episode_audio():
    for sf in SOURCES:
        cmdline = [
            "ffmpeg",
            "-hide_banner",
            "-i", fr"flac\{sf.target_name}.flac",
            "-ss", str(sf.opening_frame * 1001 / 30000),
            f"episode_audio/{sf.target_name}.wav",
        ]
        if os.path.exists(cmdline[-1]):
            continue
        print(cmdline)
        with subprocess.Popen(cmdline) as subproc:
            subproc.communicate()


def tfm_output_to_ovr(data: typing.TextIO):
    first_frame = -1
    codes = []
    deints = []
    for line in data:
        if line.startswith("#"):
            continue
        line = line.split(" ", 4)
        if len(line) < 4:
            continue
        try:
            frame, code, interlaced, *_ = line
            frame = int(frame)
        except:
            continue
        if first_frame == -1:
            first_frame = frame
        codes.append(code)
        deints.append(interlaced)
        if len(codes) == 10:
            yield f"{first_frame},{first_frame + len(codes) - 1} " + "".join(codes) + "\n"
            if "+" in deints:
                yield f"{first_frame},{first_frame + len(codes) - 1} " + "".join(deints) + "\n"
            first_frame = -1
            codes.clear()
            deints.clear()


def create_override_files():
    for sf in SOURCES:
        if not os.path.exists(fr"Z:\dconv2\src\TFM_{sf.target_name}.txt"):
            with open("Z:/dconv2/tmpf.avs", "w") as fp:
                fp.write(rf'LWLibavVideoSource("Z:\dconv2\src\{sf.target_name}.avi")')
                fp.write("\n")
                fp.write(rf'Trim({2758 + sf.opening_frame}, 0)')
                fp.write("\n")
                fp.write(rf'TFM(mode=1, PP=1, output="Z:\dconv2\src\TFM_{sf.target_name}.txt")')
                fp.write("\n")
            cmdline = [
                "ffmpeg",
                "-hide_banner",
                "-i", "tmpf.avs",
                "-f", "null",
                "NUL",
            ]
            print(cmdline)
            with subprocess.Popen(cmdline) as subproc:
                subproc.communicate()
        if not os.path.exists(fr"Z:\dconv2\src\TFM_{sf.target_name}_override.txt"):
            with open(fr"Z:\dconv2\src\TFM_{sf.target_name}.txt") as fp:
                with open(fr"Z:\dconv2\src\TFM_{sf.target_name}_override.txt", "w") as fp2:
                    for line in tfm_output_to_ovr(fp):
                        fp2.write(line)


def __main__():
    # extract_episode_audio()
    # extract_avis()
    # create_override_files()
    pass


if __name__ == "__main__":
    exit(__main__())
