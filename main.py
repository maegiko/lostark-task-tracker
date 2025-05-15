"""
LOST ARK TRACKER
Welcome to my very first web app! This is a task tracker for the popular KMMO
(Korean MMO), Lost Ark.

Lost Ark is a grindy video-game with a lot of daily/weekly tasks with lucrative
rewards! Once you complete a weekly task on ONE character, you are done until
the next week so a lot of players play more than one character (usually 6).

Since the rewards are so lucrative, players don't want to miss out! There are
3 weekly raids (boss fights) and 3 daily tasks per character, so 6 characters
would be a total of 18 weekly raids and 18 daily tasks, a hefty total of 36
things to do!

I have made this simple task tracker allowing users to add their characters,
their respective tasks and simply check them once complete!

I hope this helps alleviate any stress from managing your tasks in-game! Video
games are meant to be fun and I believe my web app allows users to have an easier time.

Author: Kenneth Koon

Date: 12/03/2024
"""

from flask import Flask, request, session, redirect
import pyhtml as h
from jsonfunctions import read_json_file

###### NOTES ######

# Uses jsonfunctions.py provided by Sim Mautner for functions to read/write from JSON files.
# Sim Mautner assisted with the external storage of my tasks.json data.
# Sim Mautner assisted with creating a session counter to repeat a html display and append
# tasks to the dictionary.
# Sim Mautner assisted with displaying the table.
# Sim Mautner assisted with refactoring my code for readability reasons.

# Any line of code followed by the comment: # type: ignore, works perfectly
# fine but for whatever reason, shows red squiggly lines on my version of the
# app. I don't like looking at this so I've forced them to disappear.

###### NOTES ######

app = Flask(__name__)
app.config['SECRET_KEY'] = "bLx1dx9ex04x8579x91hxd7xbdxa6x89x12xd7"
app.json.sort_keys = False # type: ignore

def tasks_checker(name, addOrDelete, timer):
    '''
    This function checks for tasks either present or not present in the user's
    list. It is used for generating a list of tasks for when the user is
    editing their tasks (adding or deleting).

    Args:
        name: Character Name chosen by user from a dropdown Menu.
        addOrDelete: either "Add" or "Delete:
            Add: Checks if tasks are not in the user's session, and adds
            them to a list if so.
            Delete: Checks if tasks are in the user's session, and adds them
            to a list if so.
        timer: Either Daily or Weekly, this is used to section the tasks for
               displaying purposes.

    Returns:
        A list of tasks, tasks_left(remaining tasks) or char_tasks(existing tasks).
    '''
    taskList = read_json_file('tasks.json')

    if addOrDelete == "Add":
        tasks_left = []
        for task, detail in taskList.items():
            if detail['timer'] == timer and task not in session["account"][name]:
                tasks_left.append(h.input(type='checkbox', name=task, id=detail['id'], class_='taskList'))
                tasks_left.append(h.label(for_=detail['id'], class_='taskLabel')(h.img(src=detail['icon'], class_='taskIcon'))(h.b(task)))
                tasks_left.append(h.br)
        return tasks_left

    elif addOrDelete == "Delete":
        char_tasks = []
        for task, detail in taskList.items():
            if detail['timer'] == timer and task in session["account"][name]:
                char_tasks.append(h.input(type='checkbox', name=task, id=detail['id'], class_='taskList'))
                char_tasks.append(h.label(for_=detail['id'], class_='taskLabel')(h.img(src=detail['icon'], class_='taskIcon'))(h.b(task)))
                char_tasks.append(h.br)
        return char_tasks

def dropdown_list_generator():
    '''
    Generates a list for dropdown lists for existing characters.

    Returns:
        account_list: A list of existing characters as select options.
    '''
    account_list = [h.option(id='emptyOption')(disabled=True, selected = True, value='')]
    for char in session['account']:
        account_list.append(h.option(char))
    return account_list

def character_exists(character):
    '''
    Checks for the existence of character in user's list.

    Args:
        character: character name inputted by user

    Returns:
        Exists: True
        Doesn't Exist: False
    '''
    account_list = []
    for char in session['account']:
        account_list.append(char.lower())
    if character is None:
        return False
    return character.lower() in account_list

