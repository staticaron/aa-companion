import discord
from discord.ext import commands
import discord.utils

import config
from data import cache_manager

init_extensions = [
    "cogs.profile_detection",
    "cogs.weakness"
]

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="-", description="Aerial Ace rewrite", intents=intents)

TOKEN = config.TOKEN
poketwo_user_id = config.POKETWO_ID

if __name__ == "__main__":
    for extension in init_extensions:
        bot.load_extension(extension)

@bot.event
async def on_ready():
    print(f"Bot Online as {bot.user.name}")
    await cache_manager.Cache_Data()

@bot.event
async def on_message(message):

    await Profile_Verifier(message)

    await bot.process_commands(message)
        

async def Profile_Verifier(message):

    # only check if verifier is on
    if cache_manager.VERIFIER_DATA[str(message.guild.id)]["state"] == 0:
        return

    if message.author.id == int(poketwo_user_id):

        # only check in set server...
        if message.channel.id != cache_manager.VERIFIER_DATA[str(message.guild.id)]["channel_id"]:
            return

        # detect catches...
        detected_catches = 0
        name, discrim = None, None

        try:
            embeds = message.embeds
            embed = embeds[0]
            data = embed.to_dict()

            if data['title'] == 'Trainer Profile':
                values = ((data['fields'][0]['value']).replace("*","")).split()
                detected_catches = int(values[1])
                name, discrim = (data['author']['name']).split("#")
            else:
                raise Exception()
        except:
            return
        
        # get user to which role is to be given...
        user_id = discord.utils.get(message.guild.members, name=name, discriminator=discrim).id
        member = message.guild.get_member(user_id)

        embed = discord.Embed(title="__Verification System__", color=discord.Color.blue())

        embed.add_field(
            name="User",
            value=member.mention,
            inline=False
        )

        # give badge to pros
        if detected_catches > 30000:
            value = f"{detected_catches} :zap:"
        else:
            value = detected_catches

        embed.add_field(
            name="Catches Detected",
            value=value,
            inline=False
        )

        # perform check to meet conditions
        min_catches, role_id = None, None

        role_id = cache_manager.VERIFIER_DATA[str(message.guild.id)]["role_id"]
        min_catches = cache_manager.VERIFIER_DATA[str(message.guild.id)]["min_catches"]
        role = discord.utils.get(message.guild.roles, id=role_id)

        if role is None:
            await message.channel.send("Role not found")
            return

        if detected_catches >= min_catches:
            
            if role not in member.roles:
                await member.add_roles(role)
                embed.add_field(name="Action : ", value="Verified", inline=False)
            else:
                embed.add_field(name="Action : ", value="Already Verified", inline=False)
        else:
            embed.add_field(name="Action", value="Not Verified", inline=False)
            embed.add_field(name="Remark", value=f"You need to have atleat {min_catches} to get Verified", inline=False)

        await message.channel.send(embed=embed)


bot.run(TOKEN, bot=True, reconnect=True)
