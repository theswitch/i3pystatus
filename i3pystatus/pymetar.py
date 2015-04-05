from i3pystatus import IntervalModule
import pymetar
from i3pystatus.core.util import internet, require

class Metar(IntervalModule):
    interval = 10 * 60 # 10 min refresh interval

    settings = (
        "location",
        "colourise",
        "format"
    )
    required = ("location",)

    format = "{temp}"
    colourise = False
    colour_icons = {
        "sun": (u"\uf30d", "#ffcc00"),
        "cloud": (u"\uf313", "#f8f8ff"),
        "suncloud": (u"\uf302", "#f8f8ff"),
        "rain": (u"\uf319", "#cbd2c0"),
        "fog": (u"\uf314", "#f8f8ff"),
        "default": ("", None),
    }

    def init(self):
        self.fetcher = pymetar.ReportFetcher(self.location)
        self.parser = pymetar.ReportParser()

    @require(internet)
    def run(self):
        report = self.fetcher.FetchReport()
        self.parser.ParseReport(report)

        current_temp = report.temp
        colour = None

        if self.colourise:
            icon, colour = self.colour_icons.get(report.pixmap, self.colour_icons["default"])
            current_temp = "{t}°C {i}".format(t=current_temp, i=icon)

        self.output = {
            "full_text": self.format.format(temp=current_temp),
            "color": colour
        }
