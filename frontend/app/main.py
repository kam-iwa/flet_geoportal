import asyncio

import flet as ft
import flet_map as ftmap

def main(page: ft.Page):
    page.title = "Flet Geoportal"
    page.padding = 20

    map_view = ftmap.Map(
            expand = True,
            initial_center=ftmap.MapLatitudeLongitude(51.9189046, 19.1343786),
            initial_zoom=7,
            max_zoom=19,
            min_zoom=1,
            layers=[
                ftmap.TileLayer(
                    url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                    on_image_error=lambda e: print("TileLayer Error"),
                ),
                ftmap.SimpleAttribution(
                    text="OpenStreetMap Contributors",
                    alignment=ft.Alignment.BOTTOM_RIGHT,
                    on_click=lambda e: asyncio.create_task(ft.UrlLauncher().launch_url("https://openstreetmap.org/copyright")),
                ),
            ]
        )

    page.add(
        ft.Column(
            expand = True,
            spacing = 0,
            controls = [
                ft.Container(
                    content = ft.Column([
                        ft.Text("Flet Geoportal", size=24, text_align=ft.TextAlign.CENTER),
                        ft.Row([
                            ft.VerticalDivider(),
                            ft.IconButton(ft.Icon(ft.Icons.ZOOM_IN), on_click=lambda e: asyncio.create_task(map_view.zoom_in())),
                            ft.IconButton(ft.Icon(ft.Icons.ZOOM_OUT), on_click=lambda e: asyncio.create_task(map_view.zoom_out())),
                            ft.IconButton(ft.Icon(ft.Icons.REFRESH), on_click=lambda e: asyncio.create_task(map_view.zoom_to(7))),
                        ],
                            expand = True,
                            alignment = ft.MainAxisAlignment.END
                        )
                    ]),
                    expand = 1,
                    alignment = ft.Alignment.CENTER
                ),
                ft.Row(
                    expand = 9,
                    spacing = 0,
                    controls = [
                        ft.Container(
                            content = ft.Column(
                                controls = [
                                    ft.Text("Warstwy"),
                                    ft.ListView(controls = [
                                        ft.Checkbox("Przykładowy checkbox warstwy 1"),
                                        ft.Checkbox("Przykładowy checkbox warstwy 2"),
                                        ft.Checkbox("Przykładowy checkbox warstwy 3"),
                                    ])
                                ]
                            ),
                            expand = 1
                        ),
                        ft.Container(
                            content = map_view,
                            expand = 4
                        )
                    ]
                )
            ]
        )
    )

if __name__ == "__main__":
    ft.run(main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=8550)