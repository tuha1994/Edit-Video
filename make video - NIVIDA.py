import glob
import os
import random
import subprocess

num_profile1 = int(input('Nhập số Profile bắt đầu: '))
num_profile2 = int(input('Nhập số Profile kết thúc: '))
for i in range(num_profile1, num_profile2 + 1):
    profile = f'Profile{i}'
    output_video_folder = f'{profile}/Output Video'
    os.makedirs(output_video_folder, exist_ok=True)

    txt_files = glob.glob('*.txt')
    video_files = glob.glob(f'{profile}/Input Video/*.mp4')
    for file_name in txt_files:
        input_video = random.choice(video_files)
        font_files = glob.glob(f'{profile}/Input Font/*.ttf')
        font_file = random.choice(font_files)
        font_file_path = font_file.replace('\\', '/')
        base_txt_name = os.path.basename(file_name).split('.')[0] + '.mp4'
        output_video = os.path.join(output_video_folder, f'output_{base_txt_name}')
        command = f'ffmpeg -hwaccel cuda -y -i "{input_video}" -vf "drawtext=textfile=\'{file_name}\':x=(w-text_w)/2:y=(h-text_h)/2:line_spacing=60:fontsize=60:fontcolor=white:borderw=3:bordercolor=black:fontfile=\'{font_file_path}\'" -an -c:v h264_nvenc -preset slow -rc:v vbr_hq -cq:v 19 -b:v 0 "{output_video}"'

        subprocess.run(command, shell=True)


# Đã chạy ổn định, sử dụng được nhiều fonts chữ, nhiều video đầu vào

# Dưới đây là code thêm ảnh random nhé

# import glob
# import os
# import random
# import subprocess

# output_video_folder = './Output Video'
# os.makedirs(output_video_folder, exist_ok=True)

# txt_files = glob.glob('*.txt')
# video_files = glob.glob('./Input Video/*.mp4')
# input_video = random.choice(video_files)

# # Lấy danh sách các file ảnh hình chữ nhật
# rectangle_images = glob.glob('./Rectangle Images/*.png')  # Giả sử các hình chữ nhật là file .png
# selected_image = random.choice(rectangle_images)

# for file_name in txt_files:
#     font_files = glob.glob(r'./Input Font/*.ttf')
#     font_file = random.choice(font_files)
#     font_file_path = font_file.replace('\\', '/')
#     base_txt_name = os.path.basename(file_name).split('.')[0] + '.mp4'
#     output_video = os.path.join(output_video_folder, f'output_{base_txt_name}')
#     command = f'ffmpeg -i "{input_video}" -i "{selected_image}" -filter_complex "[0:v][1:v] overlay=25:25:format=auto, drawtext=textfile=\'{file_name}\':x=(w-text_w)/4:y=(h-text_h)/2:line_spacing=30:fontsize=60:fontcolor=white:borderw=3:bordercolor=black:fontfile=\'{font_file_path}\'" -c:a copy -c:v libx264 -preset slow -crf 18 "{output_video}"'
    
#     # Thực thi câu lệnh
#     subprocess.run(command, shell=True)