def html_header(page_title):
    '''
    Generates a html head with the relevant title name.
    '''
    css_file = "static/stylesheet.css"
    return h.head(
        h.title(page_title),
        h.link(rel='stylesheet', href=css_file)
    )

def row_generator(account, task_timer, task_timer_plural):
    '''
    Generates the rows for the final table showing the user their to-do list.

    Args:
        account: Calls the users 'account' in their session
        task_timer: Either 'Daily' or 'Weekly. Used to match task in tasks.json.
        task_timer_plural: Either 'Dailies' or 'Weeklies'. Used to add either
        'Dailies' or 'Weeklies' as a element in the table to discern tasks.

    Returns:
        List: Contains the 'task timer'(Dailies or Weeklies) and the tasks the
        user chose with checkboxes to be displayed in a HTML table for the
        function of this web app.
    '''
    row = []
    count = 1
    tasks_list = read_json_file('tasks.json')
    row = [h.td(class_=f'{task_timer_plural}_header')(h.b(f"{task_timer_plural}"))]
    for char, char_tasks in account.items():
        dailies = []
        for task in char_tasks:
            if task in tasks_list:
                if tasks_list[task]["timer"] == task_timer:
                    dailies.append(h.input(type='checkbox', id=task_timer + str(count), class_='checkboxes'))
                    dailies.append(h.label(for_=task_timer + str(count))(h.img(src=tasks_list[task]['icon']))(task))
                    dailies.append(h.br)
            count += 1
        row.append(h.td(dailies))
    return row

def task_list_generator(timer):
    '''
    Generates a list of tasks (either daily or weekly) for use when the user
    adds tasks to their characters.

    Args:
        timer: Either 'Daily' or 'Weekly'. Used to match the task in
        tasks.json and add it to a daily/weekly list used to generate a html list.

    Returns:
        List: A list of tasks.
    '''
    tasks = read_json_file('tasks.json')
    tasks_list = []
    for task, task_details in tasks.items():
        if task_details["timer"] == timer:
            tasks_list.append(h.input(type='checkbox', name=task, id=task_details['id'], class_='taskList'))
            tasks_list.append(h.label(for_=task_details['id'], class_='taskLabel')(h.img(src=task_details['icon'], class_='taskIcon'))(h.b(task)))
            tasks_list.append(h.br)
    return tasks_list

def task_editor(char_name, tasks, add_or_delete):
    '''
    Adds or Removes tasks from the user's manager cookie.

    Args:
        char_name: The name of the character the user is editing.
        tasks: A list of tasks the user chose to add/remove.
        add_or_delete: 'append' or 'delete:
            append:
                Loops through the tasks list and checks if any items ARE NOT
                in the session. Adds them if they aren't.
            delete:
                loops through the tasks list and checks if any items ARE in
                the session. Deletes them if they are.
    '''
    char_name = char_name.capitalize()

    if add_or_delete == "append":
        for task in tasks:
            if task not in session["account"][char_name]:
                session["account"][char_name].append(task)
                session.modified = True

    elif add_or_delete == "delete":
        for task in tasks:
            if task in session["account"][char_name]:
                session["account"][char_name].remove(task)
                session.modified = True

def character_add(character, form_items):
    '''
    This function adds a new character and their tasks into their session.

    Args:
        character: User inputted character name as the key.
        form_items: The form submitted in order to add tasks as values to
        the character.
    '''
    character = character.capitalize()
    if character not in session['account']:
        session['account'][character] = []
        for key, value in form_items:
            if value == 'on':
                session['account'][character].append(key)

@app.route('/delete', methods=["GET", "POST"])
def delete():
    '''
    This route clears everything in the session.
    '''
    if 'account' not in session:
        return redirect('/')

    session.clear()
    response = h.html(
        html_header("Deletion"),
        h.body(
            h.h1("LOST ARK TRACKER"),
            h.p("Everything has been cleared. Click the button below to return to home screen."),
            h.div(h.a(href='/')(h.button("Back to Main Menu")))
        )
    )
    return str(response)

