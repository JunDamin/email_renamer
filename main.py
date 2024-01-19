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
from functions import (
    extract_info_from_eml,
    rename_file,
    prettify_filename,
    change_file_time,
)


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

        # page.controls.pop()
        pb.visible = True
        # 선택된 파일들의 이름을 변경
        for i, file in enumerate(selected_files):
            (
                sender_name,
                sender_address,
                date_str,
                time_str,
                subject,
            ) = extract_info_from_eml(file.path)

            info = {
                "보낸사람": sender_name,
                "메일주소": sender_address,
                "일자": date_str.replace("-", ""),
                "시간": time_str.replace(":", ""),
                "메일제목": subject,
            }

            change_file_time(file.path, date_str, time_str)

            filename = "_".join(
                [info.get(pattern) for pattern in name_pattern if pattern]
            )
            rename_file(file.path, prettify_filename(filename)[:80] + ".eml")

            progress_text.value = f"{file.name}을 처리중입니다. 기다려 주세요..."
            progress_bar.value = (i + 1) / len(selected_files)
            page.update()

        # 초기화
        # page.controls.pop()
        page.add(lv)
        lv.controls.clear()
        selected_files = []
        progress_text.value = "처리중입니다. 기다려 주세요..."
        lv.update()
        pb.visible = False
        pb.update()

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
    progress_text = ft.Text("처리중입니다. 기다려 주세요...")
    progress_bar = ft.ProgressBar(width=400)
    pb = ft.Container(
        content=Column(
            [
                ft.Text("메일 처리중", theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
                progress_text,
                progress_bar,
            ]
        ),
        visible=False,
    )
    rename_button = ft.FilledButton("파일명 변경", on_click=rename_files)

    lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

    md_explain = """### 사용설명
1. 이름을 바꿀 이메일 파일을 받습니다.(편지함관리에서 pc저장 등을 사용하시면 됩니다.) 
2. 아래 파일 선택 버튼을 누르고 eml 파일을 선택합니다.
3. 파일명 형식에 위에 있는 후보군을 드롭다운하시면 새로운 파일 형식을 지정할 수 있습니다.
4. 파일명을 변경 버튼을 클릭하시면 이메일 파일명이 파일명 형식에 따라 변경됩니다.
    - 이메일 파일의 "수정한 날짜"는 이메일 수신일시로 변경되어 탐색기에서 "수정한 날짜"로 정렬하여 활용이 가능합니다.
"""
    # 페이지에 위젯 추가
    page.add(
        Column(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Image("assets/icon.png", height=30),
                            ft.Text(
                                "Email Renamer v.2",
                                theme_style=ft.TextThemeStyle.TITLE_LARGE,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                ),
                ft.Markdown(
                    md_explain,
                    selectable=True,
                    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                    on_tap_link=lambda e: page.launch_url(e.data),
                ),
                ft.Container(
                    content=ft.Row(
                        [choose_button, rename_button],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    )
                ),
                ft.Divider(),
                ft.Container(
                    content=ft.Row(
                        [name_controller],
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                ),
                pb,
                ft.Divider(),
            ]
        ),
        lv
    )


ft.app(target=main)
