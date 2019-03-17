import datetime

import colorama
import requests
import json
import objectpath
from colorama import Fore, Style


spacex_ascii =  ' ____                      __  __\n' \
                '/ ___| _ __   __ _  ___ ___\\ \\/ /\n' \
                '\\___ \\| \'_ \\ / _` |/ __/ _ \\\\  / \n' \
                ' ___) | |_) | (_| | (_|  __//  \\ \n' \
                '|____/| .__/ \__,_|\\___\\___/_/\\_\\\n' \
                '      |_| '


rocket_text_style = Fore.LIGHTBLUE_EX + Style.BRIGHT

falcon9_ascii = '    / \\    \n' \
                '   | ' + rocket_text_style + 'F' + Style.RESET_ALL + ' |   \n' \
                '   | ' + rocket_text_style + '9' + Style.RESET_ALL + ' |   \n' \
                '    | |    \n' \
                '    | |    \n' \
                '    | |    \n' \
                '    | |    \n' \
                '    | |    \n' \
                '    | |    \n' \
                '    | |    \n' \
                '    | |    \n' \
                '    | |    \n' \
                '    | |    \n'

falcon_heavy_ascii = '    / \\    \n' \
                     '   | ' + rocket_text_style + 'F' + Style.RESET_ALL + ' |   \n' \
                     '   | ' + rocket_text_style + 'H' + Style.RESET_ALL + ' |   \n' \
                     '    | |    \n' \
                     ' / \\| |/ \\ \n' \
                     ' | || || | \n' \
                     ' | || || | \n' \
                     ' | || || | \n' \
                     ' | || || | \n' \
                     ' | || || | \n' \
                     ' | || || | \n' \
                     ' | || || | \n' \
                     ' | || || | \n'


def main():
    colorama.init()
    print(Style.BRIGHT + spacex_ascii + Style.RESET_ALL, end='')
    print(Style.BRIGHT + "UPCOMING LAUNCHES" + Style.RESET_ALL, end="\n\n")
    response = requests.get("https://api.spacexdata.com/v3/launches/upcoming")
    if response.status_code != 200:
        raise ConnectionError("Unable to get launch data")
    launches = json.loads(response.content)
    for launch in launches:
        print_launch(launch)


def print_launch(launch):
    print_launch_with(
        launch["mission_name"],
        launch["rocket"]["rocket_name"],
        get_launch_date_str(launch),
        launch["launch_site"]["site_name_long"],
        str(launch["flight_number"]),
        get_customer_str(launch),
        get_payload_str(launch)
    )


def print_launch_with(mission_name, rocket_name, launch_date, launch_site, number, customer, payload):
    data = [
        ("Mission", Style.BRIGHT + mission_name + Style.RESET_ALL),
        ("Rocket", rocket_name),
        ("Launch Date", launch_date),
        ("Launch Site", launch_site),
        ("Number", number),
        ("Customer", customer),
        ("Payload", payload)
    ]
    ascii_img = falcon_heavy_ascii if rocket_name == "Falcon Heavy" else falcon9_ascii
    for index, item in enumerate(data):
        print("{} {:14} {}".format(ascii_img.splitlines()[index], item[0], item[1]))
    print()


def get_customer_str(launch):
    customers = list(objectpath.Tree(launch).execute("$.rocket..customers.*"))
    return ", ".join(customers)


def get_payload_str(launch):
    payload = list(objectpath.Tree(launch).execute("$.rocket..payload_type"))
    return ", ".join(payload)


def get_launch_date_str(launch):
    launch_date = datetime.datetime.strptime(launch["launch_date_utc"], "%Y-%m-%dT%H:%M:%S.%fZ")
    precision = launch["tentative_max_precision"]
    date_format = "{:%d, %b %Y %H:%M:%S} (UTC)"
    if precision == "hour":
        date_format = "{:%d, %b %Y %H:%M} (UTC)"
    elif precision == "month":
        date_format = "{:%b %Y}"
    elif precision == "day":
        date_format = "{:%d, %b %Y}"
    elif precision == "quarter":
        date_format = ordinal(quarter_by_date(launch_date)) + " quarter {:%Y}"
    return date_format.format(launch_date)


def quarter_by_date(date: datetime):
    return (date.month - 1) // 3 + 1


def ordinal(n):
    return "%d%s" % (n, "tsnrhtdd"[(n / 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])


main()
