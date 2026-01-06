import asyncio

import flet as ft
import flet_map as ftm

def main(page: ft.Page):
    page.title = "Flet Geoportal"
    page.padding = 20

    page.add(
        ftm.Map(
            expand=True,
            initial_center=ftm.MapLatitudeLongitude(51.9189046, 19.1343786),
            initial_zoom=7,
            layers=[
                ftm.TileLayer(
                    url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                    on_image_error=lambda e: print("TileLayer Error"),
                ),
                ftm.SimpleAttribution(
                    text="OpenStreetMap Contributors",
                    alignment=ft.Alignment.BOTTOM_RIGHT,
                    on_click=lambda e: asyncio.create_task(ft.UrlLauncher().launch_url("https://openstreetmap.org/copyright")),
                ),
            ]
        ),
    )

if __name__ == "__main__":
    ft.run(main, view=ft.AppView.WEB_BROWSER, port=8550)