@app.route('/editcharacters', methods=["GET", "POST"])
def edit_character():
    '''
    This route allows users to add or delete characters from their list.
    '''
    if 'account' not in session:
        return redirect('/')

    if request.method == "POST" and request.form.get('character') is not None:
        character = request.form.get('character').capitalize() # type: ignore

    if 'append' in request.form:
        dailies = task_list_generator("Daily")
        weeklies = task_list_generator("Weekly")
        content = [
            h.form(action='/editcharacters')(
                h.label(for_='char_name')(h.b("Enter Character Name:")),
                h.br,
                h.input(type='text', name='character', required=True , placeholder="Character Name", class_="editName"),
                h.br,
                h.p(h.b("Choose tasks: ")),
                h.h3(class_='taskHeader')("DAILIES"),
                h.div(class_='chooseTaskList')(dailies),
                h.h3(class_='taskHeader')("WEEKLIES"),
                h.div(class_='chooseTaskList')(weeklies),
                h.br,
                h.input(type='submit', id='finish_btn', name='choosetasks', value='Finish'),
            ),
            h.div(h.a(href='/editcharacters')(h.button("Back")))
        ]

        response = h.html(
            html_header("Add Character"),
            h.body(
                h.h1("LOST ARK TRACKER"),
                content
            )
        )

    if 'delete' in request.form:
        charList = dropdown_list_generator()

        response = h.html(
            html_header("Delete Character"),
            h.body(
                h.h1("LOST ARK TRACKER"),
                h.form(action='editcharacters')(
                    h.label(for_='char_name')(h.b("Choose Character:")),
                    h.br,
                    h.select(name='character', required=True , class_="charDropDown")(charList),
                    h.br,
                    h.input(type='submit', name='removeChar', value='Delete Character', onclick='return confirm("Are you sure?")'),
                ),
                h.div(h.a(href='/editcharacters')(h.button("Back")))
            )
        )

    if 'removeChar' in request.form:
        del session['account'][character]
        response = h.html(
            html_header("Delete Character"),
            h.body(
                h.h1("LOST ARK TRACKER"),
                h.p(f"{character} has been deleted from your list!"),
                h.div(h.a(href='/tasktracker')(h.button("Back to Task Tracker")))
            )
        )

    if 'choosetasks' in request.form:
        if character_exists(character):
            content = [
                h.p(f"{character} already exists in your list! Please try again."),
                h.div(h.a(href='/editcharacters')(h.button("Back to Character Editor")))
            ]
        else:
            character_add(character, request.form.items())
            content = [
                h.p(f"{character} and their tasks have been added to your list!"),
                h.div(h.a(href='/tasktracker')(h.button("Back to Task Tracker")))
            ]

        response = h.html(
            html_header("Add Character"),
            h.body(
                h.h1("LOST ARK TRACKER"),
                content
            )
        )

    if request.method == "GET":
        response = h.html(
            html_header("Edit Characters"),
            h.body(
                h.h1("LOST ARK TRACKER"),
                h.p("You may add/delete a character here."),
                h.form(action='/editcharacters')(
                    h.input(type='submit', name='append', value='Add Character'),
                    h.input(type='submit', name='delete', value='Delete Character'),
                ),
                h.div(h.a(href='/tasktracker')(h.button("Back to Task Tracker")))
            )
        )
    return str(response)

