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
from functions import extract_info_from_eml


def main(page):
    selected_files = []
    new_prefix_field = nameController(page)

    def on_files_selected(e: FilePickerResultEvent):
        # 선택된 파일들을 리스트에 저장
        nonlocal selected_files
        selected_files = e.files

        rows = []
        for file in selected_files:
            sender_name, sender_address, date_str, time_str, subject = extract_info_from_eml(file.path)
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(date_str)),
                        ft.DataCell(ft.Text(time_str)),
                        ft.DataCell(ft.Text(sender_name)),
                        ft.DataCell(ft.Text(subject)),
                    ],
                    selected=True,
                    on_select_changed=on_select_changed_handler,
                )
            )
        data_table.rows = rows
        page.update()

    def rename_files(e):
        # 선택된 파일들의 이름을 변경
        for file in selected_files:
            print(extract_info_from_eml(file.path))

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

    data_table = ft.DataTable(
        sort_column_index=0,
        sort_ascending=True,
        heading_row_color=ft.colors.BLACK12,
        heading_row_height=100,
        data_row_color={"hovered": "0x30FF0000"},
        show_checkbox_column=False,
        divider_thickness=0,
        column_spacing=200,
        columns=[
            ft.DataColumn(
                ft.Text("일자"),
            ),
            ft.DataColumn(
                ft.Text("시간"),
            ),
            ft.DataColumn(
                ft.Text("보낸사람"),
                tooltip="보낸사람",
                numeric=False,
            ),
            ft.DataColumn(
                ft.Text("제목"),
                tooltip="이메일 제목",
                numeric=False,
            ),
        ],
    )

    # DataRow 선택 상태 변경 이벤트 핸들러
    def on_select_changed_handler(e):
        # 선택 상태 변경
        e.control.selected = not e.control.selected
        # 페이지 업데이트
        page.update()

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
                [new_prefix_field],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
    )
    page.add(
        ft.Container(content=Row([data_table], alignment=ft.MainAxisAlignment.CENTER))
    )


ft.app(target=main)
