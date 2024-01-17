import flet as ft
from flet import (
    Column,
    Container,
    Draggable,
    DragTarget,
    DragTargetAcceptEvent,
    Page,
    Row,
    border,
    colors,
)

date = {
    "content": ft.Text("일자"),
    "width": 200,
    "height": 50,
    "bgcolor": colors.BLUE_GREY_100,
    "border_radius": 5,
}

time = {
    "content": ft.Text("시간"),
    "width": 200,
    "height": 50,
    "bgcolor": colors.BLUE_GREY_100,
    "border_radius": 5,
}

sender = {
    "content": ft.Text("보낸사람"),
    "width": 200,
    "height": 50,
    "bgcolor": colors.BLUE_GREY_100,
    "border_radius": 5,
}


title = {
    "content": ft.Text("메일제목"),
    "width": 200,
    "height": 50,
    "bgcolor": colors.BLUE_GREY_100,
    "border_radius": 5,
}


def nameController(page):
    def drag_will_accept(e):
        e.control.content.border = border.all(
            2, colors.BLACK45 if e.data == "true" else colors.RED
        )
        e.control.update()

    def drag_accept(e: DragTargetAcceptEvent):
        src = page.get_control(e.src_id)
        e.control.content.bgcolor = src.content.bgcolor
        e.control.content.border = None
        # set text
        e.control.content.content = ft.Text(src.content.content.value)
        e.control.update()
        filename_display.value = "_".join(
            [
                f"<{control.content.content.value}>"
                for control in filename_field.controls
                if control.content.content and control.content.content.value
            ]
        )
        filename_display.update()

        # update attribute
        draggable_name_contorl.name_order = [
            control.content.content.value
            for control in filename_field.controls
            if control.content.content
        ]

    def drag_leave(e):
        e.control.content.border = None
        e.control.update()

    filename_field = Row(
        [
            DragTarget(
                group="eml",
                content=Container(**sender),
                on_will_accept=drag_will_accept,
                on_accept=drag_accept,
                on_leave=drag_leave,
            ),
            DragTarget(
                group="eml",
                content=Container(**date),
                on_will_accept=drag_will_accept,
                on_accept=drag_accept,
                on_leave=drag_leave,
            ),
            DragTarget(
                group="eml",
                content=Container(**time),
                on_will_accept=drag_will_accept,
                on_accept=drag_accept,
                on_leave=drag_leave,
            ),
            DragTarget(
                group="eml",
                content=Container(**title),
                on_will_accept=drag_will_accept,
                on_accept=drag_accept,
                on_leave=drag_leave,
            ),
        ]
    )
    
    filename_display = ft.Text(
        "_".join(
            [
                f"<{control.content.content.value}>"
                for control in filename_field.controls
                if control.content.content and control.content.content.value
            ]
        )
    )

    draggable_name_contorl = Column(
        [
            Row(
                [
                    Draggable(
                        group="eml",
                        content=Container(
                            content=ft.Text("보낸사람"),
                            width=200,
                            height=50,
                            bgcolor=colors.CYAN,
                            border_radius=5,
                        ),
                        content_feedback=Container(
                            width=200,
                            height=50,
                            bgcolor=colors.CYAN,
                            border_radius=3,
                        ),
                    ),
                    Draggable(
                        group="eml",
                        content=Container(
                            content=ft.Text("메일주소"),
                            width=200,
                            height=50,
                            bgcolor=colors.CYAN,
                            border_radius=5,
                        ),
                        content_feedback=Container(
                            width=200,
                            height=50,
                            bgcolor=colors.CYAN,
                            border_radius=3,
                        ),
                    ),
                    Draggable(
                        group="eml",
                        content=Container(
                            content=ft.Text("일자"),
                            width=200,
                            height=50,
                            bgcolor=colors.YELLOW,
                            border_radius=5,
                        ),
                    ),
                    Draggable(
                        group="eml",
                        content=Container(
                            content=ft.Text("시간"),
                            width=200,
                            height=50,
                            bgcolor=colors.GREEN,
                            border_radius=5,
                        ),
                    ),
                    Draggable(
                        group="eml",
                        content=Container(
                            content=ft.Text("제목"),
                            width=200,
                            height=50,
                            bgcolor=colors.GREEN,
                            border_radius=5,
                        ),
                    ),
                    Draggable(
                        group="eml",
                        content=Container(
                            content=ft.Text(""),
                            width=200,
                            height=50,
                            bgcolor=colors.BLUE_GREY_100,
                            border_radius=5,
                        ),
                    ),
                ]
            ),
            Container(width=100),
            Row([filename_field], alignment=ft.MainAxisAlignment.CENTER),
            Row(
                [ft.Text("파일명 형식: "), filename_display],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ]
    )

    return draggable_name_contorl


if __name__ == "__main__":

    def main(page):
        page.add(nameController(page))

    ft.app(target=main)
