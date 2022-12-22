import csv

CSV_FILE_NAME = "characters"
CSV_FILE_EXTENSION = "csv"

def writeCsv(data:list[dict], filename = CSV_FILE_NAME):
    if not data or len(data) <= 0:
        # check if data is empty
        return
    # for newline argument check https://stackoverflow.com/questions/3191528/csv-in-python-adding-an-extra-carriage-return-on-windows
    with open(filename+"."+CSV_FILE_EXTENSION, 'w', encoding='utf-8' , newline='') as f:
        # set writer options
        writer = csv.DictWriter(f,
            fieldnames=data[0].keys(),
            delimiter=';',
            quotechar='"',
            escapechar="\\"
        )
        # write header
        writer.writeheader()
        # write data
        writer.writerows(data)
