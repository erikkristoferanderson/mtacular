# this is a script to collect data from mta
# the intention is to call this from jupyter notebooks

import pandas as pd

# Get data from MTA website according to variables **years** and **months**.
# saves data to ../../data/raw/


import datetime
from pathlib import Path


def get_data(years, months):
    filenames = generate_filenames(years, months)
    for filename in filenames:
        download_one_file(filename)
        print(f"downloaded {filename}")

def generate_filenames(years, months):
    filenames = []
    final = datetime.date(2019, 12, 28)
    file_delta = datetime.timedelta(days=7)
    current = final
    while current.year >= min(years):
        if current.year in years and current.month in months:
            filenames.append(current.strftime('turnstile_%y%m%d.txt'))
        current -= file_delta
    return filenames


def download_one_file(filename):
    import urllib.request
    base_url = 'http://web.mta.info/developers/data/nyct/turnstile/'
    url = base_url + filename
    base_data_path = "../../data/raw/"
    file_path = base_data_path + filename
    urllib.request.urlretrieve(url, file_path)


if __name__ == "__main__":
    years_input = [2018, 2019]
    years_input = [2019]
    months_input = [3, 4]

    print(f"running {str(Path(__file__))}")
    get_data(years_input, months_input)
    print("script complete")

