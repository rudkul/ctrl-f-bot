import discord
import asyncio
import time

# *A<number> <answer>
def processStr(msg):
  return [int(msg[2:msg.find(" ")]), msg[msg.find(" ") + 1:]]

def getTimeStr(timeInt):
  hours, rem = divmod(timeInt, 3600)
  minutes, seconds = divmod(rem, 60)
  return ("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))

client = discord.Client()

# Add clues and their answers to these lists
clues = ["\nHero or tyrant,\nspreader  of Liberté, égalité, fraternité\nOr replacer of monarchy with dictatorship\nShort or average height for his time","\nBeers, Sausage and October\nA rarity: A Fatherland\n20th century unleashers of Horror\nWhen in doubt, invade Poland","\nWhen abbreviated, name-sake of our dreaded exams\nOrg shared by an entire continent\nObserves our Living Planet through Programmes\nIn space, the third most prominent","\nCall Him by Your Name, but X = ‘A’\nEarth’s greatest hope, budgets slashed\nFrom this planet, they get away\nMankind’s giant leaps well dispatched","\nRemove pac, and you’d see heaven\nClimb on board for the ride, and you’d get there\n3 minutes and 24 seconds, that's how long\nHumanity’s rockets, been launching strong","\nBeen to space but not in the race\nToyota Volkswagen step aside\nRun by reddit’s most recognizable face\n0 to 60, one point nine nine","\nMeet its maker, you can not\nKeys most private, loss spells doom\nConcerns, will environment rot\nIncrements gained, alone in a room"]
answers = ["napoleon", "germany","europeanspaceagency","nasa","spacex","tesla,inc.","bitcoin"]

# The points go here
treasure = 5 # 0_0
# Store the points the time taken(in seconds) in the following
# dictionary, keep the times sorted in acending order
# The following awards the points as follows
# 1 minute -> 500, 5 minutes -> 200, 10 minutes -> 100
award_points= {
  1200  : 8, 
  1800 : 6,
  2100 : 4,
  2400 : 2
}
# Points added if they solve the question in more time than any of the above Conditions
points_per_question = 1 # ;-;

# Victory Message
win_message = "You won!"

# Start message
begin_message = "Here is the link to start you off\n\nhttps://en.wikipedia.org/wiki/French_Revolution\nGood luck!"

# Channel ID's
channels = [x for x in range(1,200)]
num_channels = len(channels)

# Admin Channel id
admin_channel = 860619043214721065

# States for each channel
states = {channel : 0 for channel in channels}
# Times for each channel, stores each question time seperately
times = {channel : 0 for channel in channels}

# Points for each channel
points = {channel : 0 for channel in channels}

# TIme Block
block = {channel : False for channel in channels}

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  global states, clues, answers, channels
  c_id = str(message.channel)
  if message.channel.id == admin_channel:
    if message.content == '*allpoints':
      strlist = [str(x) + "---" + str(points[x]) for x in (channels) if points[x] != 0]
      await message.channel.send("POINTS\n" + "\n".join(strlist))
      return

  try:
    c_id = int(c_id[:c_id.find("_")])
  except ValueError:
    return


  if message.author == client.user and c_id not in channels:
    return


  if message.content.startswith('*hello'):
    await message.channel.send('Hello!')
    return


  if message.content.startswith("*A"):
    if times[c_id] == 0:
      await message.channel.send("Please run *start before running this command.")
      return
    
    if block[c_id]:
      await message.channel.send("You cant answer anymore, 40 minutes is up!\nRun points")
      return
    try:
      num, ans = processStr(message.content)
    except ValueError:
      await message.channel.send("Something went wrong, @ the event managers on discord.")
      return
    
    ans = ans.replace(" ","")
    # Conditions to check if answer number is valid
    if num > len(clues):
      await message.chann.send("There are only " + str(len(clues)) + " clues!")
      return

    if num < 1:
      await message.channel.send("Clue numbers are strictly positive integers")
      return

    # Check if it is legal to answer the current clue
    if num > (states[c_id] + 1):
      await message.channel.send("Answer the previous clues first, you need to answer clue:\n" + str(states[c_id] + 1) + ") " + clues[states[c_id]])
      return
    
    if num < (states[c_id] + 1):
      await message.channel.send("You have answered the clue already!")
      return
    
    # It is legal, check if the answer is correct
    if ans.lower() == answers[states[c_id]].lower():
      # Add points
      points[c_id] += points_per_question

      # Increase the state(question number)
      states[c_id] += 1
      
      # Check win condition
      if states[c_id] == len(clues):
        # Stop time
        times[c_id] = time.time() - times[c_id]
        # Give them the treasure points
        points[c_id] += treasure

        #Give them bonus based on time
        for et in award_points.keys():
          if times[c_id] <= et:
            points[c_id] += award_points[et]
            break
        
        # Congratulate them
        await message.channel.send("Took: " + getTimeStr(times[c_id]) + "\nPoints accumulated: " + str(points[c_id]) + "\n" + win_message)
        return
      
      # Tells them nice, and shows them the next clue
      await message.channel.send("That is the correct answer.\nHere is the next clue: " + clues[states[c_id]])
    else:
      await message.channel.send("That is wrong.")
    
    return
  

  # Start the game
  if message.content == "*start":
    if not times[c_id] == 0:
      await message.channel.send("Already started the game")
      return
    times[c_id] = time.time()
    await message.channel.send(begin_message)
    await asyncio.sleep(2400)
    block[c_id] = True
    await message.channel.send("---------------Cant answer anymore!---------------")
    return


  # Get the elapsed time
  if message.content == "*time":
    if times[c_id] == 0:
      await message.channel.send("Please run *start before runing this command.")
      return
    et = time.time() - times[c_id]
    await message.channel.send("Elapsed time: " + getTimeStr(et))
    return


  # Get the points
  if message.content == "*points":
    if times[c_id] == 0:
      await message.channel.send("Please run *start before runing this command.")
      return
    await message.channel.send("Points: " + str(points[c_id]))
    return


  # Display the clues
  if message.content == "*clues":
    if times[c_id] == 0:
      await message.channel.send("Please run *start before runing this command.")
      return
    todisp = [str(z) + ")  " + x + "\n" + y for x,y,z in zip(
      clues[:states[c_id]],
      answers[:states[c_id]],
      range(1, states[c_id] + 1)
    )]
    if states[c_id] < len(clues):
      todisp.append(str(states[c_id] + 1) + ")  " + clues[states[c_id]])
    await message.channel.send("Here are the clues(and answers) so far:\n" + "\n".join(todisp))
    return

  # Display the win_message again just in case
  if message.content == "*win":
    if states[c_id] == len(clues):
      await message.channel.send(win_message)
    return



client.run('ODU0MjQ0OTg4NzQ0NzYxMzY0.YMhHpA.Bq3gL6Z3Ufer_4DRTrWZkrqOnQc')