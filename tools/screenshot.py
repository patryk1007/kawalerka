"""Zrzuty ekranu modelu do sprawdzenia zmian.
Użycie: pip install playwright && playwright install chromium
        python3 tools/screenshot.py
Wynik: shots/spacer.png, shots/z_gory.png, shots/z_gory_slupek.png, shots/z_gory_rtv_bez_gornych.png, shots/z_gory_deweloper.png, shots/szopka.png
       oraz tryb realistyczny: shots/real_*.png (python3 tools/screenshot.py real – tylko te)
"""
import asyncio, pathlib, sys
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
        pg.on("console", lambda m: m.type == "error" and errors.append(m.text))
        await pg.goto((ROOT / "index.html").as_uri())
        await pg.evaluate("localStorage.clear()")
        await pg.reload()
        await pg.wait_for_timeout(2500)
        if len(sys.argv) < 2 or sys.argv[1] != "real":
            await mock(pg)
        await real(pg)
        print("Błędy JS:", errors or "brak")
        await b.close()

async def real(pg):
    """Tryb realistyczny: kilka kadrów ze spaceru (x, z, yaw, pitch), wieczór i widok z góry."""
    await pg.click("#style button[data-s=real]")
    await pg.wait_for_function("document.getElementById('hud').textContent.includes('realistyczny')", timeout=60000)
    await pg.wait_for_timeout(1500)
    views = [("real_wejscie", 1.25, .8, 3.1416, -.05), ("real_pokoj", 2.7, 6.3, .25, -.08),
             ("real_kuchnia", 1.4, 4.9, -0.75, -.12), ("real_lazienka", 2.2, .5, -2.45, -.2),
             ("real_lustro", 3.3, 1.35, 0.15, -.1), ("real_ogrod", 2.4, 10.5, 0, .02),
             ("real_szopka", 2.7, 10.2, .76, -.1), ("real_szopka_blat", 1.2, 8.15, .29, -.3), ("real_szopka_regal", 1.2, 7.95, 2.85, -.25)]
    for name, x, z, yaw, pitch in views:
        await pg.evaluate(f"A3.view({x},{z},{yaw},{pitch})")
        await pg.wait_for_timeout(900)
        await pg.screenshot(path=OUT / f"{name}.png")
    await pg.evaluate("A3.view(2.7,6.3,.25,-.08);A3.setTod('eve')")
    await pg.wait_for_timeout(1200)
    await pg.screenshot(path=OUT / "real_wieczor.png")
    await pg.evaluate("A3.setTod('day')")
    await pg.evaluate("A3.view(1.4,4.9,-0.75,-.12)")
    await pg.select_option("#fridge", "slupek")
    await pg.wait_for_timeout(900)
    await pg.screenshot(path=OUT / "real_kuchnia_slupek.png")
    await pg.select_option("#fridge", "pod")
    await pg.click("#bath button[data-v=dev]")
    await pg.evaluate("A3.view(2.2,.5,-2.45,-.2)")
    await pg.wait_for_timeout(900)
    await pg.screenshot(path=OUT / "real_lazienka_deweloper.png")
    await pg.click("#bath button[data-v=nasz]")
    await pg.click("#mode button[data-m=top]")
    await pg.wait_for_timeout(1200)
    await pg.screenshot(path=OUT / "real_z_gory.png")
    await pg.click("#mode button[data-m=walk]")
    await pg.click("#style button[data-s=mock]")

async def mock(pg):
    await pg.screenshot(path=OUT / "spacer.png")
    await pg.evaluate("A3.view(2.7,10.2,.76,-.1)")
    await pg.wait_for_timeout(500)
    await pg.screenshot(path=OUT / "szopka.png")
    await pg.evaluate("A3.view(1.25,.8,3.1416,-.05)")
    await pg.click("#mode button[data-m=top]")
    await pg.wait_for_timeout(800)
    await pg.screenshot(path=OUT / "z_gory.png")
    await pg.select_option("#fridge", "slupek")
    await pg.wait_for_timeout(800)
    await pg.screenshot(path=OUT / "z_gory_slupek.png")
    await pg.select_option("#fridge", "pod")
    await pg.select_option("#rtv", "w2x60b")
    await pg.wait_for_timeout(800)
    await pg.screenshot(path=OUT / "z_gory_rtv_bez_gornych.png")
    await pg.select_option("#rtv", "w2x60")
    await pg.click("#bath button[data-v=dev]")
    await pg.wait_for_timeout(800)
    await pg.screenshot(path=OUT / "z_gory_deweloper.png")
    await pg.click("#bath button[data-v=nasz]")
    await pg.click("#mode button[data-m=walk]")

asyncio.run(main())
