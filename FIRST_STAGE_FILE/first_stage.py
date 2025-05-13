"""
first_stage.py

Author: Kenneth Koon

Date: 12/03/2024

I've included this file for comparison reasons. 

This file contains the code used for the first stage implementation of your
proposal. You should modify it so that it contains all the code required for
your MVP.
"""
from flask import Flask, request
import pyhtml as h
'''
Hello! I have prepared this first stages code for my project. I wasn't exactly
certain on what was to be completed, so I did as much as I possibly could.
I came across a wide variety of challenges while writing my code, so I have
made an extremely bare minimum product with some missing things to function at the
very least. I will annotate things that are missing that I need to learn more
to implement.
'''
app = Flask(__name__)
account = {}
total = 0

@app.route('/tasktracker', methods=["POST"])
def tasktracker():
    '''
    This route is the final destination of the web app. This is where all the
    inputted characters and their respective tasks are displayed with checkboxes
    for the user to manually check on and off.
    '''
    # TODO - Figure out how to display columns for each character.
    # Coded for only the first character at the moment.
    tasks = []
    headers = []
    track = []
    boxes = []
    if 'finish_btn' in request.form:
        for task in request.form.keys():
            tasks.append(task)
        tasks.pop()
        for character in account:
            headers.append(character)
            account[character] = tasks
        for objects in tasks:
            track.append(objects)
            track.append(h.br)
            boxes.append(h.input(type='checkbox', id='checkbox'))
            boxes.append(h.br)

    response = h.html(
        h.body(
            h.h1("LOST ARK TRACKER"),
            h.h2("This is your tracker! Click on the checkbox if you have completed the task!"),
            h.table(
                h.tr(
                    h.th(headers[0]),
                    h.th("Tasks")
                ),
                h.tr(
                    h.td(track),
                    h.td(boxes)
                )
            ),
            h.h3("Don't forget to untick at reset!")
        )
    )
    return str(response)

@app.route('/choosetasks', methods=["POST"])
def choosetasks():
    '''
    This route is where the user will select the tasks they wish to track for
    each of the characters they have inputted.
    '''
    # TODO - Allow choosing different tasks for each character.
    # At the moment, the selected tasks are applied to every character.
    if 'name_btn' in request.form:
        for char in request.form.values():
            account[char] = ""
        del account['Next']
        response = h.html(
        h.body(
            h.h1("LOST ARK TRACKER"),
            h.h3("Click this button for a list of tasks."),
            h.h3("You may choose the things you'd like to track."),
            h.form(action='/choosetasks')(
                h.input(type='submit', name='choosetasks', id='choosetasks', value='Choose Tasks')
            )
        )
    )

    # Below is the html display I would like to repeat for the length of the
    # users' characters. I would like it to be identical except for the header
    # that displays the character name. Not sure how to do this.
    # The character names are keys in a dictionary and I am unsure as to how
    # I can print them without the brackets and quotes.
    if 'choosetasks' in request.form:
            response = h.html(
                h.body(
                h.h1("LOST ARK TRACKER"),
                h.h3(f"Choose activities for: {account}"),
                h.form(action='/tasktracker')(
                    h.h3("DAILIES:"),
                    h.input_(type='checkbox', name='Una\'s Task', id='una'),
                    h.label(for_='una')(h.b("Una's Tasks")),
                    h.br,
                    h.input_(type='checkbox', name='Chaos Dungeon', id='chaos_d'),
                    h.label(for_='chaos_d')(h.b("Chaos Dungeons")),
                    h.br,
                    h.input_(type='checkbox', name='Guardian Raid', id='g_raid'),
                    h.label(for_='g_raid')(h.b("Guardian Raids")),
                    h.br,
                    h.br,
                    h.h3("WEEKLIES:"),
                    h.input_(type='checkbox', id='valtan', name='Valtan'),
                    h.label(for_='valtan')(h.b("Valtan")),
                    h.br,
                    h.input_(type='checkbox', id='vykas', name='Vykas'),
                    h.label(for_='vykas')(h.b("Vykas")),
                    h.br,
                    h.input_(type='checkbox', id='kakul_saydon', name='Kakul Saydon'),
                    h.label(for_='kakul_saydon')(h.b("Kakul Saydon")),
                    h.br,
                    h.input_(type='checkbox', id='brelshaza', name='Brelshaza'),
                    h.label(for_='brelshaza')(h.b("Brelshaza")),
                    h.br,
                    h.input_(type='checkbox', id='akkan', name='Akkan'),
                    h.label(for_='akkan')(h.b("Akkan")),
                    h.br,
                    h.input_(type='checkbox', id='kayangel', name='Kayangel'),
                    h.label(for_='kayangel')(h.b("Kayangel")),
                    h.br,
                    h.input_(type='checkbox', id='ivory_tower', name='Ivory Tower'),
                    h.label(for_='ivory_tower')(h.b("Ivory Tower")),
                    h.br,
                    h.br,
                    h.input(type='submit', id='finish_btn', name='finish_btn', value='Next')
                    )
                )
            )
    return str(response)

@app.route('/characters', methods=["POST"])
def characters():
    '''
    This route allows the user to enter the names of their characters.
    '''
    char_names = []
    if 'char_amount_btn' in request.form:
        total = int(request.form.get('totalchars', 0))
    # The amount of textboxes printed will depend on what the user typed in
    # the previous route.
    i = 1
    while i <= total:
        char_names.append(h.label(for_="char_names")(f"{i}."))
        char_names.append(h.input(type='text', name="char_names" + str(i), id='char_names', placeholder=f"Enter Character {i} Name"))
        char_names.append(h.br)
        char_names.append(h.br)
        i += 1
    response = h.html(
        h.h1("LOST ARK TRACKER"),
        h.h2("Enter your character names"),
        h.form(action='/choosetasks')(
            char_names,
            h.input(type='submit', name='name_btn', id='name_btn', value='Next')
        )
    )
    return str(response)

@app.route('/', methods=["GET", "POST"])
def homepage():
    """
    The landing page for your project. This is the first thing your users will
    see, so you should be careful to design it to be useful to new users.
    """
    # User may designate the amount of characters they wish to track.
    response = h.html(
        h.body(
            h.h1("LOST ARK TRACKER"),
            h.form(action='/characters')(
                h.label(for_='char_name')("How many characters do you want to track: "),
                h.input(type='number', name='totalchars', id='totalchars'),
                h.br,
                h.input(type='submit', name='char_amount_btn', id='char_amount_btn', value='Next'),
            )
        )
    )
    return str(response)


if __name__ == "__main__":
    app.run(debug=True)
