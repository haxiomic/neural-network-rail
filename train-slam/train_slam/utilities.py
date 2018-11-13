import csv
import json

class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            if (hasattr(o, 'json')):
                return o.json()
            raise RuntimeError('No json method')
        except Exception:
            return super().default(o)


def write_csv(name, rows):
    with open('data/{}.csv'.format(name), 'w') as open_file:
        csv_file = csv.writer(open_file)
        csv_file.writerows(rows)

def read_csv(name):
    with open('data/{}.csv'.format(name)) as open_file:
        csv_file = csv.reader(open_file)
        return [row for row in csv_file]

if (__name__ == "__main__"):
    read_csv('london_vic_railstrings')