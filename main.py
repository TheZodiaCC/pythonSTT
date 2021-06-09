import speech_recognition as sr
import os
import subprocess
import argparse
from tqdm import tqdm


def convert_audio(input, dest):
    new_file_name = input.split(".")[0]
    new_file_name = f"{new_file_name}.{dest}"
    new_file_name = f'out/{new_file_name.split("/")[1]}'

    subprocess.call(["ffmpeg", "-i", input,
                     new_file_name])


def split_file(input_path, segment_time):
    file_name = input_path.split("/")
    file_name = file_name[1].split(".")[0]

    out = f"out/{file_name}"
    os.mkdir(out)

    subprocess.call(["ffmpeg", "-i", input_path,
                     "-f", "segment", "-segment_time", str(segment_time), "-c", "copy", f"{out}/out%03d.wav"])


def recognize_files(speech_recognizer, input_path, out_txt_path, language):
    input_path = input_path.split(".")[0]

    with open(out_txt_path, "a") as txt_file:
        for file in tqdm(sorted(os.listdir(input_path))):
            try:
                file_path = os.path.join(input_path, file)

                input_wav = sr.AudioFile(file_path)

                with input_wav as source:
                    audio = speech_recognizer.record(source)

                    txt = speech_recognizer.recognize_google(audio, language=language)

                    txt_file.write(txt)
                    txt_file.write("\n")

            except Exception as e:
                print(f"Error during processing {file_path}")


def main(opt):
    speech_recognizer = sr.Recognizer()

    input_files_root = "input"
    out_txt_path = "out_txt"
    segment_time = 5
    language = opt.language[0]

    for file in sorted(os.listdir(input_files_root)):
        try:
            print(f"Processing {file}")

            input_path = os.path.join(input_files_root, file)

            if not input_path.endswith(".wav") or not input_path.endswith(".WAV"):
                convert_audio(input_path, "wav")

            new_input_path = os.path.join("out", f'{file.split(".")[0]}.wav')
            split_file(new_input_path, segment_time)

            txt_file_name = f'{file.split(".")[0]}.txt'
            out_txt = os.path.join(out_txt_path, txt_file_name)
            recognize_files(speech_recognizer, new_input_path, out_txt, language)

        except Exception as e:
            print(e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--language', nargs='+', type=str, default='en-US', help='input language code')
    opt = parser.parse_args()

    main(opt)
