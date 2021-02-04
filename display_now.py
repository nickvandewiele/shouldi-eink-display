#!/usr/bin/python3
import sys
import os
import datetime
from PIL import ImageOps, Image, ImageFont, ImageDraw
from inky.auto import auto

imgdir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.relpath(__file__))), "imgdir"
)

if os.path.exists("lib"):
    sys.path.append("lib")
from carbonintensityforecast import CarbonIntensityForecastGB
import fonts


def main():

    inky_display = auto()

    img = Image.new("P", inky_display.resolution)
    draw = ImageDraw.Draw(img)
    template = Image.open(os.path.join(imgdir, "template.png"))
    img.paste(template, (0, 0))

    carbon_intensity = CarbonIntensityForecastGB(postcode="N1")
    intensity_data = carbon_intensity.now()
    total_value = carbon_intensity.now("total")

    total = 0

    for value in intensity_data:
        percentage_value = int(round(value["perc"]))
        coordsx = 95
        coordsy = 0
        total += percentage_value
        if value["fuel"] == "wind":
            coordsy = 10
        if value["fuel"] == "hydro":
            coordsy = 115
        if value["fuel"] == "solar":
            coordsy = 215
        draw.text(
            (coordsx, coordsy),
            str(percentage_value) + "%",
            inky_display.BLACK,
            font=fonts.raleway_reg_50,
        )

    rhs_start = 215
    draw.text((rhs_start, 10), "London", inky_display.BLACK, font=fonts.raleway_reg_50)
    draw.text((rhs_start, 70), "N1", inky_display.BLACK, font=fonts.raleway_reg_50)
    draw.text(
        (rhs_start, 135), "Total", inky_display.BLACK, font=fonts.raleway_light_25
    )
    draw.text(
        (rhs_start, 160), "renewable", inky_display.BLACK, font=fonts.raleway_light_25
    )
    draw.text(
        (rhs_start, 190), "generation", inky_display.BLACK, font=fonts.raleway_light_25
    )
    draw.text(
        (rhs_start, 215),
        str(total) + "%",
        inky_display.BLACK,
        font=fonts.raleway_reg_50,
    )

    date_now = datetime.datetime.now()
    draw.text(
        (215, 280),
        "Updated :" + date_now.strftime("%H:%M"),
        inky_display.BLACK,
        font=fonts.raleway_light_13,
    )

    inky_display.set_image(img)
    inky_display.show()


if __name__ == "__main__":
    main()
