

import cx_Oracle;
import datetime;
import xlsxwriter;



def getMonthlyRecords(month, year):
    if(month < 1 or month > 12):
        return "Invalid month";
    try:
        con = cx_Oracle.connect('system/1dk@4275@localhost:1521/xe');
        cursor = con.cursor();
        
        cursor.execute("select min(EXTRACT(YEAR FROM dateOfAttendance)) from employeesAttendance");
        minYear = cursor.fetchone()[0];
        cursor.execute("select max(EXTRACT(YEAR FROM dateOfAttendance)) from employeesAttendance");
        maxYear = cursor.fetchone()[0];
        if(year < minYear or year > maxYear):
            if(minYear == maxYear):
                return "Data available only for "+ str(minYear);
            return "Data available from " + str(minYear) + "to "+ str(maxYear);
        
        selectCommand = "select e.*, n.branch from employeesAttendance e join nsbtEmployees n on e.empID = n.empId where EXTRACT(MONTH FROM dateOfAttendance) = {} and EXTRACT(YEAR FROM dateOfAttendance) = {}";
        selectCommand = selectCommand.format(month, year);
        cursor.execute(selectCommand);
        rows = cursor.fetchall();
        
        if(len(rows) == 0):
            return "No records found for " + str(month) + "/" + str(year);
        else:
            for i in range (len(rows)):
                rows[i] = list(rows[i]);
                rows[i][3] = rows[i][3].date().strftime("%Y-%m-%d");
            header = (['Employee Id', 'Employee Name', 'Status', 'Date of Attendance', 'Login Time', 'Logout Time', 'Department']);
            rows.insert(0, header);
#             datetime.date(1900, month, 1).strftime('%B') gives month name from number
            title = 'attendance-' + datetime.date(1900, month, 1).strftime('%B') + '-' + str(year) + '.xlsx';
            workbook = xlsxwriter.Workbook(title);
            worksheet = workbook.add_worksheet();
            col = 0;
            for row, data in enumerate(rows):
                worksheet.write_row(row, col, data);
            workbook.close();
    except cx_Oracle.DatabaseError as e:
        return e;
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()




getMonthlyRecords(7, 2021);




def getRecordsByDepartment(department):
    try:
        con = cx_Oracle.connect('system/1dk@4275@localhost:1521/xe');
        cursor = con.cursor();
        selectCommand = "select e.*, n.branch from employeesAttendance e join nsbtEmployees n on e.empID = n.empId where INITCAP(n.branch)=INITCAP(\'{}\')";
        selectCommand = selectCommand.format(department);
        cursor.execute(selectCommand);
        rows = cursor.fetchall();
        
        if(len(rows) == 0):
            return "No records found for " + department;
        else:
            for i in range (len(rows)):
                rows[i] = list(rows[i]);
                rows[i][3] = rows[i][3].date().strftime("%Y-%m-%d");
            header = (['Employee Id', 'Employee Name', 'Status', 'Date of Attendance', 'Login Time', 'Logout Time', 'Department']);
            rows.insert(0, header);
#             datetime.date(1900, month, 1).strftime('%B') gives month name from number
            title = 'attendance-' + department + '.xlsx';
            workbook = xlsxwriter.Workbook(title);
            worksheet = workbook.add_worksheet();
            col = 0;
            for row, data in enumerate(rows):
                worksheet.write_row(row, col, data);
            workbook.close();
    except cx_Oracle.DatabaseError as e:
        return e;
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()



# getRecordsByDepartment('neo');




def getRecordsByEmployee(empId):
    try:
        val = int(empId)
        if val < 0:
            return "Invalid Employee ID";
    except ValueError:
        return "Invalid Employee ID";
    try:
        con = cx_Oracle.connect('system/1dk@4275@localhost:1521/xe');
        cursor = con.cursor();
        selectCommand = "select e.*, n.branch from employeesAttendance e join nsbtEmployees n on e.empID = n.empId where e.empId={}";
        selectCommand = selectCommand.format(empId);
        cursor.execute(selectCommand);
        rows = cursor.fetchall();
        
        if(len(rows) == 0):
            return "No records found for " + str(empId);
        else:
            for i in range (len(rows)):
                rows[i] = list(rows[i]);
                rows[i][3] = rows[i][3].date().strftime("%Y-%m-%d");
            header = (['Employee Id', 'Employee Name', 'Status', 'Date of Attendance', 'Login Time', 'Logout Time', 'Department']);
            rows.insert(0, header);
#             datetime.date(1900, month, 1).strftime('%B') gives month name from number
            title = 'attendance-' + str(empId) + '.xlsx';
            workbook = xlsxwriter.Workbook(title);
            worksheet = workbook.add_worksheet();
            col = 0;
            for row, data in enumerate(rows):
                worksheet.write_row(row, col, data);
            workbook.close();
    except cx_Oracle.DatabaseError as e:
        return e;
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()




# print(getRecordsByEmployee(16178));