@app.route('/edittasks', methods=["GET", "POST"])
def edit_tasks():
    '''
    This route allows users to edit the tasks of their characters. They can
    add/delete tasks.

    If the user is adding tasks, only the tasks not already tied to the
    particular character are displayed.

    If the user is deleting tasks, only the tasks tied to the particular
    character are displayed.
    '''
    if 'account' not in session:
        return redirect('/')

    if 'append' in request.form:
        rDailies = tasks_checker(request.form.get('character'), "Add", "Daily") # r means remaining (r(emaining)Dailies)
        rWeeklies = tasks_checker(request.form.get('character'), "Add", "Weekly")
        assert rDailies is not None
        assert rWeeklies is not None
        session['tempChar'] = request.form.get('character')

        if rWeeklies == [] and rDailies == []:
            content = [
                h.h1("LOST ARK TRACKER"),
                h.p(f"{session['tempChar']} has every task added already! Try again."),
                h.div(h.a(href='/edittasks')(h.button("Back")))
            ]

        elif rDailies == []:
            content = [
                h.h1("LOST ARK TRACKER"),
                h.p(f"Please choose the tasks you'd like to add to {session['tempChar']}."),
                h.form(action='/edittasks')(
                    h.h3(class_='taskHeader')("WEEKLIES"),
                    h.div(class_='chooseTaskList')(rWeeklies),
                    h.br,
                    h.input(type='submit', id='add_tasks', name='add_tasks', value='Add Task(s)')
                ),
                h.div(h.a(href='/edittasks')(h.button("Back")))
            ]

        elif rWeeklies == []:
            content = [
                h.h1("LOST ARK TRACKER"),
                h.p(f"Please choose the tasks you'd like to add to {session['tempChar']}."),
                h.form(action='/edittasks')(
                    h.h3(class_='taskHeader')("DAILIES"),
                    h.div(class_='chooseTaskList')(rDailies),
                    h.br,
                    h.input(type='submit', id='add_tasks', name='add_tasks', value='Add Task(s)')
                ),
                h.div(h.a(href='/edittasks')(h.button("Back")))
            ]

        else:
            content = [
                h.h1("LOST ARK TRACKER"),
                h.p(f"Please choose the tasks you'd like to add to {session['tempChar']}."),
                h.form(action='/edittasks')(
                    h.h3(class_='taskHeader')("DAILIES"),
                    h.div(class_='chooseTaskList')(rDailies),
                    h.h3(class_='taskHeader')("WEEKLIES"),
                    h.div(class_='chooseTaskList')(rWeeklies),
                    h.br,
                    h.input(type='submit', id='add_tasks', name='add_tasks', value='Add Task(s)')
                ),
                h.div(h.a(href='/edittasks')(h.button("Back")))
            ]

        response = h.html(
            html_header("Add Tasks"),
            h.body(
                content
            )
        )

    if 'add_tasks' in request.form:
        tasks = []
        for key, value in request.form.items():
            if value == 'on':
                tasks.append(key)
        task_editor(session['tempChar'], tasks, 'append')

        response = h.html(
            html_header('Task(s) Added'),
            h.body(
                h.h1("LOST ARK TRACKER"),
                h.p(f"You have successfully added the selected task(s) to {session['tempChar']}!"),
                h.div(h.a(href='/tasktracker')(h.button("Back to Task Tracker")))
            )
        )

    if 'delete' in request.form:
        eDailies = tasks_checker(request.form.get('character'), "Delete", "Daily") # e means existing (e(xisting)Dailies)
        eWeeklies = tasks_checker(request.form.get('character'), "Delete", "Weekly")
        assert eDailies is not None
        assert eWeeklies is not None
        session['tempChar'] = request.form.get('character')

        if eWeeklies == [] and eDailies == []:
            content = [
                h.h1("LOST ARK TRACKER"),
                h.p(f"There are no tasks left to delete from {session['tempChar']}! Try again."),
                h.div(h.a(href='/edittasks')(h.button("Back")))
            ]

        elif eDailies == []:
            content = [
                h.h1("LOST ARK TRACKER"),
                h.p(f"Please choose the tasks you'd like to delete from {session['tempChar']}."),
                h.form(action='/edittasks')(
                    h.h3(class_='taskHeader')("WEEKLIES"),
                    h.div(class_='chooseTaskList')(eWeeklies),
                    h.br,
                    h.input(type='submit', id='delete_tasks', name='delete_tasks', value='Delete Task(s)')
                ),
                h.div(h.a(href='/edittasks')(h.button("Back")))
            ]

        elif eWeeklies == []:
            content = [
                h.h1("LOST ARK TRACKER"),
                h.p(f"Please choose the tasks you'd like to delete from {session['tempChar']}."),
                h.form(action='/edittasks')(
                    h.h3(class_='taskHeader')("DAILIES"),
                    h.div(class_='chooseTaskList')(eDailies),
                    h.br,
                    h.input(type='submit', id='delete_tasks', name='delete_tasks', value='Delete Task(s)')
                ),
                h.div(h.a(href='/edittasks')(h.button("Back")))
            ]

        else:
            content = [
                h.h1("LOST ARK TRACKER"),
                h.p(f"Please choose the tasks you'd like to delete from {session['tempChar']}."),
                h.form(action='/edittasks')(
                    h.h3(class_='taskHeader')("DAILIES"),
                    h.div(class_='chooseTaskList')(eDailies),
                    h.h3(class_='taskHeader')("WEEKLIES"),
                    h.div(class_='chooseTaskList')(eWeeklies),
                    h.br,
                    h.input(type='submit', id='delete_tasks', name='delete_tasks', value='Delete Task(s)')
                ),
                h.div(h.a(href='/edittasks')(h.button("Back")))
            ]

        response = h.html(
            html_header("Delete Tasks"),
            h.body(
                content
            )
        )

    if 'delete_tasks' in request.form:
        tasks = []
        for key, value in request.form.items():
            if value == 'on':
                tasks.append(key)
        task_editor(session['tempChar'], tasks, 'delete')

        response = h.html(
            html_header('Task(s) Added'),
            h.body(
                h.h1("LOST ARK TRACKER"),
                h.p(f"You have successfully deleted the selected task(s) to {session['tempChar']}!"),
                h.div(h.a(href='/tasktracker')(h.button("Back to Task Tracker")))
            )
        )

    if request.method == "GET":
        charList = dropdown_list_generator()
        response = h.html(
            html_header("Edit Tasks"),
            h.body(
                h.h1("LOST ARK TRACKER"),
                h.p("You may add/delete tasks from a character here."),
                h.form(action='/edittasks')(
                    h.label(for_='char_name')(h.b("Choose Character:")),
                    h.br,
                    h.select(name='character', required=True , class_="charDropDown")(charList),
                    h.br,
                    h.input(type='submit', name='append', value='Add Task(s)'),
                    h.input(type='submit', name='delete', value='Delete Task(s)'),
                ),
                h.div(h.a(href='/tasktracker')(h.button("Back to Task Tracker")))
            )
        )
    return str(response)

