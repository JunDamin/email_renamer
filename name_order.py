import flet as ft
from flet import (
    Column,
    Container,
    Draggable,
    DragTarget,
    DragTargetAcceptEvent,
    Row,
    border,
    colors,
)
from copy import deepcopy

options_setting = {
    "일자": colors.AMBER_ACCENT_100,
    "시간": colors.AMBER_100,
    "보낸사람": colors.TEAL_100,
    "메일주소": colors.BLUE_100,
    "메일제목": colors.DEEP_ORANGE_100,
}

initial_setting = {
    key: options_setting.get(key) for key in ["일자", "시간", "보낸사람", "메일제목"]
}

example = {
    "보낸사람": "전다민",
    "메일주소": "jdm@koica.go.kr",
    "일자": "20240116",
    "시간": "091102",
    "메일제목": "[RE][Re] 이메일 백업 안내",
}


class Item(Draggable):
    def __init__(
        self,
        page,
        group,
        text,
        parent=None,
        drag_will_accept=None,
        drag_leave=None,
        width=70,
        height=30,
        bgcolor=colors.GREY_300,
        border_radius=10,
        alignment=ft.alignment.center,
    ):
        self.page = page
        self._content_text = text
        self.parent = parent
        self._color = bgcolor
        self.content = DragTarget(
            self,
            group=group,
            content=Container(
                content=ft.Text(text),
                width=width,
                height=height,
                bgcolor=self.color,
                border_radius=border_radius,
                alignment=alignment,
            ),
            on_will_accept=drag_will_accept,
            on_accept=self.drag_accept,
            on_leave=drag_leave,
        )
        self.content.parent = self
        super().__init__(
            content=self.content,
            group=group,
            content_feedback=Container(
                width=width,
                height=height,
                bgcolor=bgcolor,
                border_radius=border_radius,
                content=ft.Text(text, theme_style=ft.TextThemeStyle.BODY_MEDIUM),
                alignment=ft.alignment.center
            ),
        )

    @property
    def content_text(self):
        return self._content_text

    @content_text.setter
    def content_text(self, text):
        self._content_text = text
        self.content.content.content = ft.Text(text)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, bgcolor):
        self._color = bgcolor
        self.content.content.bgcolor = bgcolor

    def drag_accept(self, e: DragTargetAcceptEvent):
        e.control.content.border = None
        src = self.page.get_control(e.src_id)
        target = e.control.parent

        src.color, target.color = target.color, src.color
        src.content_text, target.content_text = target.content_text, src.content_text

        src.update()
        target.update()

        if self.parent:
            self.parent.update()


class Fields:
    def __init__(self):
        self._items = []

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, items):
        self._items = items
        self.order = [item.content_text for item in self._items]
        self.filename = "_".join([example.get(text) for text in self.order if text])
        self.filename_display = ft.Text(self.filename)

    def update(self):
        self.order[:] = [item.content_text for item in self.items]
        self.filename = "_".join([example.get(text) for text in self.order if text])
        self.filename_display.value = self.filename
        self.filename_display.update()


def nameController(page):
    def drag_will_accept(e):
        e.control.content.border = border.all(
            2, colors.BLACK45 if e.data == "true" else colors.RED
        )
        e.control.update()

    def drag_leave(e):
        e.control.content.border = None
        e.control.update()

    fields = Fields()
    fields.items = [
        Item(
            page=page,
            group="eml",
            text="",
            drag_will_accept=drag_will_accept,
            drag_leave=drag_leave,
            parent=fields,
        )
        for _ in range(4)
    ]


    option_list = [
        Item(page, group="eml", text=name, bgcolor=bgcolor, parent=fields)
        for name, bgcolor in options_setting.items()
    ]

    draggable_name_contorl = Column(
        [
            Row(
                [
                    ft.Text("파일명 예시: ", theme_style=ft.TextThemeStyle.BODY_LARGE),
                    fields.filename_display,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            Container(
                content=Row(
                    [
                        ft.Text("이름 패턴: ", theme_style=ft.TextThemeStyle.BODY_MEDIUM),
                        *fields.items,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                padding=10,
                border_radius=10,
                border=ft.border.all(2, colors.BLUE_100),
            ),
            Container(width=100),
            Container(
                content=Row(
                    controls=option_list,
                ),
                bgcolor=colors.WHITE,
                padding=10,
                border_radius=10,
            ),
        ]
    )

    draggable_name_contorl.name_order = fields.order

    return draggable_name_contorl


if __name__ == "__main__":

    def main(page):
        page.add(nameController(page))

    ft.app(target=main)
