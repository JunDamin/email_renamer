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

import re

def prettify_filename(name):
    result = re.sub(r"[!\"\$\&\'\*\+\,/:;<=>\?\\^_`{|}~\n]", "_", name)
    return re.sub(r" +", r" ", result)


# %%
import email
from email import policy

def read_eml(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return email.message_from_file(f, policy=policy.default)

def compare_eml(file1, file2):

    if file1 == file2:
        return False
    if not os.path.exists(file1):
        return False 
    if not os.path.exists(file2):
        return False

    # EML 파일 읽기
    eml1 = read_eml(file1)
    eml2 = read_eml(file2)

    # 헤더와 본문 분리 및 비교
    headers1 = dict(eml1.items())
    headers2 = dict(eml2.items())

    # 헤더와 본문 비교
    headers_equal = headers1 == headers2

    return headers_equal

# %%
def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File {file_path} has been deleted.")
    except OSError as e:
        print(f"Error: {e.strerror}")
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


def rename_file(original_path, new_name):
    # 파일 존재 여부 확인
    if not os.path.exists(original_path):
        return "NOT_EXIST"

    folder, original_filename = os.path.split(original_path)
    new_path = os.path.join(folder, new_name)

    # 새 파일 이름 중복 여부 확인 및 카운트 적용
    count = 1
    filename, file_extension = os.path.splitext(new_name)

    
    if compare_eml(original_path, new_path):
        delete_file(original_path)
        return f"DUPLICATES"
    
    # count up
    while os.path.exists(new_path):
        new_path = os.path.join(folder, f"{filename} ({count}){file_extension}")
        count += 1

    # 파일 이름 변경
    os.rename(original_path, new_path)
    
    return f"SUCCESS"


# %%