@app.route('/tasktracker', methods=["GET", "POST"])
def tasktracker():
    '''
    This route is the final destination of the web app. This is where all the
    inputted characters and their respective tasks are displayed with checkboxes
    for the user to manually check on and off.
    '''
    if 'account' not in session:
        return redirect('/')

    session.permanent = True

    headers = [h.th("")]
    for char in session["account"]:
        headers.append(h.th(class_='charNames')(char))

    dailies = row_generator(session["account"], 'Daily', 'Dailies')
    weeklies = row_generator(session["account"], 'Weekly', 'Weeklies')

    response = h.html(
        html_header("LOA Task Tracker"),
        h.body(
            h.h1(class_='trackerTitle')("LOST ARK TRACKER"),
            h.h2("This is your tracker. Click on the checkbox once you have completed the task."),
            h.h2("And that's it!"),
            h.h3("Checkboxes automatically reset!"),
            h.div(class_='tracker_table')(
                h.table(
                    h.tr(headers),
                    h.div(class_='tableTasks')(h.tr(class_='daily_table')(dailies)),
                    h.tr(class_='weekly_table')(weeklies),
                )
            ),
            h.div(
                h.a(href='/editcharacters')(h.button(class_='editChar')("Add/Delete Character")),
                h.br,
                h.a(href='/edittasks')(h.button("Add/Delete Task(s)"))
            ),
            h.form(action='/delete')(
                h.input(type='submit', name='delete', value='Delete Everything', onclick='return confirm("Are you sure?")'),
            ),
            h.h2(class_='dailyReset')("Daily Reset:"),
            h.div(class_='drtDiv')(
                h.h3(class_='dailyResetTime')("8pm AEST")
            ),
            h.h2(class_='weeklyReset')("Weekly Reset:"),
            h.div(class_='wrtDiv')(
                h.h3(class_='weeklyResetTime')("Every Wednesday 8pm AEST")
            ),
            h.script(src='static/javascript.js')
        )
    )
    return str(response)

