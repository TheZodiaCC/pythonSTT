# pythonSTT
simple Speech To Text converter

### Installation
- `pip3 install -r requirements.txt`
- If you don't have ffmpeg installed: `sudo apt install ffmpeg`

### Usage
- Place audio file into `input` directory
- Run `python3 main.py --language <4_character_language_code>`
- Output will be saved to `out_txt/<audio_file_name>`

### Tips
You can specify `output`, `input` and `segment length` by editing 
`input_files_root`, `out_txt_path`, `segment_time` variables
