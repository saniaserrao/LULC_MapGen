import os
from PIL import Image
from selenium import webdriver


def export_lulc(map_dir, roi, map):
    dir = os.path.join(map_dir, roi)

    os.makedirs(dir, exist_ok=True)

    map_html_path = os.path.join(dir, "lulc_map.html")
    screenshot_path = os.path.join(dir, "lulc_map_screenshot.png")
    output_tiff_path = os.path.join(dir, "lulc_map" + roi + ".tiff")
    map.save(map_html_path)

    if not os.path.exists(map_html_path):
        print(f"Error: Map HTML file does not exist at {map_html_path}")
    else:
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")

            window_width = 1920
            window_height = 1080
            options.add_argument(f"--window-size={window_width},{window_height}")

            driver = webdriver.Chrome(options=options)
            driver.get(f"file://{os.path.abspath(map_html_path)}")

            driver.save_screenshot(screenshot_path)
            driver.quit()

            with Image.open(screenshot_path) as img:
                img.convert("RGB").save(output_tiff_path, format="TIFF")

            os.remove(screenshot_path)
            os.remove(map_html_path)

            print(f"TIFF file saved as {output_tiff_path}")

        except Exception as e:
            print(f"Error occurred: {e}")
