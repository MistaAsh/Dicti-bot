#including required modules to the program
import os
import requests
import json
import discord
import datetime

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome to my Discord server!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg == '$help':
        embedv = discord.Embed(title='Dicti\'s walkthrough', 
        color=0xFF5733,
        timestamp=datetime.datetime.utcnow())

        embedv.set_thumbnail(url = 'https://i.imgur.com/emVAdxH.jpg')

        embedv.add_field(name = '`$help`',
        value = 'Displays the list of commands supported by Dicti and the specific syntax need for the usage',
        inline = False)

        embedv.add_field(name = '`$dict <word>`',
        value = 'Displays information on the word used involving parameters such as definitions, synonyms, phonetics, etc.',
        inline = False)

        embedv.add_field(name = '`$urban <word>`',
        value = 'Displays information regarding the colloquial use of the word and the its different meanings under different contexts',
        inline = False)

        await message.channel.send(embed = embedv)

    # if msg.startswith('$urban'):
    #     word = msg.split('$urban ', 1)[1]

    #     response = requests.get("https://api.urbandictionary.com/v0/define?term=" + word)
    #     json_data = json.loads(response.text)

    #     deflist = json_data['list']
    #     n = len(deflist)

    #     if n > 0:
    #         deflist = sorted(deflist, key = lambda x: x['thumbs_up'], reverse = True)
    #         n = min(5, n)

    #         page = []





        
    #     else:
    #         noword = 'No meanings found'
    #         await message.channel.send(noword)

    if msg.startswith('$dict'):
        word = msg.split('$dict ', 1)[1]

        response = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/" + word)
        json_data = json.loads(response.text)

        if type(json_data) == list:
            n = len(json_data)

            page = []
            
            for i in range(n):
                embedv = discord.Embed(title = 'Dictionary ('+str(i+1)+'/'+str(n)+')', 
                description = json_data[i]['word'].title(), 
                color=0xFF5733,
                timestamp=datetime.datetime.utcnow()) 

                embedv.add_field(name = '\u200b', 
                value = '**Origin: **'+json_data[i]['origin'] +'\n' + '**Parts of Speech: **'+json_data[i]['meanings'][0]['partOfSpeech'],
                inline = False)

                embedv.add_field(name = '\u200b',
                value = '\u200b', 
                inline = False)

                embedv.add_field(name = 'Phonetics',
                value = 'Text: '+json_data[i]['phonetics'][0]['text'] + '\n' + 'Audio: '+json_data[i]['phonetics'][0]['audio'],
                inline = False)

                embedv.add_field(name = '\u200b',
                value = '\u200b', 
                inline = False)

                defs = json_data[i]['meanings'][0]['definitions']

                for j in range(len(defs)):
                    x = len(defs[j]['synonyms'])
                    y = len(defs[j]['antonyms'])

                    if x > 0 and y > 0:
                        embedv.add_field(name = 'Definition '+str(j+1),
                        value = defs[j]['definition'] + '\n' + 'Synonyms: ' + str(defs[j]['synonyms'][:min(x,5)]) + '\n' + 'Antonyms: ' + str(defs[j]['antonyms'][:min(y,5)]), 
                        inline = False) 
                    elif x > 0 and y == 0:
                        embedv.add_field(name = 'Definition '+str(j+1),
                        value = defs[j]['definition'] + '\n' + 'Synonyms: ' + str(defs[j]['synonyms'][:min(x,5)]), 
                        inline = False) 
                    elif x == 0 and y > 0:
                        embedv.add_field(name = 'Definition '+str(j+1),
                        value = defs[j]['definition'] + '\n' + 'Antonyms: ' + str(defs[j]['antonyms'][:min(y,5)]), 
                        inline = False) 
                    else:
                        embedv.add_field(name = 'Definition '+str(j+1),
                        value = defs[j]['definition'], 
                        inline = False)           

                embedv.add_field(name = '\u200b',
                value = '\u200b', 
                inline = False)     

                page.append(embedv)
            
            emb = await message.channel.send(embed = page[0])
            await emb.add_reaction("◀️")
            await emb.add_reaction("▶️")

            def check(reaction, user):
                return user == message.author

            k = 0 
            reaction = None

            while True:
                if str(reaction) == '◀️':
                    if k > 0:
                        k -= 1
                        await emb.edit(embed = page[k])
                elif str(reaction) == '▶️':
                    if k < n-1:
                        k += 1
                        await emb.edit(embed = page[k])

                try:
                    reaction, user = await client.wait_for('reaction_add', timeout = 30.0, check = check)
                    await emb.remove_reaction(reaction, user)
                except:
                    break
        
        else:
            noword = json_data['title']
            await message.channel.send(noword)

client.run(TOKEN)