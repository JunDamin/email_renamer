# %% 파일 수정 시간 변경

import os
import time

# 파일 경로
# file_path = 'email_renamer.py'

# 변경하고자 하는 시간 (예: 2022년 1월 1일)
new_time = time.mktime(time.strptime('2022-01-01', '%Y-%m-%d'))

# 수정된 시간과 접근한 시간 변경
# os.utime(file_path, (new_time, new_time))

# %% eml 파일에서 데이터 추출

import email
import os
from email.parser import BytesParser
from email.policy import default
from email.utils import parseaddr
import re

def extract_info_from_eml(file_path):
    # EML 파일을 읽고 파싱하기
    with open(file_path, 'rb') as file:
        msg = BytesParser(policy=default).parse(file)
    
    # 보낸 사람, 날짜, 시간, 제목 추출
    sender = msg.get('From')
    date = msg.get('Date')
    subject = msg.get('Subject')

    # 보낸 사람 정보 추출 및 이름과 주소 분리
    sender_name, sender_address = parseaddr(sender)

    # 날짜와 시간을 분리하기 (옵션)
    date_time = email.utils.parsedate_to_datetime(date)
    date_str = date_time.strftime("%Y-%m-%d")
    time_str = date_time.strftime("%H:%M:%S")

    return sender_name, sender_address, date_str, time_str, subject

# 사용 예시
# eml_file_path = r'C:\Users\freed\Downloads\[FWD]업데이트 오류에 대한 조치 방법입니다..eml'  # EML 파일 경로
# info = extract_info_from_eml(eml_file_path)
# print(f"보낸 사람: {info[0]}, 보낸 일자: {info[1]}, 보낸 시간: {info[2]}, 제목: {info[3]}")

# %%

import os

def change_file_time(path, date_str, time_str):
    
    # 수정시간 변경
    new_time = time.mktime(time.strptime(f'{date_str} {time_str}', '%Y-%m-%d %H:%M:%S'))
    
    while True:
        os.utime(path, (new_time, new_time))
        time.sleep(0.01)
        mod_time = os.path.getmtime(path)
        if mod_time == new_time:
            break
        time.sleep(0.1)
    return True


def rename_file(original_path, new_name, ):
    # 파일 존재 여부 확인
    if not os.path.exists(original_path):
        return "Error: 원본 파일이 존재하지 않습니다."

    folder, original_filename = os.path.split(original_path)
    new_path = os.path.join(folder, new_name)

    # 새 파일 이름 중복 여부 확인 및 카운트 적용
    count = 1
    filename, file_extension = os.path.splitext(new_name)
    while os.path.exists(new_path):
        new_path = os.path.join(folder, f"{filename}_{count}.{file_extension}")
        count += 1



    # 파일 이름 변경
    os.rename(original_path, new_path)
    
    return f"파일 이름이 '{original_filename}'에서 '{os.path.basename(new_path)}'로 변경되었습니다."

# 사용 예시
# original_file_path =  r'C:\Users\freed\Downloads\test.eml'  # EML 파일 경로
# new_file_name = 'test.eml'   # 새 파일 이름
# result = rename_file(original_file_path, new_file_name, "2022-01-01", "12:12:12")
# print(result)

# %%
import re

def prettify_filename(name):
    result = re.sub(r"[!\"\$\&\'\*\+\,/:;<=>\?\\^_`{|}~\n]", "_", name)
    return re.sub(r" +", r" ", result)