from datetime import datetime
#list of users
users = [{'name': 'Semen', 'birthday': datetime(year=2021, month=10, day=24)},
                 {'name': 'George', 'birthday': datetime(
                     year=2021, month=10, day=27)},
                 {'name': 'Peter', 'birthday': datetime(
                     year=2021, month=10, day=22)},
                 {'name': 'Vasyl', 'birthday': datetime(
                     year=2021, month=10, day=25)},
                 {'name': 'Victoria', 'birthday': datetime(
                     year=2021, month=10, day=26)},
                 {'name': 'Catalina', 'birthday': datetime(
                     year=2021, month=10, day=28)},
                 {'name': 'Daniela', 'birthday': datetime(
                     year=2021, month=10, day=1)},
                 {'name': 'Paul', 'birthday': datetime(
                     year=2021, month=10, day=24)},
                 {'name': 'Kevin', 'birthday': datetime(
                     year=2021, month=10, day=27)}
                 ]


def print_collection(birtdays):
    for key, values in birtdays.items():
        if values:
            print(f'{key} : {values}')


def congratulate(users):
    #Print list of employees, who have birthdays next week

    current_week = datetime.now().isocalendar().week
    birthday = {'Monday': '', 'Tuesday': '',
                'Wednesday': '', 'Thursday': '', 'Friday': ''}

    for user in users:

        user_week = user['birthday'].isocalendar().week
        day = user['birthday'].weekday()
        weekday = user['birthday'].strftime('%A')

        if user_week == current_week+1 and day < 6:
            if birthday[weekday]:
                birthday[weekday] += f", {user['name']}"
            else:
                birthday[weekday] += user['name']

        elif user_week == current_week and 5 < day < 8:
            if birthday['Monday']:
                birthday['Monday'] += f", {user['name']}"
            else:
                birthday['Monday'] += user['name']

    print_collection(birthday)
    return birthday


if __name__ == '__main__':
    congratulate(users)