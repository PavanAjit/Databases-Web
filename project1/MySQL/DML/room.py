import csv

def read_rooms(fname):
  with open(fname) as f:
    data = csv.reader(f,delimiter=',')
    for row in data:
      bcode = row[0].strip()
      rnumber = row[1].strip()
      cap = row[2].strip()
      layout = row[3].strip()
      media = row[4].strip()
      type = row[6].strip()
      dept = row[7].strip()
      print("insert into ROOM values ("+ \
        "'"+bcode+"',"+ \
        "'"+rnumber+"',"+ \
        cap+","+ \
        "'"+layout+"',"+ \
        "'"+type+"',"+ \
        "'"+dept+"');")
      ms = media.split(";")
      for m in ms:
        mstrip = m.strip()
        if mstrip != "":
          print("insert into ROOMMEDIA values ('"+bcode+"','"+rnumber+"','"+mstrip+"');")

def main():
  read_rooms("classrooms.csv")

main()
