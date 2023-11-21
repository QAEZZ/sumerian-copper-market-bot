import discord

EMBED_COLOR = discord.Colour.from_rgb(205, 110, 70)

LOGO = 'https://cdn.discordapp.com/attachments/977002095930662962/1175304701043015701/2023_11_17_0rr_Kleki.png'

PREFIX = 'scm.'
CLIENT_ID = 1175302342212599899
CLIENT_OWNER = 1123758641485459477
ACTIVITY = discord.Game('Bartering for copper.')

COG_ACCESS = [1123758641485459477] # allowed to load, unload, and reload cogs
ECONOMY_MODERATOR = [1123758641485459477] # allowed to use moderation commands for the economy

HELP_DESCRIPTION = f"""
**Client Tools**
> `help` : shows this
> `info` : Shows information about the client
> `latency` : Shows the latency in ms

**Market Tools**
> `create` : Become a trader
> `bal` : Shows your balance
> `mine` : Go to the mines
> `beg` : No one likes a begger
> `gamble` : Gamble away your copper <:PRAISEDALORD:1079102735011557407>
> `give` : Give money to someone
> `ask` : Ask Ea-Nasir something
> `rps` : Play RPS with Ea-Nasir, place bets even
> `lb` : Show the leader board [low, medium, high, all]
> `convert` : Convert between grades

**Market Mod Tools**
> `reset` : Reset a user's balance
> `delete` : Delete a user

**Syntax Tips**
> `<parameter>` : Angles brackets indicate that they are required.
> `[parameter]` : Square brackets indicate that they are optional.

**Types**
> `low` : References low-grade copper.
> `medium` : References medium-grade copper.
> `high` : References high-grade copper.
> `all` : All grades of copper, it will be noted when you can use this.

*Learn more about a command by using* `{PREFIX}help <command>`
"""