# daemonfunctions.py
# Written by Xzavier Williams
import discord
from discord.ext import commands
from daemonfunctions import *

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='+', intents=intents)


@client.event
async def on_ready():
    print('Art Daemon is online')


@client.command()
async def challenge(ctx):
    print('command get')
    # Check and make sure the 'Challenger' role exists. If it doesn't add it
    confirm_challenger_role(ctx.guild.roles, ctx)

    # Preemptively set consent for use in the consent loop.
    consent = False

    # Define the actual size of the array (counting zero as a position) and set the limitcounter to 0. This is used
    # To stop the upcoming while loop from running forever
    limit = len(ctx.guild.members) - 1
    limitcount = 0

    # Loop through all users until we land on one that that consents to participate. Consent is determined through role
    # membership via consentcheck()
    while not consent:

        # Load the proposed next proctor's index number into a variable. The index is the potential proctor's position
        # within the guild.members array
        potential_index = set_procotor(ctx)

        # Load the user object of the potential proctor into a variable
        user = ctx.guild.members[potential_index]

        # Load the answer for consent of the potential proctor into a variable
        consent = consentcheck(user)

        # Increment the limitcount to prevent endless looping
        limitcount += 1

        # If this statement triggers it should mean that there are no willing participants.
        if limitcount > limit:
            print("No participants found")

            await ctx.send('There are no willing participants')
            return

    # Generate and send a message stating who the next proctor will be
    message = "This week " + user.name + " selects the challenge"
    await ctx.send(message)


@client.command()
async def remind(ctx):
    print('command get')

    # Read the current challenge out of the text file and into a variable. Strip the command out of the text.
    current_challenge = read_text_file('challengestore.txt')
    current_challenge = current_challenge.replace('+setchallenge', '')

    # Get the current proctor's index and use that value to store the member's name in a variable. Finally use previously
    # Collected data to generate and send the reminder message
    proctor_index = get_proctor()
    member = ctx.guild.members[proctor_index].name
    message = "This week " + member + " selected the challenge \n" \
                                      "The challenge presented is: \n" + current_challenge
    await ctx.send(message)


@client.command()
async def tome(ctx):
    print(read_text_file('tome_message.txt'))

    # Reads the tome_message file out into a discord message
    await ctx.send(read_text_file('tome_message.txt'))


@client.command()
async def join(ctx):
    # Check to make sure the challenger role exists and if not, add it. Also utilizes the fact that the role ID of
    # Challenger is returned from 'confirm_challenger_role' to store said ID into a variable
    role_id = confirm_challenger_role(ctx.guild.roles, ctx)

    # Check to see what the command user's consent status is.
    consent = consentcheck(ctx.message.author)

    # Use the role ID to grab the actual role object and store it in a variable. If the user has the role, remove it.
    # Elsewise add it.
    role = ctx.guild.get_role(role_id)
    if consent:
        await ctx.message.author.remove_roles(role)
        print('Removed Role')
        await ctx.send(ctx.message.author.name + ' has quit the challenge')

    else:
        await ctx.message.author.add_roles(role)
        print('Added role')
        await ctx.send(ctx.message.author.name + ' has joined the challenge')


@client.command()
async def setchallenge(ctx):
    # Store command message into a variable
    challs = ctx.message.content
    challs = str(challs)

    # Write new challenge to a file
    set_new_challenge(challs)

    print(ctx.message.content)
    await ctx.send('The challenge has been updated')


@client.command()
async def partners(ctx):
    # Run partner picker to build and array of partner groups
    group_array = partner_picker(ctx.guild.members)

    # Print those groups we were talking about earlier to a discord message
    for x in group_array:
        await ctx.send(x)


@client.command()
async def info(ctx):
    print(read_text_file('artdaemon_info.txt'))

    # Reads info file out into a discord message
    await ctx.send(read_text_file('artdaemon_info.txt'))


client.run('')
