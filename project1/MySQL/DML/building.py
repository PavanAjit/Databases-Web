import csv

def read_building(fname):
  with open(fname) as f:
    data = csv.reader(f,delimiter=',')
    for row in data:
      print("insert into BUILDING values ('"+row[0].strip()+"','"+row[1].strip()+"');")

def main():
  read_building("building-codes.csv")

main()
