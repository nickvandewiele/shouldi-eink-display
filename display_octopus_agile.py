#!/usr/bin/python3
import sys
import os
import datetime
import requests
import matplotlib.pyplot as plt
import io
from PIL import ImageOps, Image, ImageFont, ImageDraw
from inky.auto import auto
import pandas as pd
from pandas.io.json import json_normalize
import matplotlib.dates as mdates

if os.path.exists("lib"):
    sys.path.append("lib")
import fonts


def main():
    inky_display = auto()
    inky_display.set_border(inky_display.WHITE)
    BASE_URL = "https://api.octopus.energy/v1/products/AGILE-18-02-21/electricity-tariffs/E-1R-AGILE-18-02-21-C/standard-unit-rates/"
    params = {}
    params["period_from"] = (
        datetime.datetime.now()
        .replace(hour=0, minute=0, second=0, microsecond=0)
        .strftime("%Y-%m-%dT%H:%MZ")
    )
    params["period_to"] = (
        datetime.datetime.now()
        .replace(hour=23, minute=0, second=0, microsecond=0)
        .strftime("%Y-%m-%dT%H:%MZ")
    )
    response_forecast = requests.request(method="GET", url=BASE_URL, params=params)
    response = response_forecast.json()

    if response_forecast.status_code != 200:
        print("Error")

    x = []
    y = []

    df = json_normalize(response["results"])
    df["valid_from"] = pd.to_datetime(df["valid_from"])
    df = df.set_index("valid_from").resample("60min").mean().reset_index("valid_from")

    plt.style.use("ggplot")
    COLOR = "black"
    plt.rcParams["text.color"] = COLOR
    plt.rcParams["xtick.color"] = COLOR
    plt.rcParams["ytick.color"] = COLOR
    plt.rcParams["axes.grid"] = False
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["font.sans-serif"] = ["Arial"]
    plt.rcParams["axes.spines.left"] = False
    plt.rcParams["axes.spines.right"] = False
    plt.rcParams["axes.spines.top"] = False
    plt.rcParams["axes.spines.bottom"] = False
    plt.rcParams.update({"font.size": 13})
    x_pos = [i for i, _ in enumerate(x)]
    plt.figure(frameon=False)
    plt.tight_layout()
    figure = plt.gcf()  # get current figure
    ax = plt.gca()
    df.plot(
        kind="bar",
        x="valid_from",
        y="value_inc_vat",
        ax=ax,
        color="black",
        legend=False,
        figsize=(4.75, 2.8),
    )
    f = lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S").strftime("%H")
    ax.set_xticklabels(
        labels=[f(x.get_text()) for x in ax.get_xticklabels()], rotation=0
    )
    ax.locator_params(nbins=4, axis="x")
    plt.savefig("energy.png", transparent=True, dpi=100)
    img = Image.new("P", inky_display.resolution)
    draw = ImageDraw.Draw(img)
    plot = Image.open("energy.png")
    img.paste(plot, (-28, 26))
    draw.rectangle([(0, 0), (400, 55)], inky_display.BLACK)
    draw.text((10, 10), "Agile tariff ", inky_display.WHITE, font=fonts.raleway_reg_30)
    draw.text((160, 20), "p/kWh ", inky_display.WHITE, font=fonts.raleway_reg_20)
    draw.text(
        (300, 10),
        datetime.datetime.now().strftime("%d/%m"),
        inky_display.WHITE,
        font=fonts.raleway_bold_30,
    )
    inky_display.set_image(img)
    inky_display.show()


if __name__ == "__main__":
    main()