from datetime import datetime

# The Moscow Times
dt1 = datetime.strptime("Wednesday, October 2, 2002", "%A, %B %d, %Y")

# The Guardian
dt2 = datetime.strptime("Friday, 11.10.13", "%A, %d.%m.%y")

# Daily News
dt3 = datetime.strptime("Thursday, 18 August 1977", "%A, %d %B %Y")

print(dt1)  # 2002-10-02 00:00:00
print(dt2)  # 2013-10-11 00:00:00
print(dt3)  # 1977-08-18 00:00:00
