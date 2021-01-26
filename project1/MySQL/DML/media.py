import csv

def read_media(fname):
  with open(fname) as f:
    data = csv.reader(f,delimiter=',')
    for row in data:
      print("insert into MEDIA values ('"+row[0].strip()+"','"+row[1].strip()+"');")

def main():
  read_media("media-codes.csv")

main()
