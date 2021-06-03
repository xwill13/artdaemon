# daemonfunctions.py defines the non-command functions that the bot needs to run.
# Written by Xzavier Williams
# Contributions from Dan Dewaters

import random
import time


# Opens the file. Reads the file. Returns the value
# In the context of this application prev_member_index.txt holds a number that represents the last proctor's index
# within the discord.py array 'Memberlist'. Thus get_proctor will be called for the purpose of determining the
# last member of the guild to choose a challenge. It returns a simple number or integer.
def get_proctor():
    unum = read_text_file("prev_member_index.txt")
    unum = int(unum)
    if unum == '':
        unum = 0
    return unum


# Takes in the index of the user and increments by 1. Writes to prev_member_index.txt
def find_next_proctor(prev_proctor_index, guild_size):
    prev_proctor_index += 1
    if prev_proctor_index > (guild_size - 1):
        prev_proctor_index = 0
    f = open("prev_member_index.txt", "w")
    prev_proctor_index = str(prev_proctor_index)
    f.write(prev_proctor_index)
    f.close()


# A function that exists to check a member's willingness to participate in challenges. Checks to see if
# the user has the role "Challenger" and if so allows participation in the challenges. Consent is assumed
# to be false
def consentcheck(member):
    consents = False
    for role in member.roles:
        if role.name == "Challenger":
            consents = True

    return consents


# Works in combination with "find_next_proctor" to update the file "prev_member_index.txt" to reflect the newly selected
# proctor's index.
def set_procotor(ctx):
    # Get the index for the last known proctor
    prev_proc = get_proctor()
    print("Last member position was " + str(prev_proc))

    # determine guild size
    guildsize = len(ctx.guild.members)
    print("Guild has " + str(guildsize) + " members")

    # set new member position in the text file, effectively selecting the next challenge selector
    find_next_proctor(prev_proc, guildsize)

    # set new member position in the variable
    prev_proc = get_proctor()
    print("Increased member position is " + str(prev_proc))

    return prev_proc


# Define the perfect code for a partner picking function
# contributed by DAN
# edited by Xzavier. edits make use of the newly discovered guild.members attribute, rather than
# needing to read an external file for that information.

def partner_picker(memberlist, msg="{} will give their prompt to {}"):
    # Open text file of names
    # file_object = open(fileName, "r")
    names = []

    # create dictionary
    namesarray = []

    # create an array of user names
    for i in memberlist:
        if consentcheck(i):
            names.append(i.name)

    print('Names')
    print(names)
    # Set rng seet, shuffle order of names
    random.seed(time.time())
    random.shuffle(names)
    print(names)

    # Loop through list, each person's partner is the next person in the list
    for i in range(len(names)):
        namesarray.append(msg.format(names[i - 1], names[i]))

    # Spit out the array

    return namesarray


# Opens a text file, reads it, and returns a variable containing the output as a string.
def read_text_file(filename):
    file = open(filename)
    file_as_string = file.read()
    file.close()

    return file_as_string

# A function designed to ensure that the server has the 'Challenger' role. If there is no challenger role it will be
# added. Lastly the function returns the ID of the challenger role for use in assigning the role to guild members
def confirm_challenger_role(roles, ctx):
    print('Checking for Challenger role')

    # Preemptively setting variables
    missing_challenger_role = True
    role_id_no = 0

    # Loop through all guild roles to see if 'Challenger exists'
    for x in roles:
        if x.name == 'Challenger':
            missing_challenger_role = False
            role_id_no = x.id

    # Create it if it doesn't
    if missing_challenger_role:
        print('The Server does not have the **Challenger** Role')
        ctx.guild.create_role('Challenger')
    else:
        print('Role Present')

    # Loop through all existing roles and get the ID of the 'Challenger' role
    for y in roles:
        if y.name == 'Challenger':
            role_id_no = y.id

    return role_id_no


# A function to be called when writing a new challenge to the challengestore.txt file
# Works in tandem with the setchallenge command
def set_new_challenge(challenge_string):
    # Opens the file
    f = open('challengestore.txt', 'w')

    # Strips the command from the text and writes the resulting string to the challenge storage file.
    # Then close the file.
    f.write(challenge_string.replace('+chalset ', ''))
    f.close()
