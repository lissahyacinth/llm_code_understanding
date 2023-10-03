import numpy as np
import pandas as pd
from pandas.core.nanops import nanmean as pd_nanmean
from statsmodels.tools.validation import PandasWrapper, array_like
from statsmodels.tsa.filters.filtertools import convolution_filter
from statsmodels.tsa.stl._stl import STL
from statsmodels.tsa.stl.mstl import MSTL
from statsmodels.tsa.tsatools import freq_to_period


def modify_series(
    x,
    model="additive",
    filt=None,
    period=None,
    two_sided=True,
    extrapolate_trend=0,
):
    pfreq = period
    pw = PandasWrapper(x)
    if period is None:
        pfreq = getattr(getattr(x, "index", None), "inferred_freq", None)

    x = array_like(x, "x", maxdim=2)
    nobs = len(x)

    if not np.all(np.isfinite(x)):
        raise ValueError("This function does not handle missing values")
    if model.startswith("m"):
        if np.any(x <= 0):
            raise ValueError(
                "Multiplicative seasonality is not appropriate "
                "for zero and negative values"
            )

    if period is None:
        if pfreq is not None:
            pfreq = freq_to_period(pfreq)
            period = pfreq
        else:
            raise ValueError(
                "You must specify a period or x must be a pandas object with "
                "a PeriodIndex or a DatetimeIndex with a freq not set to None"
            )
    if x.shape[0] < 2 * pfreq:
        raise ValueError(
            f"x must have 2 complete cycles requires {2 * pfreq} "
            f"observations. x only has {x.shape[0]} observation(s)"
        )

    if filt is None:
        if period % 2 == 0:  # split weights at ends
            filt = np.array([0.5] + [1] * (period - 1) + [0.5]) / period
        else:
            filt = np.repeat(1.0 / period, period)

    nsides = int(two_sided) + 1
    trend = convolution_filter(x, filt, nsides)

    if extrapolate_trend == "freq":
        extrapolate_trend = period - 1

    if extrapolate_trend > 0:
        trend = _extrapolate_trend(trend, extrapolate_trend + 1)

    if model.startswith("m"):
        detrended = x / trend
    else:
        detrended = x - trend

    period_averages = seasonal_mean(detrended, period)

    if model.startswith("m"):
        period_averages /= np.mean(period_averages, axis=0)
    else:
        period_averages -= np.mean(period_averages, axis=0)

    seasonal = np.tile(period_averages.T, nobs // period + 1).T[:nobs]

    if model.startswith("m"):
        resid = x / seasonal / trend
    else:
        resid = detrended - seasonal

    results = []
    for s, name in zip(
        (seasonal, trend, resid, x), ("seasonal", "trend", "resid", None)
    ):
        results.append(pw.wrap(s.squeeze(), columns=name))
    return Result(
        seasonal=results[0],
        trend=results[1],
        resid=results[2],
        observed=results[3],
    )
