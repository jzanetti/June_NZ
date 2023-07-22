import pandas as pd
from pytrends import dailydata
from pytrends.request import TrendReq


def get_google_trends_data(keyword, timeframe, geo):
    # pytrends = TrendReq(hl="en-US", tz=120)  # Set the timezone to match New Zealand (UTC+12:00)

    # pytrends.build_payload(kw_list=[keyword])

    df = dailydata.get_daily_data("measles", 2019, 1, 2019, 2, geo="NZ", wait_time=15.0)

    print(df)
    # pytrends.interest_by_region(resolution="REGION", inc_low_vol=True, inc_geo_code=True)
    raise Exception("12321")

    pytrends.build_payload(kw_list=[keyword], timeframe=timeframe, geo=geo)
    time_df = pytrends.interest_over_time(resolution="REGION", inc_low_vol=True, inc_geo_code=True)
    data = pytrends.interest_by_region(resolution="REGION", inc_low_vol=True, inc_geo_code=True)

    return data


def main():
    keyword = "measles"
    timeframe = "2018-01-01 2019-12-31"
    geo = "NZ"  # Geo code for New Zealand

    data = get_google_trends_data(keyword, timeframe, geo)
    data.reset_index(inplace=True)
    data.columns = ["Region", "Search Interest", "Geo Code"]

    print(data)


if __name__ == "__main__":
    main()
