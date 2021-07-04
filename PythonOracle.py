import cx_Oracle;
import datetime;

def createTable():
    try:
        con = cx_Oracle.connect('system/1dk@4275@localhost:1521/xe');
        cursor = con.cursor();
        command = "create table employeesAttendance(empId NUMBER(5) not null, empName varchar(30) not null, status varchar(3) CHECK (status IN ('IN','OUT') ) not null, dateOfAttendance DATE not null, loginDateTime char(5), logoutDateTime char(5), constraint t_pk primary key (empId, dateOfAttendance))";
        cursor.execute(command);
    except cx_Oracle.DatabaseError as e:
        print("There is a problem with Oracle", e)
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()
#createTable();

def insertRecords(empId, empName, dateTimeOfAttendance):

    dateOfAttendance = dateTimeOfAttendance.date().strftime("%Y-%m-%d");
    dateTimeOfAttendance = dateTimeOfAttendance.strftime("%Y-%m-%d %H:%M:%S");
    try:
        con = cx_Oracle.connect('system/1dk@4275@localhost:1521/xe');
        cursor = con.cursor();
        
        
#         check if there is any entry for employee for today
        selectCommand = "select empName from employeesAttendance where empId={} and dateOfAttendance=to_date(\'{}\', 'yyyy/mm/dd')";
        selectCommand = selectCommand.format(empId, dateOfAttendance);
        cursor.execute(selectCommand);
        rows = cursor.fetchone();
        
        
#         if there is an entry for today, check if employee already logged out
        selectCommand1 = "select empName from employeesAttendance where empId={} and dateOfAttendance=to_date(\'{}\', 'yyyy/mm/dd') and status=\'{}\'";
        selectCommand1 = selectCommand1.format(empId, dateOfAttendance, 'OUT');
        cursor.execute(selectCommand1);
        rows1 = cursor.fetchone();
        

        if(rows == None):
            command = "insert into employeesAttendance(empId, empName, status, dateOfAttendance, loginDateTime) values({}, \'{}\', \'{}\', to_date(\'{}\', 'yyyy/mm/dd'), to_char(to_date(\'{}\', 'yyyy/mm/dd hh24:mi:ss'), 'hh24:mi'))";
            command = command.format(empId, empName, 'IN', dateOfAttendance, dateTimeOfAttendance);
        elif(rows1 == None):
            command = "update employeesAttendance set status=\'{}\', logoutDateTime = to_char(to_date(\'{}\', 'yyyy/mm/dd hh24:mi:ss'), 'hh24:mi') where empId={} and dateOfAttendance=to_date(\'{}\', 'yyyy/mm/dd')";
            command = command.format('OUT',dateTimeOfAttendance, empId, dateOfAttendance);
        else:
            return "Already logged out for the day";
        
        
        cursor.execute(command);
        con.commit();
        return "";
    except cx_Oracle.DatabaseError as e:
        return e;
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()


def validate_Employee(empId):
    # print("gggggggggggggggg")
    try:

        con = cx_Oracle.connect('system/1dk@4275@localhost:1521/xe');
        cursor = con.cursor();
        # sqlq = "SELECT COUNT(1) FROM  nsbtEmployees WHERE empId = ? " , empId
        # cursor.execute(sqlq)
        # if cursor.fetchone()[0]:
        #   print("ddd")
        selectCommand1 = "select empName from  nsbtEmployees where empId={}" ;
        selectCommand1 = selectCommand1.format(empId);
        cursor.execute(selectCommand1);
        rows1 = cursor.fetchone();
        con.commit();
        if rows1:
            return True;
        else:
            return False;
        return "";
    except cx_Oracle.DatabaseError as e:
        return e;
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()


#print(insertRecords(16180, 'Taylor', datetime.datetime.now()));
#print(insertRecords(16180, 'Taylor', datetime.datetime.now()));
#print(insertRecords(16180, 'Taylor', datetime.datetime.now()));
#createTable()
print(validate_Employee(16145))