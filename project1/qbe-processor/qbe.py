import mysql.connector as mysql
import traceback
from graphene import ObjectType, String, List, Schema
import json
import base64


class ColumnEntity(ObjectType):
    table = String()
    column = String()
    datatype = String()


# noinspection PyUnusedLocal,PyBroadException
class Query(ObjectType):
    tables = List(String,
                  user=String(required=True, description="Username for MySQL DB"),
                  passwd=String(required=True, description="Password for MySQL DB"),
                  host=String(default_value="127.0.0.1",
                              description="Host for DB server. Defaults to Localhost"),
                  database=String(required=True, description="Database name"))

    columns = List(ColumnEntity,
                   user=String(required=True, description="Username for MySQL DB"),
                   passwd=String(required=True, description="Password for MySQL DB"),
                   host=String(default_value="127.0.0.1",
                               description="Host for DB server. Defaults to Localhost"),
                   database=String(required=True, description="Database name"))

    qbe = List(String,
               user=String(required=True, description="Username for MySQL DB"),
               passwd=String(required=True, description="Password for MySQL DB"),
               host=String(default_value="127.0.0.1",
                           description="Host for DB server. Defaults to Localhost"),
               database=String(required=True, description="Database name"),
               qbequery=String(required=True, description="Array of entities containing field and value"))

    @staticmethod
    def resolve_tables(parent, info, host, user, passwd, database):
        """ Example Usage
        query {
          tables(user:"bdhol1", passwd:"testpassword", database:"qbe")
        }
        """
        try:
            db = mysql.connect(
                host=host,
                database=database,
                user=user,
                passwd=passwd,
                auth_plugin='mysql_native_password'
            )
            query = f'SELECT distinct table_name from INFORMATION_SCHEMA.COLUMNS ' \
                    f'where table_schema = "{database}"'
            cursor = db.cursor()
            cursor.execute(query)
            records = cursor.fetchall()
            cursor.close()
            tables = list()
            for record in records:
                tables.append(record[0])
            return tables
        except Exception:
            print(str(traceback.format_exc()))
            raise ConnectionRefusedError("Invalid Credentials or Database Name")

    @staticmethod
    def resolve_columns(parent, info, host, user, passwd, database):
        """
        query {
          columns (user: "bdhol1", passwd: "testpassword", database: "qbe", host: "127.0.0.1") {
            column
            datatype
            table
          }
        }
        :return: list of string
        """
        print(info)
        try:
            db = mysql.connect(
                host=host,
                database=database,
                user=user,
                passwd=passwd,
                auth_plugin='mysql_native_password'
            )
            query = f'SELECT table_name, column_name, data_type ' \
                    f'from INFORMATION_SCHEMA.COLUMNS where table_schema = "{database}"'
            cursor = db.cursor()
            cursor.execute(query)
            records = cursor.fetchall()
            cursor.close()
            column_entities = list()
            for record in records:
                column_entities.append(ColumnEntity(table=record[0],
                                                    column=record[1],
                                                    datatype=record[2]))
            return column_entities
        except Exception:
            print(str(traceback.format_exc()))
            raise ConnectionRefusedError("Invalid Credentials or Database Name")

    @staticmethod
    def resolve_qbe(parent, info, host, user, passwd, database, qbequery):
        """
        :return: list of string
        """
        print(info)
        try:
            db = mysql.connect(
                host=host,
                database=database,
                user=user,
                passwd=passwd,
                auth_plugin='mysql_native_password'
            )
            qbequery_decoded = base64.b64decode(qbequery).decode()
            query = qbe2sql(qbedata=qbequery_decoded)
            cursor = db.cursor()
            try:
                cursor.execute(query)
            except Exception:
                raise ValueError("Error executing query [%s] in MySQL" % query)
            records = cursor.fetchall()
            cursor.close()

            result = list()
            # add column headers by splitting query
            result.append(query.replace("distinct", "").
                          split("FROM")[0].split("SELECT")[-1].split(","))

            # add result rows
            for record in records:
                result.append(record)

            return [query, json.dumps(result)]
        except ValueError as ve:
            raise ve
        except Exception:
            raise ConnectionRefusedError("Invalid Credentials or Database Name")


# noinspection PyTypeChecker
schema = Schema(query=Query)


