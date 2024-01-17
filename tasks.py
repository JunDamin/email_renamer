import flet as ft

def main(page):
    page.title = "Drag and Drop Reordering"

    items = ["Item 1", "Item 2", "Item 3", "Item 4"]

    def on_drop(e):
        nonlocal items
        dragged_item = e.data
        target_index = items.index(e.control.data)
        dragged_index = items.index(dragged_item)
        items.insert(target_index, items.pop(dragged_index))
        update_view()

    def update_view():
        page.controls.clear()
        for item in items:
            page.controls.append(
                ft.DragTarget(
                    data=item,
                    on_accept=on_drop,
                    content=ft.Draggable(
                        data=item,
                        content=ft.Text(value=item)
                    )
                )
            )
        page.update()

    update_view()

ft.app(target=main)
