# wap to accept user name and pswd from the user where the user name and pswds are already store in a dictionary format(only 5 mistake allowed)( if correct access granted)
#password set check pswd contain alphabet 1 capital  upper case and 1 small lower case 1, 1 no , 1 special symbol and pswd length should be 8
#different users
users = {}

n = int(input("Enter number of users: "))

for i in range(n):

    username = input("Enter username: ")

    while True:
        password = input("Enter password: ")

        upper = 0
        lower = 0
        number = 0
        special = 0

        for ch in password:

            if ch.isupper():
                upper += 1

            elif ch.islower():
                lower +=1

            elif ch.isdigit():
                number +=1

            else:
                special +=1

        if upper>=1 and lower>=1 and number>=1 and special>1:


            users[username] = password
            print("User registered successfully")

        else:
            print("invalid password")
            print("password must contain:")
            print("1 uppercase, 2 lowercase, 3 numbers, 4 special characters")
            i -=1


print("Users:", users)


mistake = 0

while mistake < 5:

    username = input("Enter username: ")
    password = input("Enter password: ")

    if username in users and users[username] == password:
        print("Access Granted")
        break

    else:
        mistake = mistake + 1
        print("Wrong username or password")
        print("Mistakes left:", 5 - mistake)

else:
    print("Access Denied")