def qbe2sql(qbedata):
    """
    [
        {"field": field, "value": value}

    ]
    :param qbedata:
    :return:
    """
    # Used the following IBM documentation on QBE for a better understanding
    # https://www.ibm.com/support/knowledgecenter/SS9UMF_11.1.0/ugr/ugr/tpc/dsq_start_qbe_query.html
    select_part = "SELECT "
    from_part = "FROM "
    where_part = "WHERE TRUE AND"
    orderby_part = "ORDER BY "

    # Step 1: is to normalize the array of objects to object
    table_fields = list()
    condition_field = ""
    column_fields = list()

    qbe_normalized = dict()
    for entry in json.loads(qbedata):
        qbe_normalized[entry["field"]] = entry["value"]

    for key in qbe_normalized:
        if key == "Condition":
            condition_field = qbe_normalized[key]
        elif "." in key:
            column_fields.append(key)
        else:
            table_fields.append(key)

    # At this point, Condition_field for demo should be _C > 200
    # column_fields should be building_0.bcode, ...etc.
    # table_fields should be building_0

    # Step 2. Look at the values of the table fields and if it is not empty, append
    # those values to the column fields which starts with that same name

    # Implementation of Advanced Feature 1 - Unique
    unq_found = False
    for field in table_fields:
        for entry in qbe_normalized:
            if "UNQ." in qbe_normalized[entry] and field == entry:
                unq_found = True

    if unq_found:
        select_part += "distinct "
    clean_part_of_it(qbe_normalized=qbe_normalized, whatpart="UNQ.")

    # Implementation of Advanced Feature 2 - Order by
    cleanup_list = []
    order_by_dict = dict()
    for entry in qbe_normalized:
        if "AO." in qbe_normalized[entry]:
            temp = qbe_normalized[entry]
            key, cleaning_key = get_ao_do_key(temp[temp.find("AO."):temp.find("AO.")+3])
            cleanup_list.append(cleaning_key)
            order_by_dict[key] = entry
        if "DO." in qbe_normalized[entry]:
            temp = qbe_normalized[entry]
            key, cleaning_key = get_ao_do_key(temp[temp.find("DO."):temp.find("DO.")+3])
            cleanup_list.append(cleaning_key)
            order_by_dict[key] = entry
        if "AO(" in qbe_normalized[entry]:
            temp = qbe_normalized[entry]
            key, cleaning_key = get_ao_do_key(temp[temp.find("AO("):temp.find("AO(")+6])
            cleanup_list.append(cleaning_key)
            order_by_dict[key] = entry
        if "DO(" in qbe_normalized[entry]:
            temp = qbe_normalized[entry]
            key, cleaning_key = get_ao_do_key(temp[temp.find("DO("):temp.find("DO(")+6])
            cleanup_list.append(cleaning_key)
            order_by_dict[key] = entry

    order_by_key_list = list(order_by_dict.keys())
    order_by_key_list.sort()    # ["0-AO", "1-DO"]

    for key in order_by_key_list:
        if "DO" in key:
            orderby_part = orderby_part + order_by_dict[key] + " desc, "
        else:
            orderby_part = orderby_part + order_by_dict[key] + ", "

    if orderby_part[-2:] == ", ":
        orderby_part = orderby_part[:-2]

    for key in cleanup_list:
        clean_part_of_it(qbe_normalized=qbe_normalized, whatpart=key)

    for field in table_fields:
        # field will be building_0
        for entry in qbe_normalized:
            # building_0.bcode,
            if field in entry and field != entry:
                qbe_normalized[entry] = qbe_normalized[field] + qbe_normalized[entry]

    # Removing table entries from qbe_normalized
    for table in table_fields:
        # from_part is "FROM "
        # from_part is "FROM ROOM ROOM_0, BUILDING BUILDING_0,
        from_part += table[:-2] + " " + table + ", "
        qbe_normalized.pop(table)
    from_part = from_part[:-2]           # Removing trailing ,<space>

    # Run clean empties
    qbe_normalized = clean_what_is_told(qbe_normalized=qbe_normalized, tell="")

    # Step 3: form the select part
    for key in qbe_normalized:
        if "P." in qbe_normalized[key]:
            select_part += key + ", "
    select_part = select_part[:-2]

    qbe_normalized = clean_part_of_it(qbe_normalized=qbe_normalized, whatpart="P.")
    qbe_normalized = clean_what_is_told(qbe_normalized=qbe_normalized, tell="")

    for key in qbe_normalized:
        if key == "Condition":
            condition_field = qbe_normalized[key]
        else:
            column_fields.append(key)

    # for e.g. condition _C > 200 => condition_field = ["_C", ">", "200]
    condition_items = condition_field.split(" ")
    for item in condition_items:
        if "_" in item:
            # then its a variable
            matching_entries = list()
            for entry in qbe_normalized:
                if qbe_normalized[entry] == item:
                    matching_entries.append(entry)
            # if matching entries length = 1, then substitute
            if len(matching_entries) == 1:
                condition_field = condition_field.replace(item, matching_entries[0])
            elif len(matching_entries) > 1:
                condition_field = condition_field.replace(item, " = ".join(matching_entries))
            else:
                raise ValueError("Bad QBE Query. Condition variable is missing from the Skeleton")
            qbe_normalized = clean_part_of_it(qbe_normalized=qbe_normalized, whatpart=item)
    if "Condition" in qbe_normalized:
        qbe_normalized.pop("Condition")
    qbe_normalized = clean_what_is_told(qbe_normalized=qbe_normalized, tell="")

    remaining_variable_list = dict()

    for entry in qbe_normalized:
        if qbe_normalized[entry].lstrip().startswith("_"):
            if qbe_normalized[entry] in remaining_variable_list:
                remaining_variable_list[qbe_normalized[entry]].append(entry)
            else:
                remaining_variable_list[qbe_normalized[entry]] = [entry]
        elif qbe_normalized[entry].lstrip().startswith("=") or \
                qbe_normalized[entry].lstrip().startswith("!=") or \
                qbe_normalized[entry].lstrip().startswith(">") or \
                qbe_normalized[entry].lstrip().startswith(">=") or \
                qbe_normalized[entry].lstrip().startswith("<") or \
                qbe_normalized[entry].lstrip().startswith("<=") or \
                qbe_normalized[entry].lstrip().startswith("BETWEEN") or \
                qbe_normalized[entry].lstrip().startswith("IN") or \
                qbe_normalized[entry].lstrip().startswith("LIKE") or \
                qbe_normalized[entry].lstrip().startswith("NOT"):
            condition_field += " AND " + entry + " " + qbe_normalized[entry]
            qbe_normalized[entry] = ""
        else:
            condition_field += " AND " + entry + " = " + qbe_normalized[entry]
            qbe_normalized[entry] = ""

    clean_what_is_told(qbe_normalized=qbe_normalized, tell="")

    for entry in remaining_variable_list:
        if len(remaining_variable_list[entry]) <= 1:
            raise ValueError("Bad QBE Query. Single variable found that is not referenced in the condition box")
        else:
            condition_field += " AND " + " = ".join(remaining_variable_list[entry])

    query_string = select_part + " " + from_part + " " + where_part + " " + condition_field

    # Check for dangling AND conditions
    if query_string.rstrip()[-3:] == "AND":
        query_string = query_string[:-5]

    # Add the order by part after the where condition is cleaned
    if orderby_part != "ORDER BY ":
        query_string = query_string + " " + orderby_part

    # Remove all extra spaces
    for i in range(10):
        query_string = query_string.replace("  ", " ")
    query_string = query_string.replace("AND AND", "AND")

    return query_string


def clean_what_is_told(qbe_normalized, tell):
    # Removing entries with value = ""
    qbe_normalized_cleaned = dict()
    for entry in qbe_normalized:
        if qbe_normalized[entry] != tell:
            qbe_normalized_cleaned[entry] = qbe_normalized[entry]
    return qbe_normalized_cleaned


def clean_part_of_it(qbe_normalized, whatpart):
    # Removing entries with value = ""
    for entry in qbe_normalized:
        if whatpart in qbe_normalized[entry]:
            qbe_normalized[entry] = str(qbe_normalized[entry]).replace(whatpart, "")
    return qbe_normalized


def get_ao_do_key(ao_do_value):
    cleaned_value = str(ao_do_value).lstrip().rstrip().replace(" ", "")
    if cleaned_value == "AO.":
        return "0-AO", cleaned_value
    elif cleaned_value == "DO.":
        return "0-DO", cleaned_value
    elif "AO(" in cleaned_value:
        return cleaned_value[3] + "-AO", cleaned_value
    elif "DO(" in cleaned_value:
        return cleaned_value[3] + "-DO", cleaned_value
    else:
        raise ValueError("Bad QBE Query. Invalid AO/DO condition")
