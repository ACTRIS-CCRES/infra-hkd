# Download spreadsheet

In order to download a spreadsheet from google we use the following endpoint : 

```
https://docs.google.com/spreadsheets/d/{self.id}/gviz/tq?tqx=out:{self.what}&gid={self.gid}
```

Helper script is inside `spreadsheet/`, you need to fill the `config.example.toml` and rename it to `config.toml`.


Each section is read and downloaded

Config of toml file : 

| Attribute   | Type   | Comment                            |
|-------------|--------|------------------------------------|
| id          | str    | Id of the spreadsheet              |
| gid         | number | Number of the sheet                |
| export_type | str    | Type of export you want (csv, pdf) |
| output_file | str    | Where to save the file             |