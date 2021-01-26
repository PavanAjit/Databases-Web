import sys
import graphene
import mysql.connector as mysql

class User(graphene.ObjectType):
    username=graphene.String()
    password=graphene.String()
    database=graphene.String()

class Tables(graphene.ObjectType):
    tablename=graphene.String()

class Building(graphene.ObjectType):
    bcode = graphene.String()
    bname = graphene.String()

class Media(graphene.ObjectType):
    mcode = graphene.String()
    description = graphene.String()

class Room(graphene.ObjectType):
    bldg = graphene.String()
    rnumber = graphene.String()
    cap = graphene.Int()
    layout = graphene.String()
    rtype = graphene.String()
    dept = graphene.String()
    media = graphene.List(Media)

class Queries(graphene.ObjectType):
    tables=graphene.List(Tables,username=graphene.String(),password=graphene.String(),database=graphene.String())
    # tables=graphene.List(Tables)
    buildings = graphene.List(Building)
    media = graphene.List(Media)
    rooms = graphene.List(Room,building=graphene.String())
    room = graphene.Field(Room,building=graphene.String(),
                               rno=graphene.String())
    roommedia = graphene.List(Media,building=graphene.String(),
                                    rno=graphene.String())
    roomscap = graphene.List(Room,cap_lower=graphene.Int(),
                                  cap_upper=graphene.Int())

    def resolve_tables(self,info,username,password,database):
    # def resolve_tables(self,info):
        db = mysql.connect(
            host="localhost",
            database=str(database),
            user=str(username),
            passwd=str(password),
            auth_plugin='mysql_native_password'
        )
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema ='"+db.database+"'"
        cursor = db.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        db.close()
        #if len(records) == 0:
        #  return ??
        tables = []
        for record in records:
            tables.append(Tables(tablename=record[0]))
        return tables
        
    def resolve_buildings(self, info):
        db = mysql.connect(
            host="localhost",
            database="project1",
            user="root",
            passwd="root123",
            auth_plugin='mysql_native_password'
        )
        query = "select bcode,bname from BUILDING "
        cursor = db.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        db.close()
        #if len(records) == 0:
        #  return ??
        buildings = []
        for record in records:
            buildings.append(Building(bcode=record[0],bname=record[1]))
        return buildings

    def resolve_media(self, info):
        db = mysql.connect(
            host="localhost",
            database="project1",
            user="root",
            passwd="root123",
            auth_plugin='mysql_native_password'
        )
        query = "select mcode,description from MEDIA "
        cursor = db.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        db.close()
        #if len(records) == 0:
        #  return ??
        media = []
        for record in records:
            media.append(Media(mcode=record[0],description=record[1]))
        return media

    def resolve_rooms(self, info, building):
        db = mysql.connect(
            host="localhost",
            database="project1",
            user="root",
            passwd="root123",
            auth_plugin='mysql_native_password'
        )
        query = "select rnumber from ROOM where ROOM.bcode='"+building+"'"
        cursor = db.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        db.close()
        #if len(records) == 0:
        #    abort(404)
        rooms = []
        for record in records:
            rooms.append(Room(bldg=building,rnumber=record[0],
                              cap=0,layout="",rtype="",dept=""))
        return rooms

    def resolve_room(self, info, building, rno):
        db = mysql.connect(
            host="localhost",
            database="project1",
            user="root",
            passwd="root123",
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()
        query1 = "select cap,layout,type,dept,bname from ROOM,BUILDING "+ \
                 "where ROOM.bcode='"+building+"' and ROOM.rnumber='"+rno+ \
                 "' and ROOM.bcode=BUILDING.bcode"
        cursor.execute(query1)
        records1 = cursor.fetchall()
        query2 = "select MEDIA.mcode,description "+ \
                "from ROOM,ROOMMEDIA,MEDIA "+ \
                "where ROOM.bcode='"+building+"' and "+ \
                "ROOM.rnumber='"+rno+"' and "+ \
                "ROOM.bcode=ROOMMEDIA.bcode and "+ \
                "ROOM.rnumber=ROOMMEDIA.rnumber and "+ \
                "ROOMMEDIA.mcode=MEDIA.mcode"
        cursor.execute(query2)
        records2 = cursor.fetchall()
        cursor.close()
        db.close()
        if len(records1) == 0:
          return None
        media = []
        for record2 in records2:
            media.append(Media(mcode=record2[0],description=record2[1]))
        return Room(
            bldg=records1[0][4]+" ("+building+")",
            rnumber=rno,
            cap=records1[0][0],
            layout=records1[0][1],
            rtype=records1[0][2],
            dept=records1[0][3],
            media=media
        )

    def resolve_roommedia(self, info, building, rno):
        db = mysql.connect(
            host="localhost",
            database="project1",
            user="root",
            passwd="root123",
            auth_plugin='mysql_native_password'
        )
        query = "select MEDIA.mcode,description "+ \
                "from ROOM,ROOMMEDIA,MEDIA "+ \
                "where ROOM.bcode='"+building+"' and "+ \
                "ROOM.rnumber='"+rno+"' and "+ \
                "ROOM.bcode=ROOMMEDIA.bcode and "+ \
                "ROOM.rnumber=ROOMMEDIA.rnumber and "+ \
                "ROOMMEDIA.mcode=MEDIA.mcode"
        cursor = db.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        db.close()
        #if len(records) == 0:
        #  return ??
        media = []
        for record in records:
            media.append(Media(mcode=record[0],description=record[1]))
        return media

    def resolve_roomscap(self, info, cap_lower, cap_upper):
        db = mysql.connect(
            host="localhost",
            database="project1",
            user="root",
            passwd="root123",
            auth_plugin='mysql_native_password'
        )
        query = "select bcode, rnumber, cap from ROOM where cap >= "+str(cap_lower) + \
                " and cap <= "+str(cap_upper)
        cursor = db.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        db.close()
        rooms = []
        for record in records:
            rooms.append(Room(bldg=record[0],rnumber=record[1],
                              cap=record[2],layout="",rtype="",dept=""))
        return rooms

########### MUTATIONS ################
class CreateBuilding(graphene.Mutation):
    # define output of mutation here
    ok = graphene.Boolean()
    bcode = graphene.String()
    bname = graphene.String()
    # define data to be sent to server as part of insert
    class Arguments:
        bcode = graphene.String()
        bname = graphene.String()
    # code to modify database
    def mutate(self, info, bcode, bname):
        db = mysql.connect(
            host="localhost",
            database="project1",
            user="root",
            passwd="root123",
            auth_plugin='mysql_native_password'
        )
        sql = "insert into BUILDING values ('"+bcode+"','"+bname+"')"
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
            cursor.close()
            db.close()
            return CreateBuilding(ok=True,bcode=bcode,bname=bname)
        except Exception as e:
            db.rollback()
            cursor.close()
            db.close()
            return CreateBuilding(ok=False,bcode="",bname="")

class CreateRoom(graphene.Mutation):
    # define output of mutation here
    ok = graphene.Boolean()
    bldg = graphene.String()
    rnumber = graphene.String()
    # define data to be sent to server as part of insert
    class Arguments:
        bldg = graphene.String()
        rnumber = graphene.String()
        cap = graphene.Int()
        layout = graphene.String()
        rtype = graphene.String()
        dept = graphene.String()
        media = graphene.List(graphene.String)
    # code to modify database
    def mutate(self, info, bldg, rnumber, cap, layout, rtype, dept, media):
        db = mysql.connect(
            host="localhost",
            database="project1",
            user="root",
            passwd="root123",
            auth_plugin='mysql_native_password'
        )
        #sql = "insert into ROOM (bcode,rnumber,cap,layout,type,dept) " + \
        #      "values (%s,%s,%d,%s,%s,%s)"
        #vals = (bldg,rnumber,cap,layout,rtype,dept)
        sql = "insert into ROOM values ('"+bldg+"','"+rnumber+ \
              "',"+str(cap)+",'"+layout+"','"+rtype+"','"+dept+"')"
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            for m in media:
                sql = "insert into ROOMMEDIA values ('"+bldg+"','"+ \
                      rnumber+"','"+m+"')"
                values = (bldg,rnumber,m)
                cursor.execute(sql)
            db.commit()
            cursor.close()
            db.close()
            #print(sql)
            return CreateRoom(ok=True,bldg=bldg,rnumber=rnumber)
        except Exception as e:
            #print(sql)
            #print(e)
            db.rollback()
            cursor.close()
            db.close()
            return CreateRoom(ok=False,bldg="",rnumber="")

class UpdateRoomCapacity(graphene.Mutation):
    # define output of mutation here
    ok = graphene.Boolean()
    bldg = graphene.String()
    rnumber = graphene.String()
    cap = graphene.Int()
    # define data to be sent to server as part of insert
    class Arguments:
        bldg = graphene.String()
        rnumber = graphene.String()
        cap = graphene.Int()
    # code to modify database
    def mutate(self, info, bldg, rnumber, cap):
        db = mysql.connect(
            host="localhost",
            database="project1",
            user="root",
            passwd="root123",
            auth_plugin='mysql_native_password'
        )
        sql = "update ROOM set cap = "+str(cap)+" where "+ \
              "bcode = '"+bldg+"' and rnumber = '"+rnumber+"'"
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
            cursor.close()
            db.close()
            #print(sql)
            return UpdateRoomCapacity(ok=True,bldg=bldg,rnumber=rnumber,cap=cap)
        except Exception as e:
            #print(sql)
            #print(e)
            db.rollback()
            cursor.close()
            db.close()
            return UpdateRoomCapacity(ok=False,bldg="",rnumber="",cap=0)

class DeleteRoom(graphene.Mutation):
    # define output of mutation here
    ok = graphene.Boolean()
    bldg = graphene.String()
    rnumber = graphene.String()
    # define data to be sent to server as part of insert
    class Arguments:
        bldg = graphene.String()
        rnumber = graphene.String()
    # code to modify database
    def mutate(self, info, bldg, rnumber):
        db = mysql.connect(
            host="localhost",
            database="project1",
            user="root",
            passwd="root123",
            auth_plugin='mysql_native_password'
        )
        sql1 = "delete from ROOMMEDIA"+" where "+ \
               "bcode = '"+bldg+"' and rnumber = '"+rnumber+"'"
        sql2 = "delete from ROOM"+" where "+ \
               "bcode = '"+bldg+"' and rnumber = '"+rnumber+"'"
        cursor = db.cursor()
        try:
            cursor.execute(sql1)
            cursor.execute(sql2)
            db.commit()
            cursor.close()
            db.close()
            #print(sql)
            return DeleteRoom(ok=True,bldg=bldg,rnumber=rnumber)
        except Exception as e:
            #print(sql)
            #print(e)
            db.rollback()
            cursor.close()
            db.close()
            return DeleteRoom(ok=False,bldg="",rnumber="")
#class Mutations(graphene.ObjectType):
#    create_building = CreateBuilding.Field()
#    create_room = CreateRoom.Field()
class Mutations(graphene.ObjectType):
    create_building = CreateBuilding.Field()
    create_room = CreateRoom.Field()
    update_room_capacity = UpdateRoomCapacity.Field()
    delete_room = DeleteRoom.Field()

#class Mutation(AllMutations):
#    pass

########## SCHEMA ##########

schema = graphene.Schema(query=Queries,mutation=Mutations)

########## CLIENT SIDE QUERIES/MUTATIONS #########
# query = """
# {
#   buildings {
#     bcode
#     bname
#   }
# }
# """
# result = schema.execute(query)
# print(result.data['buildings'])

# query = """
# {
#   media {
#     mcode
#     description
#   }
# }
# """
# result = schema.execute(query)
# print(result.data['media'])

# query = """
# {
#   rooms (building: "CLSO") {
#       rnumber
#   }
# }
# """
# result = schema.execute(query)
# print(result.data['rooms'])

#query = """
# {
#   room (building: "CLSO", rno: "206") {
#       cap
#     	layout
#     	rtype
#     	dept
#       media {
#         mcode
#         description
#       }
#   }
#}
#"""
#result = schema.execute(query)
#print(result.data['room'])

#query = """
#{
#  roommedia (building: "CLSO", rno: "206") {
#   mcode
#   description
#  }
#}
#"""
#result = schema.execute(query)
#print(result.data)
#print(result.data['roommedia'])

# query = """
# mutation {
#   createBuilding(bcode:"2PP", bname:"2 Park Place") {
#     id
#     bcode
#     bname
#   }
# }
# """
# result = schema.execute(query)
# print(result.data)
#
#query = """
#mutation {
#  createRoom (bldg:"CLSO",rnumber:"9999",cap:44,
#              layout:"Round Tables",rtype:"G",dept:"",
#              media:["IWS","LAC"]) {
#    ok
#    bldg
#    rnumber
# }
#}
#"""
# result = schema.execute(query)
# print(result.data)
#
# update room capacity
#mutation {
#  updateRoomCapacity (bldg:"CLSO", rnumber:"206",cap:199) {
#    ok
#    bldg
# }
#}
#
#mutation {
#  deleteRoom(bldg:"CLSO", rnumber:"9999") {
#    ok
#    bldg
#    rnumber
#  }
#}
#