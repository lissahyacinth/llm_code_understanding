from darts.models.filtering.filtering_model import FilteringModel
from darts.timeseries import TimeSeries


class Filter(FilteringModel):
    """
    A simple moving average filter. Works on deterministic and stochastic series.
    """

    def __init__(self, window: int, centered: bool = True):
        super().__init__()
        self.window = window
        self.centered = centered

    def filter(self, series: TimeSeries):
        transformation = {
            "function": "mean",
            "mode": "rolling",
            "window": self.window,
            "center": self.centered,
            "min_periods": 1,
        }

        return series.window_transform(
            transforms=transformation, forecasting_safe=False
        )
