import flet as ft
from flet import (
    TextField,
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Column,
    Row,
    colors,
)
from name_order import nameController
from functions import (
    extract_info_from_eml,
    rename_file,
    prettify_filename,
    change_file_time,
)
import os


def main(page):
    selected_files = []
    name_controller = nameController(page)
    n_files = 0

    def on_files_selected(e: FilePickerResultEvent):
        # 선택된 파일들을 리스트에 저장
        nonlocal selected_files
        selected_files = e.files
        nonlocal n_files

        if not selected_files:
            page.update()
            return None

        n_files = len(selected_files)
        for file in selected_files:
            lv.controls.append(ft.Text(f"{file.name}"))
        lv_divider.visible = True
        page.update()

    def rename_files(e):
        nonlocal selected_files
        if not selected_files:
            return
        error_list = []
        name_pattern = name_controller.name_order
        rename_button.disabled = True
        rename_button.update()
        pb.visible = True

        status = {"SUCCESS": 0, "NOT_EXIST": 0, "DUPLICATES": 0}
        # 선택된 파일들의 이름을 변경
        for i, file in enumerate(selected_files):
            if not os.path.exists(file.path):
                error_list.append(file.path)
                status["NOT_EXIST"] += 1
                continue

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
            if filename == "":
                filename = "파일명없음"

            res = rename_file(file.path, prettify_filename(filename)[:80] + ".eml")

            status[res] += 1

            progress_text.value = f"{file.name}을 처리중입니다. 기다려 주세요... "
            progress_bar.value = (i + 1) / len(selected_files)
            page.update()

        result_text.value = (
            f"""{status.get('SUCCESS')}건의 변환을 완료하였습니다.
        """
            + (
                f"\n{status.get('DUPLICATES')}개 중복 파일이 있었습니다."
                if status.get("DUPLICATES")
                else ""
            )
            + (
                (
                    f"\n하기의 {status.get('NOT_EXIST')}개의 파일은 찾을 수 없었습니다.\n"
                    + "\n".join(f"1. {path}" for path in error_list)
                )
                if error_list
                else ""
            )
        )

        show_result(None)

        # 초기화
        # page.controls.pop()
        page.add(lv)
        lv.controls.clear()
        selected_files = []
        progress_text.value = "처리중입니다. 기다려 주세요..."
        lv.update()
        lv_divider.visible = False
        lv_divider.update()
        pb.visible = False
        pb.update()
        rename_button.disabled = False
        rename_button.update()

    def show_result(e):
        result.open = True
        result.update()

    def close_result(e):
        result.open = False
        result.update()

    result_text = ft.Markdown(
        value=f"{n_files}건의 변환을 완료하였습니다.",
        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
        selectable=True,
    )
    result = ft.AlertDialog(
        modal=True,
        title=ft.Text("변환완료"),
        content=ft.Container(
            ft.Column(
                [
                    result_text,
                    ft.ElevatedButton("닫기", on_click=close_result),
                ],
                tight=True,
                width=500,
            ),
            padding=10,
        ),
        open=False,
        adaptive=True,
    )
    page.overlay.append(result)

    def show_bs(e):
        bs.open = True
        bs.update()

    def close_bs(e):
        bs.open = False
        bs.update()

    md_explain = """### 사용설명 
1. 이름을 바꿀 이메일 파일을 받아 한 폴더에 모아둡니다.(편지함관리에서 pc저장 등을 사용하시면 됩니다.)
2. "파일선택" 버튼을 누르고 모아둔 eml 파일을 선택합니다.(단, Kdocu에 있는 파일은 작동하지 않습니다.)
3. 드래그엔 드롭을 하여 원하는 이름 패턴를 정합니다.(파일명 예시를 참고하세요.)
4. "파일명 변경" 버튼을 클릭하시면 선택된 이메일들의 파일명이 지정한 이름 순서에 따라 변환됩니다.
    - 이메일 파일의 "수정한 날짜"는 이메일 수신일시로 변경되어 탐색기에서 정렬하여 활용이 가능합니다.
"""
    bs = ft.AlertDialog(
        modal=True,
        title=ft.Text("사용설명"),
        content=ft.Container(
            ft.Column(
                [
                    ft.Markdown(
                        md_explain,
                        selectable=True,
                        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                        on_tap_link=lambda e: page.launch_url(e.data),
                    ),
                    ft.ElevatedButton("사용설명 닫기", on_click=close_bs),
                ],
                tight=True,
                width=500,
            ),
            padding=10,
        ),
        open=False,
        adaptive=True,
    )
    page.overlay.append(bs)

    bs_button = ft.FilledTonalButton(text="사용설명", on_click=show_bs)

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
    lv_divider = ft.Divider(visible=False)

    # windows
    page.window_max_width = 450
    page.window_width = 450
    page.update()

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
                    ),
                    padding=20,
                    bgcolor=colors.GREY_300,
                ),
                ft.Container(
                    content=ft.Row(
                        [choose_button, rename_button, bs_button],
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
                lv_divider,
            ]
        ),
        lv,
    )


ft.app(target=main)
