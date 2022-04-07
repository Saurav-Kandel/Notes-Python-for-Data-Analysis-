import csv

with open('hour.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
