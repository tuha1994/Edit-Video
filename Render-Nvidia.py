import os,time
import subprocess

def get_video_duration(input_filepath):
    try:
        # Lấy thời lượng của video
        ffprobe_command = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_filepath]
        result = subprocess.run(ffprobe_command, capture_output=True, text=True)
        duration_str = result.stdout.strip()
        if duration_str:
            return float(duration_str)
        else:
            print(f"Không thể lấy thông tin về thời lượng video từ '{input_filepath}'.")
            return None
    except Exception as e:
        print(f"Lỗi xảy ra khi lấy thông tin về thời lượng video từ '{input_filepath}': {e}")
        return None


def cut_video(input_folder, output_folder):
    
    # Lấy đường dẫn tới thư mục đầu vào và đầu ra
    input_video_path = os.path.join(os.getcwd(), input_folder)
    output_video_path = os.path.join(os.getcwd(), output_folder)

    if not os.path.exists(input_video_path) or not os.path.isdir(input_video_path):
        print(f"Thư mục '{input_video_path}' không tồn tại hoặc không phải là một thư mục.")
        return
    for file in os.listdir(input_video_path):
        input_filepath = os.path.join(input_video_path, file)
        if os.path.isfile(input_filepath) and file.lower().endswith('.mp4'):
            duration = get_video_duration(input_filepath)
            
            if duration is not None:
                filename = os.path.splitext(file)[0]
                num_parts = int(filename.split('-')[-1])
                output_filename = os.path.join(output_video_path, f"{filename} - パート")
                for i in range(num_parts):
                    start_time = int(i * (duration / num_parts))
                    dodai = int(duration / num_parts)

                    
                                     
                    time.sleep(5)
                    end_time = (i + 1) * (duration / num_parts)
                    text = 'パート'
                    output_filepath = f"{output_filename} {i+1}-{num_parts}.mp4"
                    text_bottom = f'{text} '
                    line1 = filename.split('-')[0]
                    line2 = filename.split('-')[1]
                    
                    
                    ffmpeg_command = [
                        'ffmpeg', '-y', '-hwaccel', 'cuda', '-hwaccel_output_format', 'cuda', '-i', input_filepath, '-filter_complex',
                        "asetrate=44100*0.94,aresample=44100,atempo=1/0.94,volume=1.12dB;eq=brightness=-0.019:contrast=1.098:saturation=1.085:gamma=1.025:gamma_r=0.983:gamma_b=1.025,scale=720:512,pad=720:1280:(ow - iw)/2:(oh- ih)/2:color=black,setsar=1," +
                        "drawtext=text='" + line1 + "':x=(w-text_w)/2:y=(h-text_h)/6:fontsize=42:fontcolor=white:fontfile='" + font_path + "',drawtext=text='" + line2 + "':x=(w-text_w)/2:y=(h-text_h)/4:fontsize=42:fontcolor=white:fontfile='" + font_path + "',drawtext=text='':x=(w-text_w)/2:y=(h-text_h)/4:fontsize=42:fontcolor=white:fontfile='" + font_path + "',drawtext=text='" + text_bottom + str(i+1) + "/" + str(num_parts) + "':x=(w-text_w)/2:y=(h-text_h)-((h-text_h)/6):fontsize=60:fontcolor=white:fontfile='" + font_path + "'", 
                        '-map_metadata', '-1', '-c:v', 'h264_nvenc', '-preset', 'fast',
                        '-metadata:s', 'title=""', '-metadata', 'artist=""', '-metadata', 'album_artist=""',
                        '-metadata', 'album=""', '-metadata', 'date=""', '-metadata', 'track=""',
                        '-metadata', 'genre=""', '-metadata', 'publisher=""', '-metadata', 'encoded_by=""',
                        '-metadata', 'copyright=""', '-metadata', 'handler_name=""', '-metadata', 'composer=""',
                        '-metadata', 'performer=""', '-metadata', 'TIT1=""', '-metadata', 'TIT3=""',
                        '-metadata', 'disc=""', '-metadata', 'TKEY=""', '-metadata', 'TBPM=""',
                        '-metadata', 'language="eng"', '-metadata', 'encoder=""',
                        '-pix_fmt', 'yuv420p', '-g', '60', '-r', '30',
                        '-b:v', '2000k', '-acodec', 'libmp3lame', '-b:a', '128k', '-ar', '44100',
                        '-ss', str(start_time), '-t', str(int(duration / num_parts)),
                        output_filepath
                    ]
                    # setpts=PTS/2.0, tăng giảm tốc độ
                    subprocess.run(ffmpeg_command)
                    print(f"Đã tạo video mới: {output_filepath}")

input_folder = 'Input Video'
output_folder = 'Output Video'

font_path = 'fontJapan.ttf'
cut_video(input_folder, output_folder)

