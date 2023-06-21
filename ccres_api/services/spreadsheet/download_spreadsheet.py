import requests
import dataclasses
from typing import Dict
import toml

@dataclasses.dataclass
class GoogleSpreadSheet:
    id:str
    gid:int
    export_type: str = "csv"
    
    def download(self, to:str)-> None:
        response = requests.get(f"https://docs.google.com/spreadsheets/d/{self.id}/gviz/tq?tqx=out:{self.export_type}&gid={self.gid}")
        if response.status_code != 200:
            raise ValueError(f"Something went wrong with the spreadsheet {self.id}")
        with open(to, "w") as f:
            f.write(response.content.decode("utf-8"))
        

def main():
    config = toml.load("./config.toml")
    for section, content in config.items():
        spreadsheet = GoogleSpreadSheet(id=content["id"], gid=content["gid"], export_type=content["export_type"])
        spreadsheet.download(content["output_file"])
        print(f"Spreadsheet {section} saved in {content['output_file']}")

if __name__ == "__main__":
    main()