import nextcord
from nextcord.ext import commands


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        await ctx.send("This is a test command!")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        channel_id = 1125581329875087360
        channel = guild.get_channel(channel_id)

        if channel:
            embed = nextcord.Embed(
                title="Welcome!",
                description=f"Welcome to the family , {member.mention}!",
                color=nextcord.Color.green()
            )
            embed.set_thumbnail(url=member.avatar.url)
            embed.add_field(name="Information", value="Please register your roles and read our guidelines. Thank you!",
                            inline=False)

            await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Basic(bot))
