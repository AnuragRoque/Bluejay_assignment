import csv
from datetime import datetime, timedelta
# CSV file
filename = 'Assignment_Timecard.csv'

# required time thresholds
consecutive_days_threshold = 7
time_between_shifts_min = timedelta(hours=1)
time_between_shifts_max = timedelta(hours=10)
max_shift_duration = timedelta(hours=14)


# function to convert time strings to datetime objects
def parse_time(time_str):
    try:
        return datetime.strptime(time_str, '%m/%d/%Y %I:%M %p')
    except ValueError:
        return None

# helper function to calculate the duration between two time strings
def calculate_duration(start_time_str, end_time_str):
    start_time = parse_time(start_time_str)
    end_time = parse_time(end_time_str)

    if start_time and end_time:
        return end_time - start_time
    else:
        return None

# 
with open(filename, 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row

    current_employee = None
    consecutive_days = 0
    previous_end_time = None

    #lists for each category
    consecutive_days_employees = []
    less_than_10_hours_employees = []
    long_shift_employees = []

    # Iterate over each row in the CSV file
    for row in reader:
        position_id = row[0]
        start_time = row[2]
        end_time = row[3]
        employee_name = row[7]

        # Check if the employee has worked for 7 consecutive days
        if employee_name == current_employee:
            consecutive_days += 1

        else:
            consecutive_days = 1
            current_employee = employee_name
            
        if consecutive_days == consecutive_days_threshold:
            consecutive_days_employees.append((employee_name, position_id))

        # Check if the time between shifts is less than 10 hours but greater than 1 hour
            
        if previous_end_time and start_time:
            time_between_shifts = parse_time(start_time) - parse_time(previous_end_time)
            if time_between_shifts_min < time_between_shifts < time_between_shifts_max:
                less_than_10_hours_employees.append((employee_name, position_id))

        # Check if the employee has worked for more than 14 hours in a single shift
        shift_duration = calculate_duration(start_time, end_time)
        if shift_duration and shift_duration > max_shift_duration:
            long_shift_employees.append((employee_name, position_id))

        # Update the previous end time for the next iteration
        previous_end_time = end_time

    # Print the categorized employee lists
    print("Employees who worked for 7 consecutive days: ")
    for employee in consecutive_days_employees:
        print(f"Employee: {employee[0]} (ID: {employee[1]})")

    print("\nEmployees with less than 10 hours between shifts: ")
    for employee in less_than_10_hours_employees:
        print(f"Employee: {employee[0]} (ID: {employee[1]})")

    print("\nEmployees who worked more than 14 hours in a single shift:")
    for employee in long_shift_employees:
        print(f"Employee: {employee[0]} (ID: {employee[1]})")

#create output file
with open('output.txt', 'w') as f:
        f.write("Employees who worked for 7 consecutive days: \n")
        for employee in consecutive_days_employees:
            f.write(f"Employee: {employee[0]} (ID: {employee[1]})\n")


        f.write("\nEmployees with less than 10 hours between shifts: \n")
        for employee in less_than_10_hours_employees:
            f.write(f"Employee: {employee[0]} (ID: {employee[1]})\n")

        f.write("\nEmployees who worked more than 14 hours in a single shift: \n")
        for employee in long_shift_employees:
            f.write(f"Employee: {employee[0]} (ID: {employee[1]})\n")