@app.route('/choosetasks', methods=["POST"])
def choosetasks():
    '''
    This route is where the user will select the tasks they wish to track for
    each of the characters they have inputted.
    '''
    char_up_to = session.get('char_count', -1)

    if char_up_to >= 0:
        character_name = list(session["account"].keys())[char_up_to]
        for task, tick in request.form.items():
            if tick == "on":
                session["account"][character_name].append(task)
                session.modified = True

    session['char_count'] += 1
    char_up_to += 1

    if char_up_to >= len(session["account"]):
        return redirect('/tasktracker')

    character_name = list(session["account"].keys())[char_up_to]

    dailies = task_list_generator("Daily")
    weeklies = task_list_generator("Weekly")

    response = h.html(
        html_header("Choose Tasks"),
        h.body(
        h.h1("LOST ARK TRACKER"),
        h.h3(f"Choose activities for: {character_name}"),
        h.form(action='/choosetasks')(
            h.h3(class_='taskHeader')("DAILIES"),
            h.div(class_='chooseTaskList')(dailies),
            h.h3(class_='taskHeader')("WEEKLIES"),
            h.div(class_='chooseTaskList')(weeklies),
            h.br,
            h.input(type='submit', id='finish_btn', name='choosetasks', value='Next')
            )
        )
    )
    return str(response)

@app.route('/characters', methods=["GET", "POST"])
def characters():
    '''
    This route allows the user to enter the names of their characters. There
    are attributes set so that the user must enter a name in the text input.
    '''
    if request.method == 'GET':
        return redirect('/')

    if "account" not in session:
        session["account"] = {}
    if "char_count" not in session:
        session["char_count"] = -1
    char_names = []
    total = 0

    if 'char_amount_btn' in request.form:
        total = int(request.form.get('totalchars', 0))

    i = 1
    while i <= total:
        char_names.append(h.input(type='text', name="char_names" + str(i), id='char_names', required=True, placeholder=f"Enter Name", class_='editName'))
        char_names.append(h.br)
        char_names.append(h.br)
        i += 1

    if 'char_amount_btn' in request.form:
        response = h.html(
            html_header("Enter Characters"),
            h.body(
                h.h1("LOST ARK TRACKER"),
                h.h2("Enter your character name(s)"),
                h.form(action='/characters')(
                    char_names,
                    h.input(type='submit', name='name_btn', id='name_btn', value='Next')
                )
            )
        )
    if 'name_btn' in request.form:
        characters_list = []
        confirm_character_list = []
        for char in request.form.values():
            characters_list.append(char.capitalize())
        characters_list.remove("Next")
        for chars in characters_list:
            confirm_character_list.append(h.li(chars))
        for char in characters_list:
            session["account"][char] = []
            session.modified = True

        response = h.html(
            html_header("Confirm Characters"),
            h.body(
                h.h1("LOST ARK TRACKER"),
                h.h2("Do you confirm these are your character(s)?"),
                h.div(h.ul(class_='charList')(confirm_character_list)),
                h.form(action='/choosetasks')(
                    h.input(type='submit', value='Confirm', name='confirm_char')
                ),
                h.div(h.a(href='/delete')(h.button("Back")), onclick='return confirm("Are you sure?")')
            )
        )
    return str(response)

@app.route('/', methods=["GET", "POST"])
def homepage():
    """
    My home page. The user will choose the amount of characters they wish
    to track. There are attributes set so that the user cannot submit 0,
    negative or None characters. Automatically redirects to /tasktracker
    if the user has already stored their characters/tasks.
    """
    if 'account' in session:
        return redirect('/tasktracker')

    response = h.html(
        html_header("Lost Ark Tracker"),
        h.body(
            h.h1("LOST ARK TRACKER"),
            h.form(action='/characters')(
                h.label(for_='char_name')("How many characters do you want to track: "),
                h.br,
                h.input(type='number', name='totalchars', required=True, min='1', id='totalchars', class_='numOfChar'),
                h.br,
                h.input(type='submit', name='char_amount_btn', id='char_amount_btn', value='Next'),
            )
        )
    )
    return str(response)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
