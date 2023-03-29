from collections import OrderedDict
from typing import Optional


class FluxQueryBuilder:
    """Class that helps building a flux query for influxdb"""

    def __init__(self, bucket: str):
        self.bucket: str = bucket
        self.start: Optional[str] = None
        self.stop: Optional[str] = None
        self.filters: OrderedDict = OrderedDict()

    def range(self, start: str, stop: Optional[str] = None) -> "FluxQueryBuilder":
        self.start = start
        self.stop = stop
        return self

    def filter(self, on: str, what: str) -> "FluxQueryBuilder":
        self.filters[on] = what
        return self

    def build(self) -> str:
        query = f'from(bucket: "{self.bucket}")'
        if self.start is None:
            raise ValueError("You need to provide a range")
        start_str = f"start: {self.start}"
        stop_str = f", stop: {self.stop}" if self.stop is not None else ""
        ident = " " * 4
        query += "\n"
        query += ident + f"|> range({start_str} {stop_str})"
        for on, what in self.filters.items():
            query += "\n"
            query += ident + f'|> filter(fn: (r) => r["{on}"] == "{what}")'
        return query


def main():
    query = (
        FluxQueryBuilder("My bucket")
        .range(start="5m", stop="2m")
        .filter(on="_measurement", what="my_var")
        .build()
    )
    print(query)


if __name__ == "__main__":
    main()
