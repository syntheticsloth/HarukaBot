import asyncio
import re
from typing import Optional

import validators

import discord
from discord.ext import commands
from discord.commands import Option, OptionChoice, SlashCommandGroup, user_command
from discord.commands.permissions import default_permissions

from formatting.embed import gen_embed, embed_splitter
from formatting.constants import THUMB
from __main__ import log, db


class Tiering(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.refill_running = {}

    @staticmethod
    def has_modrole():
        async def predicate(ctx):
            document = await db.servers.find_one({"server_id": ctx.guild.id})
            if document['modrole']:
                role = discord.utils.find(lambda r: r.id == document['modrole'], ctx.guild.roles)
                return role in ctx.author.roles
            else:
                return False

        return commands.check(predicate)

    guides = SlashCommandGroup('guide', 'Commands to post various tiering guides',
                               default_member_permissions=discord.Permissions(manage_messages=True))

    @guides.command(name='carpal-avoidance',
                    description='Generates a guide for avoiding Carpal Tunnel or RSI')
    @default_permissions(manage_messages=True)
    async def vsliveguide(self,
                          ctx: discord.ApplicationContext,
                          channel: Option(discord.SlashCommandOptionType.channel,
                                          ('Channel to post guide in. If not specified, '
                                           'will post in current channel'),
                                          required=False)):
        await ctx.interaction.response.defer()
        if channel:
            dest_channel = channel
        else:
            dest_channel = ctx.interaction.channel
        embed = gen_embed(
            name=f"{ctx.guild.name}",
            icon_url=ctx.guild.icon.url,
            title='Carpal Tunnel & Tiering Wellness',
            content=('Graciously created by **Aris/Nio**, originally for PRSK, edited by **Neon**'
                     '\n***Disclaimer: This is not medical advice. This is for educational purposes only and is my'
                     " (aris') research and does not replace going to the doctor.***"))
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        embed = gen_embed(
            title="What is Carpal Tunnel Syndrome/RSI?",
            content=('**Carpal Tunnel Syndrome** is the irritation of the median nerve within the carpal tunnel at the'
                     ' base of your hand. When the nerve becomes irritated in this region due to pressure, inflammation'
                     ', and/or stretching (ie gaming), symptoms are likely to occur.\n\nRepetitive quick movements over'
                     ' long periods of time (ie, tiering) can damage the carpal tunnel nerve in your wrists. This may'
                     ' cause numbness and weakness in your hands over long periods of time, which can become'
                     ' permanent.\n\n**Repetitive Strain Injury (RSI)** is damage damage to your muscles, tendons or'
                     ' nerves caused by repetitive motions and constant use. Anyone can get a RSI.'))
        embed.set_footer(text=('https://esportshealthcare.com/carpal-tunnel-syndrome/\n'
                               'https://my.clevelandclinic.org/health/diseases/17424-repetitive-strain-injury'))
        await dest_channel.send(embed=embed)
        embed = gen_embed(
            title="Symptoms of Carpal Tunnel Syndrome/RSI",
            content=('🔹 Feelings of pain or numbness in your fingers\n'
                     '🔹 Weakness when gripping objects with one or both hands\n'
                     '🔹 "Pins and needles" or swollen feeling in your fingers\n'
                     '🔹 Burning or tingling in the fingers, especially the thumb, index, and middle fingers\n'
                     '🔹 Pain or numbness that is worse at night\n\nIf you ever feel pain, **TAKE A BREAK!**'))
        embed.set_footer(text='https://www.hopkinsmedicine.org/health/conditions-and-diseases/carpal-tunnel-syndrome')
        await dest_channel.send(embed=embed)
        embed = gen_embed(
            title="Before Playing",
            content=('Below is a helpful guide for warming up. Other guides for Gamer Stretches™ probably exist on the'
                     ' internet. If you have one you like, keep following it.\n\nTake off any wristwatches before'
                     ' playing - wearing them worsens carpal tunnel.\n\nGrab a jug of water or other drinks to keep'
                     ' hydration within arm\'s reach.'))
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        await dest_channel.send(content='https://esportshealthcare.com/gamer-warm-up/')
        embed = gen_embed(
            title="While Playing",
            content=('**Try to keep good posture.**\nTyping ergonomics logic likely applies here.\n'
                     '🔹 Consider playing on index fingers; it\'s easier on your wrists. Put your phone or tablet flat'
                     ' on the table, and tap on it as if it was a keyboard.\n'
                     '🔹 Position your wrist straight/aligned and neutral, as if you were playing piano.\n'
                     '🔹 Try to look down at your screen with your eyes instead of moving your head.'
                     ' You may need to perform neck stretches if your neck hurts.'))
        embed.set_image(url='https://files.s-neon.xyz/share/unknown.png')
        embed.add_field(name='Keep your hands warm',
                        value='Play in a warm environment - hand pain and stiffness is more likely in a cold one.',
                        inline=False)
        embed.add_field(name='Ideally, your screen should be at eye level',
                        value=('I think theoretically the best way to accomplish this is to cast your phone/tablet to'
                               'a monitor/TV and play while looking straight at the monitor you casted to instead of'
                               ' your device screen.'),
                        inline=False)
        embed.set_footer(text=('Exercises and tips in this section from:\n'
                               'https://youtu.be/EiRC80FJbHU\n'
                               'https://bit.ly/3lD5ot9\n'
                               'https://bit.ly/38IZeVI'))
        await dest_channel.send(embed=embed)
        embed = gen_embed(
            title="Routines",
            content=('**Every 20 minutes**, do the 20-20-20 rule: look at something 20 feet away, for about 20 seconds,'
                     ' to give your eyes a break. This is easily done while menuing in between songs.\n\n'
                     '**Every 60 minutes**, consider taking a 5 minute break to rest your hands.\n\n'
                     '**Every 2-3 hours**, shake out your hands and perform some hand/finger exercises. See below for'
                     ' an instructional video.\n\n'
                     '**1-2 times a day**, run your hands gently under warm water. Move your hands up and down under'
                     ' the water.\n\n'
                     '**If your hands hurt, take breaks more often.**'))
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        await dest_channel.send(content='https://youtu.be/EiRC80FJbHU?t=85')
        embed = gen_embed(
            title="After Playing",
            content=('Below is a helpful guide for post-game stretches. Again, other guides for Gamer Stretches™'
                     ' probably exist on the internet. If you have one you like, keep following it.'))
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        await dest_channel.send(content='https://esportshealthcare.com/gamer-stretches/')
        await ctx.interaction.followup.send(embed=gen_embed(
            title='Carpal Avoidance Guide',
            content=f'Carpal Tunnel & RSI Avoidance guide posted in {dest_channel.mention}'),
            ephemeral=True)

    @guides.command(name='cheerful-carnival',
                    description='Generates a guide for Cheerful Carnival events')
    @default_permissions(manage_messages=True)
    async def marathonguide(self,
                          ctx: discord.ApplicationContext,
                          channel: Option(discord.SlashCommandOptionType.channel,
                                          ('Channel to post guide in. If not specified, '
                                           'will post in current channel'),
                                          required=False)):
        await ctx.interaction.response.defer()
        if channel:
            dest_channel = channel
        else:
            dest_channel = ctx.interaction.channel
        embed = gen_embed(
            name=f"{ctx.guild.name}",
            icon_url=ctx.guild.icon.url,
            title='Cheerful Carnival Filling Info',
            content=("Adapted from Azufire's \"FILLER 101 [Cheerful Carnival]\" guide from R8SS."))
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        embed = gen_embed(
            title="HOW TO MAKE A TEAM / SKILLS 101",
            content=("__ONLY 2 THINGS MATTER__: Max skill bonus (biggest score% boost) and TALENT\n\n"
                     "__BEST SKILLS (IN ORDER)__ *(example values are skill lvl 1, 4\* cards)*:\n"
                     "1. **Unit Scorer [UScorer]** NEEDS ALL CARDS FROM SAME UNIT (yes, VS works)\n"
                     "```\"Score boost 80% for 5 seconds; For every member of [UNIT] in your team, there will be an extra score boost of 10%, with a maximum boost of 130%\"```\n"
                     "2. **Life Scorer [LScorer]**\n"
                     "```\"Score boost 70% if life is under 800 (100% if life is over 800) for 5 seconds. For every 10 life, score is increased by +1% (up to 120%)\"```\n"
                     "3. **Perfect Scorer [PScorer]**\n"
                     "```\"110% score boost for 5 seconds for PERFECTs only.\"```\n"
                     "4. **Scorer**\n"
                     "```\"100% score boost for 5 seconds.\"```\n"
                     "5. **Healer (OK ONLY IN CC)**\n"
                     "```\"Recover 350 life; 80% score boost for 5 seconds.\"```\n"
                     "**NOTES**\n"
                     "Leader trigger is the most powerful (furthest card on left) - put your strongest skill card here\n\n"
                     "Other cards still trigger their skills in song - use your best skill cards in every team slot\n\n"
                     "DON'T USE Accuracy Scorer / Combo Scorer [AScorer/GScorer] 9/10 TIMES\n"
                     "```\"70% score boost for 5 seconds (120% until GREAT or lower)\"```\n"
                     "Tierers have skill issue and can't all perfect combo all the time\n\n"
                     "Use only if your tierers are built different/say it*s OK"))
        embed.set_image(url='https://svenxiety.xyz/junk/fill_best.png')
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        embed = gen_embed(
            title="HEALERS? IN MY TIERING ROOM?",
            content=("In CC, you get more points if you are at or above max HP at the end of a song. Most rooms will want 1 player with a HEALER lead, or BIRTHDAY card if tierers have skill issue/are dying (birthday cards = stronger heal, weaker score boost)."))
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        embed = gen_embed(
            title="TALENT LEVEL? SANDBAGGING?",
            content=("CC means you need to match with an enemy team of a similar talent level. If your lobby is too strong, matchmaking will take longer and matches are harder to win because you will be fighting other high talent teams.\n\n"
                     "Some fillers will bring the lowest level cards they can (\"sandbag\") to either barely hit 150k talent for pro rooms, OR as low as possible talent (while still having good skills) for gen rooms."))
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        embed = gen_embed(
            title="WHAT'S AN ISV / HOW DO I CALCULATE?",
            content=("**ISV:** Internal Skill Value - used to measure team strength / order rooms\n\n"
                     "First value = leader skill value (number in front of %)\n\n"
                     "Second value = sum of ALL skill values in team\n\n"
                     "Ex: if you have a team of all 4* PScorers with base skill 110 → ISV = 110 / 550"))
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        embed = gen_embed(
            title="WHAT'S ROOM ORDER?",
            content=("Because player skills trigger in a specific order in multi lives based on player order in the room, some player skills will be more important than others.\n\n"
                     "For high tier runs with room orders, managers will tell you what team to use and what room slot to go in (P1 - P5).\n\n"
                     "Join when your number is called. Then when you load into the lobby, call the next number to join.\n\n"
                     "However, for CC, since matchmaking is frequently unstable, prioritize getting matches over maintaining room order. In the case of a disconnect/disband, simply rejoin as fast as possible to return to matchmaking."))
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        await ctx.interaction.followup.send(embed=gen_embed(
            title='Cheerful Carnival Filling Info',
            content=f'Cheerful Carnival guide posted in {dest_channel.mention}'),
            ephemeral=True)

    @guides.command(name='efficiency',
                    description='Generates an efficiency guide for tiering')
    @default_permissions(manage_messages=True)
    async def efficiencyguide(self,
                              ctx: discord.ApplicationContext,
                              channel: Option(discord.SlashCommandOptionType.channel,
                                              ('Channel to post guide in. If not specified, '
                                               'will post in current channel'),
                                              required=False)):
        await ctx.interaction.response.defer()
        if channel:
            dest_channel = channel
        else:
            dest_channel = ctx.interaction.channel
        embed = gen_embed(
            name=f"{ctx.guild.name}",
            icon_url=ctx.guild.icon.url,
            title='Tiering Etiquette and Efficiency',
            content='Efficiency guidelines adapted from Alpha Gathering, with additions by synthsloth.')
        # embed.set_image(url='https://files.s-neon.xyz/share/bandori-efficiency.png')
        await dest_channel.send(embed=embed)
        embed = gen_embed(
            title='Fast Menuing',
            content=("After completing a song, tap through the buttons on the bottom right to skip through the "
                     "screens as fast as you can.\n\n"
                     "The same applies for the song selection screen in Marathons and the ready up screen in Cheerful "
                     "Carnivals.\n\n"
                     "If you need to type something in chat, try to menu first to keep things going smoothly."))
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        # await dest_channel.send(content='https://twitter.com/Binh_gbp/status/1106789316607410176')
        embed = gen_embed(
            title='Energy Refilling',
            content=("For **Marathon** events, refill during the song selection screen.\n\n"
                     "For **Cheerful Carnival** events, refill during matchmaking."))
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        embed = gen_embed(
            title='Doormatting',
            content=("Doormatting is when you play on Easy, hit enough notes in a song, and then stop playing. This is for **fillers "
                     "only**.\n\n"
                     "You must hit **at least 50% of the notes** in a song, otherwise you will get a conduct warning.\n\n"
                     "For Hitorinbo Envy during Marathon events, it's suggested to hit all of the notes up until the end of "
                     "fever chance (43 notes) before going afk.\n\n"
                     "For Cheerful Carnival events, since song selection is random, ensure you hit at least half of the notes "
                     "in the selected song before you stop playing."))
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        embed = gen_embed(
            title='Room Swaps',
            content=("Have the room code typed in beforehand.\n\n"
                     "Join as soon as someone says the room is open (\"op\"). You can also spam the join button "
                     "when they say \"sc\".\n\n"
                     "If there is room order, pay attention to the spot you've been assigned and be ready to join as soon as "
                     "someone types it in chat (P2, P3, P4, P5 or 2, 3, 4, 5).\n\n"
                     "If you are P1, create the room beforehand. Try rolling codes until you get one that is easy to type.\n\n"
                     "For Marathon events, have the song Hitorinbo Envy selected from a Solo Show before you join to prevent "
                     "accidentally selecting the wrong song. Do not rely on selecting \"Recommended\" each round.\n\n"
                     "Make sure you're using the correct team."))
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        embed = gen_embed(
            title='Don\'t All Perfect',
            content=("Try not to All Perfect (AP). The messages \"Full Combo\" And \"Show Cleared\" have the same animation "
                     "length at the end of a song. However, \"ALL PERFECT\" has a longer animation. Every second counts!"))
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        embed = gen_embed(
            title='Communication',
            content=("Try to have another device to communicate with others, otherwise use in-game stamps if you can't.\n\n"
                     "If the runner or a manager is in voice chat (VC), you can also join that.\n\n"
                     "Let the other people know if you need to leave a couple of rounds prior to doing so."))
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        embed = gen_embed(
            title='Fill Scheduling',
            content=("Please only sign up for hours you are able to do. Don't sign up for super long shifts if you cannot "
                     "make it through.\n\n"
                     "Expect to have to stay for the **entirety** of your shift.\n\n"
                     "In case you're unable to make it to your shift or need to end your shift early, let the managers and runners "
                     "know as soon as possible so a replacement can be found."))
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        embed = gen_embed(
            title='Rank Checking',
            content=("Do not leave the room to check your rank. Use Nenerobo to check your rank, leaderboard, cutoffs, etc.\n\n"
                     "Link your Discord account with Nenerobo prior to entering the room. Type /rank to begin the linking process.\n\n"))
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        embed = gen_embed(
            title='Other Considerations',
            content=("Make sure you have a stable internet connection before entering a room. Disconnects will disrupt room order"
                     "and may lead to a conduct warning.\n\n"
                     "Make sure your device is fully charged and/or plugged in to avoid disruptions due to low battery "
                     "notifications.\n\n"
                     "Enable \"Do Not Disturb\" to avoid distractions.\n\n"
                     "For iOS users, utilize \"Guided Access\" to avoid accidentally exiting the app while playing."))
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        await ctx.interaction.followup.send(embed=gen_embed(
            title='Efficiency Guide',
            content=f'Tiering etiquette and efficiency guide posted in {dest_channel.mention}'),
            ephemeral=True)

    @guides.command(name='fill-teams',
                    description='Generates a guide for creating fill teams')
    @default_permissions(manage_messages=True)
    async def marathonguide(self,
                          ctx: discord.ApplicationContext,
                          channel: Option(discord.SlashCommandOptionType.channel,
                                          ('Channel to post guide in. If not specified, '
                                           'will post in current channel'),
                                          required=False)):
        await ctx.interaction.response.defer()
        if channel:
            dest_channel = channel
        else:
            dest_channel = ctx.interaction.channel
        embed = gen_embed(
            name=f"{ctx.guild.name}",
            icon_url=ctx.guild.icon.url,
            title='Fill Teams Guide',
            content=("Adapted from Alpha Gathering's fill teams guide and Azufire's \"FILLER 101\" guides from R8SS."))
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        embed = gen_embed(
            title="HOW TO MAKE A TEAM / SKILLS 101",
            content=("__BEST SKILLS (IN ORDER)__ *(example values are skill lvl 1, 4\* cards)*:\n"
                     "1. **Unit Scorer [UScorer]** NEEDS ALL CARDS FROM SAME UNIT (yes, VS works)\n"
                     "```\"Score boost 80% for 5 seconds; For every member of [UNIT] in your team, there will be an extra score boost of 10%, with a maximum boost of 130%\"```\n"
                     "2. **Life Scorer [LScorer]**\n"
                     "```\"Score boost 70% if life is under 800 (100% if life is over 800) for 5 seconds. For every 10 life, score is increased by +1% (up to 120%)\"```\n"
                     "3. **Perfect Scorer [PScorer]**\n"
                     "```\"110% score boost for 5 seconds for PERFECTs only.\"```\n"
                     "4. **Scorer**\n"
                     "```\"100% score boost for 5 seconds.\"```\n"
                     "5. **Healer (OK ONLY IN CC)**\n"
                     "```\"Recover 350 life; 80% score boost for 5 seconds.\"```\n"
                     "**NOTES**\n"
                     "Leader trigger is the most powerful (furthest card on left) - put your strongest skill card here\n\n"
                     "Other cards still trigger their skills in song - use your best skill cards in every team slot\n\n"
                     "DON'T USE Accuracy Scorer / Combo Scorer [AScorer/GScorer] 9/10 TIMES\n"
                     "```\"70% score boost for 5 seconds (120% until GREAT or lower)\"```\n"
                     "Tierers have skill issue and can't all perfect combo all the time\n\n"
                     "Use only if your tierers are built different/say it*s OK"))
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        embed = gen_embed(
            title="Best Fill Team",
            content=("Your regular Marathon fill team. Focus on maximizing your ISV here."))
        embed.set_image(url='https://svenxiety.xyz/junk/fill_best.png')
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        embed = gen_embed(
            title="Fill Team <180k Talent (Pro Room Sandbag)",
            content=("Your best possible fill team while staying under 180k talent. This is used for sandbagging in Pro rooms during CC events.\n\n"
                     "Unleveled 4\* cards are useful here, but 3\*, 2\* and 1\* cards can be swapped in as well. Prioritize scorer abilities."))
        embed.set_image(url='https://svenxiety.xyz/junk/fill_sb1.png')
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        embed = gen_embed(
            title="Fill Team <120k Talent (Gen Room Sandbag)",
            content=("Your best possible fill team while staying under 120k talent. This is used for sandbagging in Gen rooms during CC events.\n\n"
                     "Unleveled 4\* cards are useful here, but 3\*, 2\* and 1\* cards can be swapped in as well. Prioritize scorer abilities and try to get talent as low as possible."))
        embed.set_image(url='https://svenxiety.xyz/junk/fill_sb2.png')
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        embed = gen_embed(
            title="Sandbag Heal Team",
            content=("This team should be similar to the previous sandbag team, but with a Healer lead. Aim for less than 120k talent. Only your leader needs to be a Healer.\n\n"
                     "Use a regular Healer rather than a Birthday Healer, as regular Healers provide higher score boost."))
        embed.set_image(url='https://svenxiety.xyz/junk/fill_hsb.png')
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        await ctx.interaction.followup.send(embed=gen_embed(
            title='Fill Teams Guide',
            content=f'Fill teams guide posted in {dest_channel.mention}'),
            ephemeral=True)

    @guides.command(name='marathon',
                    description='Generates a guide for Marathon events')
    @default_permissions(manage_messages=True)
    async def marathonguide(self,
                          ctx: discord.ApplicationContext,
                          channel: Option(discord.SlashCommandOptionType.channel,
                                          ('Channel to post guide in. If not specified, '
                                           'will post in current channel'),
                                          required=False)):
        await ctx.interaction.response.defer()
        if channel:
            dest_channel = channel
        else:
            dest_channel = ctx.interaction.channel
        embed = gen_embed(
            name=f"{ctx.guild.name}",
            icon_url=ctx.guild.icon.url,
            title='Marathon Filling Info',
            content=("Adapted from Azufire's \"FILLER 101\" guide from R8SS."))
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        embed = gen_embed(
            title="HOW TO MAKE A TEAM / SKILLS 101",
            content=("__ONLY 2 THINGS MATTER__: Hit 150k talent and max skill bonus (biggest score% boost)\n\n"
                     "__BEST SKILLS (IN ORDER)__ *(example values are skill lvl 1, 4\* cards)*:\n"
                     "1. **Unit Scorer [UScorer]** NEEDS ALL CARDS FROM SAME UNIT (yes, VS works)\n"
                     "```\"Score boost 80% for 5 seconds; For every member of [UNIT] in your team, there will be an extra score boost of 10%, with a maximum boost of 130%\"```\n"
                     "2. **Life Scorer [LScorer]**\n"
                     "```\"Score boost 70% if life is under 800 (100% if life is over 800) for 5 seconds. For every 10 life, score is increased by +1% (up to 120%)\"```\n"
                     "3. **Perfect Scorer [PScorer]**\n"
                     "```\"110% score boost for 5 seconds for PERFECTs only.\"```\n"
                     "4. **Scorer**\n"
                     "```\"100% score boost for 5 seconds.\"```\n"
                     "5. **Healer (BOOOOO)**\n"
                     "```\"Recover 350 life; 80% score boost for 5 seconds.\"```\n"
                     "**NOTES**\n"
                     "• Leader trigger is the most powerful (furthest card on left) - put your strongest skill card here\n\n"
                     "• Other cards still trigger their skills in song - use your best skill cards in every team slot\n\n"
                     "• DON'T USE Accuracy Scorer / Combo Scorer [AScorer/GScorer] 9/10 TIMES\n"
                     "```\"70% score boost for 5 seconds (120% until GREAT or lower)\"```\n"
                     "Tierers have skill issue and can't all perfect combo all the time\n\n"
                     "Use only if your tierers are built different/say it's OK"))
        embed.set_image(url='https://svenxiety.xyz/junk/fill_best.png')
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        embed = gen_embed(
            title="WHAT'S AN ISV / HOW DO I CALCULATE?",
            content=("**ISV:** Internal Skill Value - used to measure team strength / order rooms\n\n"
                     "First value = leader skill value (number in front of %)\n\n"
                     "Second value = sum of ALL skill values in team\n\n"
                     "Ex: if you have a team of all 4* PScorers with base skill 110 → ISV = 110 / 550"))
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        embed = gen_embed(
            title="WHAT'S ROOM ORDER?",
            content=("Because player skills trigger in a specific order in multi lives based on player order in the room, some player skills will be more important than others.\n\n"
                     "For high tier runs with room orders, managers will tell you what room slot to go in (P1 - P5).\n\n"
                     "Join when your number is called. Then when you load into the lobby, call the next number to join.\n\n"
                     "For lower tier runs, placing the strongest fillers as P4 and P5 is typically good enough."))
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        embed = gen_embed(
            title="WHAT'S EBI / EBI JAIL?",
            content=("Ebi = Hitorinbo Envy, the only song that matters.\n\n"
                     "It's the shortest song in the game, meta pick for tierers, and you will probably play it if it’s a Marathon event (for hours at a time, usually, hence \"ebi jail\")."))
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        await ctx.interaction.followup.send(embed=gen_embed(
            title='Marathon Filling Info',
            content=f'Marathon Filling guide posted in {dest_channel.mention}'),
            ephemeral=True)

    @guides.command(name='terms',
                    description='Generates a list of terms for tiering')
    @default_permissions(manage_messages=True)
    async def termsguide(self,
                              ctx: discord.ApplicationContext,
                              channel: Option(discord.SlashCommandOptionType.channel,
                                              ('Channel to post guide in. If not specified, '
                                               'will post in current channel'),
                                              required=False)):
        await ctx.interaction.response.defer()
        if channel:
            dest_channel = channel
        else:
            dest_channel = ctx.interaction.channel
        embed = gen_embed(
            name=f"{ctx.guild.name}",
            icon_url=ctx.guild.icon.url,
            title='Tiering Terms',
            content=("Tiering terms from R8SS, with additions by synthsloth"))
        # embed.set_image(url='https://files.s-neon.xyz/share/bandori-efficiency.png')
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        embed = gen_embed(
            title='Cards',
            content=("**Ascorer:** Accuracy Scorer card. \"*Score +xx% for 5s and Score +xxx% until a GREAT or worse "
                     "tap is recorded.*\"\n\n"
                     "**Fes:** Colorful Festival card, AKA Colofes or Colorfes\n\n"
                     "**Gscorer:** Another name for Ascorer (Accuracy Scorer)\n\n"
                     "**Healer:** Healer card. \"*Life Recovery +350 and Score +x% for 5s.*\"\n\n"
                     "**Lscorer:** Life Scorer card. \"*Score +x% for 5s if your Life is below 800 upon activating "
                     "or Score +y% if above 800, and +1% every time your Life increases by 10 (max z%).*\"\n\n"
                     "**PLocker:** Perfect Locker card. \"*BAD or better taps change to PERFECT taps for 5.5s and "
                     "Score +x% for 5s.*\"\n\n"
                     "**Pscorer:** Perfect Scorer card. \"*Score +x% for PERFECT taps for 5s*\"\n\n"
                     "**Scorer:** Regular scorer card. \"*Score +x% for 5s.*\"\n\n"
                     "**Uscorer:** Unit Scorer card. \"*Score +x% for 5s. Score +10% for every [Unit] Character, "
                     "excluding self, plus an extra 10% (up to +y%) when all Characters are from [Unit].*\""))
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        embed = gen_embed(
            title='Mechanics',
            content=("**AP:** All Perfect\n\n"
                     "**BP:** \"Battle Power\". Another name for Talent\n\n"
                     "**Cans/Boosts/Energy/Drinks:** The amount of energy you use per game. The higher its amount, "
                     "the higher the rewards\n\n"
                     "**CC:** Cheerful Carnival\n\n"
                     "**EB:** Event Bonus\n\n"
                     "**Encore:** 6th skill activation. It's triggered by the player with the highest score (co-op) "
                     "or your leader card (solo show)\n\n"
                     "**EP:** Event Points\n\n"
                     "**FC:** Full Combo\n\n"
                     "**ISV:** Internal Skill Value\n\n"
                     "**MR:** Mastery Rank\n\n"
                     "**Nats:** Energy that regenerates over time (1 energy per 30 mins)\n\n"
                     "**Podium:** Top 3 players of any event\n\n"
                     "**SF:** Short for Super Fever. Tap all the notes during Fever Chance to get extra rewards "
                     "(but NOT extra event points!)\n\n"
                     "**SL:** Short for skill level"))
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        embed = gen_embed(
            title='Tiering',
            content=("**Boat:** To push someone out of their rank\n\n"
                     "**Conduct Warning:** A warning from the game after repeated disconnects. This warning will "
                     "prevent you from joining shows for a certain amount of time. The length of time increases "
                     "with each disconnect.\n\n"
                     "**DC:** Disconnect\n\n"
                     "**Doormat:** During Marathon filling, playing on Easy and hitting every note until the end of "
                     "Fever, and then stopping playing. Allows the filler to do more things during filling\n\n"
                     "**Fillers:** People who help the tierer achieve their goal\n\n"
                     "**Grief:** Ruining something. Whether that's super fever, menuing or anything else\n\n"
                     "**MM:** Short for matchmaking\n\n"
                     "**Menuing:** Tapping the screen after the song ends to play the next one as fast as possible\n\n"
                     "**op:** Open, means the room is open and you can join\n\n"
                     "**Otsu:** Abbreviation of \"otsukaresama\", meaning \"good work\" or \"nice job\". Used when "
                     "leaving a room or after event end\n\n"
                     "**Park:** Achieving a set number of event points and stopping there (for example 6,666,666 or "
                     "20,000,000)\n\n"
                     "**Pub:** Either opening the room to public or playing in co-op\n\n"
                     "**Runner:** A tierer, typically one going for a high tier and being hosted by a server\n\n"
                     "**sc:** \"Scores\", \"spam code\", \"show clear\", etc. During room swaps, indicates you can start "
                     "spamming the \"Join\" button"))
        embed.set_footer(text=discord.Embed.Empty)
        await dest_channel.send(embed=embed)
        await ctx.interaction.followup.send(embed=gen_embed(
            title='Tiering Terms',
            content=f'Tiering terms guide posted in {dest_channel.mention}'),
            ephemeral=True)

def setup(bot):
    bot.add_cog(Tiering(bot))
