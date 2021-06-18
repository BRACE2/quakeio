import re

import numpy as np

from quakeio.core import GroundMotionSeries
from quakeio.utils.parseutils import open_quake

RE_TIME_STEP = re.compile(r"DT=\s+(.*)SEC")


def read_nga(read_file, *args, **kwds):
    with open_quake(read_file, "r") as f:
        header = [next(f) for _ in range(4)]
    dt = float(RE_TIME_STEP.search(header[-1]).group(1).strip())
    series_type = header[-2][:5].lower()
    accel = np.genfromtxt(read_file, skip_header=4, skip_footer=1).flatten()
    return GroundMotionSeries(
        accel, dict(time_step=dt, series_type=series_type, units="g")
    )


FILE_TYPES = {
    "nga.at2": {
        "read": read_nga,
        "type": GroundMotionSeries,
    }
}
