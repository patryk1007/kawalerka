"""Zrzuty ekranu modelu do sprawdzenia zmian.
Użycie: pip install playwright && playwright install chromium
        python3 tools/screenshot.py
Wynik: shots/spacer.png, shots/z_gory.png, shots/z_gory_slupek.png, shots/z_gory_deweloper.png
"""
import asyncio, pathlib
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "shots"

async def main():
    OUT.mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"])
        pg = await b.new_page(viewport={"width": 1200, "height": 760})
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        await pg.goto((ROOT / "index.html").as_uri())
        await pg.evaluate("localStorage.clear()")
        await pg.reload()
        await pg.wait_for_timeout(2500)
        await pg.screenshot(path=OUT / "spacer.png")
        await pg.click("#mode button[data-m=top]")
        await pg.wait_for_timeout(800)
        await pg.screenshot(path=OUT / "z_gory.png")
        await pg.select_option("#fridge", "slupek")
        await pg.wait_for_timeout(800)
        await pg.screenshot(path=OUT / "z_gory_slupek.png")
        await pg.select_option("#fridge", "pod")
        await pg.click("#bath button[data-v=dev]")
        await pg.wait_for_timeout(800)
        await pg.screenshot(path=OUT / "z_gory_deweloper.png")
        print("Błędy JS:", errors or "brak")
        await b.close()

asyncio.run(main())
