import flet as ft
from flet import (
    TextField,
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Column,
    Row,
)
from name_order import nameController
from functions import extract_info_from_eml, rename_file, prettify_filename


def main(page):
    selected_files = []
    name_controller = nameController(page)

    def on_files_selected(e: FilePickerResultEvent):
        # 선택된 파일들을 리스트에 저장
        nonlocal selected_files
        selected_files = e.files

        for file in selected_files:
            lv.controls.append(ft.Text(f"{file.name}"))
        page.update()

    def rename_files(e):
        nonlocal selected_files
        name_pattern = name_controller.name_order
            
        # 선택된 파일들의 이름을 변경
        for file in selected_files:
            sender_name, sender_address, date_str, time_str, subject = extract_info_from_eml(file.path)

            info = {"보낸사람": sender_name, "메일주소": sender_address, "일자": date_str.replace("-", ""), "시간": time_str.replace(":", ""), "메일제목":subject, }
            filename = "_".join([info.get(pattern) for pattern in name_pattern])
            rename_file(file.path, prettify_filename(filename) + ".eml", date_str, time_str)

            # 초기화
            lv.controls.clear()
            selected_files = []
            lv.update()

    # 여러 파일 선택 가능하도록 설정
    pick_files_dialog = FilePicker(on_result=on_files_selected)
    page.overlay.append(pick_files_dialog)

    # 파일명 변경 버튼
    choose_button = ElevatedButton(
        "파일 선택",
        on_click=lambda _: pick_files_dialog.pick_files(
            allow_multiple=True, allowed_extensions=["eml"]
        ),
    )

    rename_button = ElevatedButton("파일명 변경", on_click=rename_files)
    
    lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)


    # 페이지에 위젯 추가
    page.add(
        ft.Container(
            content=Row(
                [choose_button, rename_button],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
        )
    )
    page.add(
        ft.Container(
            content=Row(
                [name_controller],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
    )
    page.add(
        ft.Container(content=Row([lv], alignment=ft.MainAxisAlignment.CENTER))
    )


ft.app(target=main)
