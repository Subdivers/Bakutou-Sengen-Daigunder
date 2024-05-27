import dataclasses
import os.path
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


def encode(sf: SourceFile):
    ovr_path = fr"Z:\dconv2\src\TFM_{sf.target_name}_override.txt"
    ranges = []
    with open(ovr_path) as fp:
        for line in fp:
            if not line.startswith("#filter:"):
                continue
            line = line[8:].strip().split(" ", 1)
            if len(line) != 2:
                continue
            frame_first, frame_last = line[0].split(",")
            frame_first = int(frame_first.strip(), 10)
            frame_last = int(frame_last.strip(), 10)
            if not ranges and frame_first != 0:
                ranges.append((0, frame_first - 1, "TDecimate(mode=1)"))
            elif ranges and frame_first != ranges[-1][1] + 1:
                ranges.append((ranges[-1][1] + 1, frame_first - 1, "TDecimate(mode=1)"))
            ranges.append((frame_first, frame_last, line[1].strip()))

    if ranges:
        ranges.append((ranges[-1][1] + 1, 0, "TDecimate(mode=1)"))

    with open("Z:/dconv2/tmpf.avs", "w") as fp:
        fp.write(rf'LWLibavVideoSource("Z:\dconv2\src\{sf.target_name}.avi")' + "\n")
        fp.write(rf'Trim({2758 + sf.opening_frame}, 0)' + "\n")
        fp.write("ConvertToYV24()\n")
        fp.write(rf'ep = TFM(mode=1, PP=7, ovr="{ovr_path}", clip2=QTGMC().SelectEven())' + "\n")
        fp.write(rf'p0 = LWLibavVideoSource("Z:\dconv2\brightroom.mp4").ConvertToYV24().AssumeFPS(24000, 1001)' + "\n")
        fp.write(rf'p1 = LWLibavVideoSource("Z:\dconv2\ep_op1_avgall.mp4").ConvertToYV24().AssumeFPS(24000, 1001)' +
                 "\n")
        fp.write('space = " "\n')
        fp.write(r'ep.WriteFileStart("Z:\dconv2\frames.txt", "", append=false)' + "\n")

        if ranges:
            first = True
            for frame_first, frame_last, filters in ranges:
                fp.write(f"ptsrc = ep.Trim({frame_first}, {frame_last})\n")
                if filters and filters != "_":
                    fp.write(f"pt = ptsrc.{filters}\n")
                else:
                    fp.write("pt = ptsrc\n")
                fp.write(
                    r'pt.WriteFileStart( ' '\\\n'
                    r'    "Z:\dconv2\frames.txt", ' '\\\n'
                    r'    "ptsrc.FrameCount", "space", ' '\\\n'
                    r'    "FrameCount", "space", ' '\\\n'
                    r'    "FrameRateNumerator", "space", ' '\\\n'
                    r'    "FrameRateDenominator", ' '\\\n'
                    r'    append=true)' '\n')
                if first:
                    fp.write("c = ")
                    first = False
                else:
                    fp.write("c = c + ")
                fp.write('pt.AssumeFPS(24000, 1001)\n')
        else:
            fp.write("c = ep.TDecimate(mode=1)")

        fp.write("p0 + p1 + c.BilinearResize(640, 480, 10, 0, -4, -0)\n")
    cmdline = [
        "ffmpeg",
        "-hide_banner", "-y",
        "-i", "tmpf.avs",
        "-i", "ep_brightroom_and_op1.wav",
        "-i", f"src/flac/{sf.target_name}.flac",
        # "-f", "ffmetadata", "-i", "tmp.chapter.txt",
        "-c:v", "libx264",
        "-crf", "19",
        "-preset", "veryslow",
        "-c:a", "flac",
        "-compression_level", "8",
        "-filter_complex", ";".join((
            f"[2:a:0]atrim=start={(sf.opening_frame + 2758) * 1001 / 30000},asetpts=PTS-STARTPTS[epaudio]",
            "[1:a:0][epaudio]concat=n=2:v=0:a=1[outa]"
        )),
        "-map", "0:v",
        "-map", "[outa]",
        "-map_metadata", "1",
        "-metadata:s:v:0", "language=jpn",
        "-metadata:s:a:0", "language=jpn",
        fr"output\{sf.target_name}_tmp.mp4",
    ]
    print(cmdline)
    with subprocess.Popen(cmdline) as subproc:
        subproc.communicate()
    framerates = [
        (150, 120, 24000, 1001),
        (1146, 916, 24000, 1001),
        (78, 46, 18000, 1001),
        (1534, 1227, 24000, 1001),
    ]
    with open("Z:/dconv2/frames.txt") as fp:
        for line in fp:
            line = line.strip().split(" ")
            if len(line) != 4:
                continue
            num_old_frames, num_new_frames, num, denom = line
            num_new_frames = int(num_new_frames, 10)
            num_old_frames = int(num_old_frames, 10)
            num = int(num)
            denom = int(denom)
            framerates.append((num_old_frames, num_new_frames, num, denom))

    timecodes = []
    mytime = 0
    for num_old_frames, num_new_frames, num, denom in framerates:
        for i in range(num_new_frames):
            timecodes.append(mytime + 1000 * (i * denom / num))
        mytime += 1000 * num_old_frames * 1001 / 30000
        pass

    with open("Z:/dconv2/timecodes.txt", "w") as fp:
        fp.write("\n".join(str(int(x)) for x in timecodes))

    cmdline = [
        "mp4fpsmod",
        "-t", "Z:/dconv2/timecodes.txt",
        "-o", f"output/{sf.target_name}.mp4",
        "-x",
        f"output/{sf.target_name}_tmp.mp4",
    ]
    print(cmdline)
    with subprocess.Popen(cmdline) as subproc:
        subproc.communicate()


def __main__():
    encode(SOURCES[3])
    # extract_episode_audio()
    # extract_avis()
    # create_override_files()
    pass


if __name__ == "__main__":
    exit(__main__())
