import discord
from discord.utils import get
from discord.ext import commands
import json

from data import cache_manager

class Profile_Detection(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot
        self.verifier_enabled = False
        self.min_catches = None
        self.verified_role = None

    @commands.command(name="verifier", aliases = ["ver"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def set_verifier(self, ctx, min_catches : int, role_id : int, channel_id : int):

        if min_catches > 10000:
            embed = discord.Embed(title="Hold UP", description="The max value of min_catches can't/shouldn't exceed 10,000", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        role = get(ctx.guild.roles, id=role_id)
        channel = get(ctx.guild.channels, id=channel_id)

        if role is None or channel is None:
            await ctx.send(embed=discord.Embed(title="Error!", description="Either Role or Channel was not found. \nCheck if both role and channel ids are correct", color=discord.Color.red()))
            return

        embed = discord.Embed(title="Verification System",color=discord.Color.blue())

        embed.add_field(
            name="Minimum Catches",
            value=min_catches,
            inline=False
        )
        embed.add_field(
            name="Verifying Role",
            value=role.mention, 
            inline=False
        )
        embed.add_field(
            name="Verifying Channel",
            value=channel.mention,
            inline=False
        )

        current_state = ("enabled" if cache_manager.VERIFIER_DATA[str(ctx.guild.id)]["state"] == 1 else "disabled")
        embed.set_footer(text=f"Verifier is {current_state}")

        await ctx.send(embed=embed)

        with open("data/data.json", "r") as f_out:
            data = json.loads(f_out.read())
            data["verifier"][str(ctx.guild.id)]["min_catches"] = min_catches
            data["verifier"][str(ctx.guild.id)]["role_id"] = role.id
            data["verifier"][str(ctx.guild.id)]["channel_id"] = channel_id

            with open("data/data.json", "w") as f_in:
                json_object = json.dumps(data)
                f_in.write(json_object)

        await cache_manager.Cache_Data()

    @set_verifier.error
    async def set_verifier_handler(self, ctx, error):
        await ctx.send(f"Verifier command requires input in the following format ```-ver <catches : interger> <role_id : int> <channel_id : int>\n\n-ver 100 929300000128307745 929300000128307763```")
        await ctx.send(f"{error}")

    @commands.command(name="verifier_info", aliases=["ver_info"])
    @commands.guild_only()
    async def ver_info(self, ctx):
        min_catches = cache_manager.VERIFIER_DATA[str(ctx.guild.id)]["min_catches"]
        role = get(ctx.guild.roles, id=cache_manager.VERIFIER_DATA[str(ctx.guild.id)]["role_id"])
        channel = get(ctx.guild.channels, id=cache_manager.VERIFIER_DATA[str(ctx.guild.id)]["channel_id"])
        state = ("Enabled" if cache_manager.VERIFIER_DATA[str(ctx.guild.id)]["state"] == 1 else "Disabled") 

        embed = discord.Embed(title="__Verification System Info__", color=discord.Color.blue())
        embed.add_field(name="Minimum Catches Required", value=min_catches, inline=False)
        embed.add_field(name="Verifying Role",value=role.mention, inline=False)
        embed.add_field(name="Verification Channel", value=channel.mention, inline=False)

        embed.set_footer(text=f"Verifier is {state}")

        await ctx.send(embed=embed)
        

    @commands.command(name="verifier_toggle", aliases = ["ver_toggle"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def ver_toggle(self, ctx):
        if self.verifier_enabled is False:
            self.verifier_enabled = True
            await ctx.send("Verifier was enabled")
        else:
            self.verifier_enabled = False
            await ctx.send("Verifier was disabled")

        with open("data/data.json", "r") as f_out:
            data = json.loads(f_out.read())
            data["verifier"][str(ctx.guild.id)]["state"] = int(self.verifier_enabled)

            with open("data/data.json", "w") as f_in:
                json_object = json.dumps(data)
                f_in.write(json_object)

        await cache_manager.Cache_Data()

    @ver_toggle.error
    async def ver_toggle_handler(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Be a Admin when?")
        else:
            embd = discord.Embed(title="Error!", color=discord.Color.red())
            embd.description = error
            await ctx.send(embed=embd)

def setup(bot):
    bot.add_cog(Profile_Detection(bot))