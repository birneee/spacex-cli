import datetime
import requests
import json
import objectpath


def main():
    print("Upcoming SpaceX Launches")
    response = requests.get("https://api.spacexdata.com/v3/launches/upcoming")
    if response.status_code != 200:
        raise ConnectionError("Unable to get launch data")
    launches = json.loads(response.content)
    title_length = calculate_title_length(launches)
    for launch in launches:
        print_launch(launch, title_length)


def print_launch(launch, title_length):
    mission_name = launch["mission_name"]
    print_title(mission_name, title_length)
    print_info("Rocket", launch["rocket"]["rocket_name"])
    print_launch_date(launch)
    print_info("Launch Site", launch["launch_site"]["site_name_long"])
    print_info("Number", str(launch["flight_number"]))
    print_customers(launch)
    print_payload(launch)
    print()


def print_customers(launch):
    customers = list(objectpath.Tree(launch).execute("$.rocket..customers.*"))
    if customers.__len__() == 1:
        print_info("Customer", customers[0])
    elif customers.__len__() > 1:
        print_info("Customers", ", ".join(customers))


def print_payload(launch):
    payload = list(objectpath.Tree(launch).execute("$.rocket..payload_type"))
    print_info("Payload", ", ".join(payload))


def print_launch_date(launch):
    launch_date = datetime.datetime.strptime(launch["launch_date_utc"], "%Y-%m-%dT%H:%M:%S.%fZ")
    precision = launch["tentative_max_precision"]
    date_format = "{:%d, %b %Y %H:%M:%S} (UTC)"
    if precision == "month":
        date_format = "{:%b %Y}"
    elif precision == "day":
        date_format = "{:%d, %b %Y}"
    elif precision == "quarter":
        date_format = ordinal(quarter_by_date(launch_date)) + " quarter {:%Y}"
    print_info("Launch Date", date_format.format(launch_date))


def quarter_by_date(date: datetime):
    return (date.month - 1) // 3 + 1


def ordinal(n):
    return "%d%s" % (n, "tsnrhtdd"[(n / 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])


def calculate_title_length(launches):
    length = 80
    for launch in launches:
        title: str = launch["mission_name"]
        tmp = len(title) + 10
        if tmp > length:
            length = tmp
    return length


def print_info(key: str, value: str):
    print(key.ljust(14, ' ') + value)


def print_title(title, length):
    print("- {} ".format(title).ljust(length, '-'))


main()
