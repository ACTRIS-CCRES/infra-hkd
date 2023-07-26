import requests
import dataclasses
from typing import Dict, Optional
import toml
import pathlib

RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"
GREEN_DOT = f"{GREEN}⬤{RESET}"
RED_DOT = f"{RED}⬤{RESET}"


def download_csv(url: str, to: str) -> None:
    response = requests.get(url)
    if response.status_code != 200:
        print(response.content)
        print(response.status_code)
        print(f" {RED_DOT} Something went wrong with the spreadsheet {url}")
    with open(to, "w") as f:
        f.write(response.content.decode("utf-8"))


def download(config: str, output_folder: str):
    _output_folder = pathlib.Path(output_folder)
    toml_conf = toml.load(config)
    for instrument_type, instruments in toml_conf.items():
        for instrument_name, instrument_config in instruments.items():
            print(f"Treating [{instrument_type}].[{instrument_name}] ...")
            url: Optional[str] = instrument_config.get("url")
            if url is None:
                print(f'Cannot find "url" field in [{instrument_type}].[{instrument_name}]')
                continue
            url = url.strip()
            output_file = (
                _output_folder.absolute() / f"{instrument_type}" / f"{instrument_name}.csv"
            )
            output_file.parent.mkdir(parents=True, exist_ok=True)
            download_csv(url, str(output_file))
            print(f"{GREEN_DOT} Spreadsheet {url} saved in {output_file}")


def main():
    download("./config.toml", "./csv_export/")


if __name__ == "__main__":
    main()
