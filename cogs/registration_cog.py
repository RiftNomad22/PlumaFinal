import nextcord
import asyncio
from nextcord.ext import commands


class RegistrationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.available_roles = {
            "Cluster1": {"id": 1125366196649349191, "emoji": "1️⃣"},
            "Cluster2": {"id": 1125366820602396712, "emoji": "2️⃣"},
            "Cluster3": {"id": 1125367433872560199, "emoji": "3️⃣"},
            "Cluster4": {"id": 1125367875075584030, "emoji": "4️⃣"},
            "Private School": {"id": 1125368370238341120, "emoji": "5️⃣"},
            "School Head": {"id": 1125368799185604678, "emoji": "🌝"},
            "NSBI coor": {"id": 1125369272735109230, "emoji": "🔧"},
            "LIS coor": {"id": 1125371604281593988, "emoji": "🪛"},
            "BEIS coor": {"id": 1125371619326558210, "emoji": "🔩"},
            "Research Focal": {"id": 1125965435150544966, "emoji": "🔍"}
        }

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.send_registration_message(member)

    async def send_registration_message(self, member):
        roles_to_assign = []

        embed = nextcord.Embed(title="Role Registration")
        embed.description = "React with the corresponding emoji(s) to assign yourself role(s):\n\n"

        for role_name, role_data in self.available_roles.items():
            embed.description += f"{role_data['emoji']} {role_name}\n"
            roles_to_assign.append(role_data["id"])

        message = await member.send(embed=embed)

        for role_name, role_data in self.available_roles.items():
            emoji = role_data["emoji"]
            await message.add_reaction(emoji)

        def check(reaction, user):
            return user == member and str(reaction.emoji) in [role_data["emoji"] for role_data in
                                                              self.available_roles.values()]

        try:
            while True:
                reaction, _ = await self.bot.wait_for("reaction_add", timeout=3600.00, check=check)
                role_name = self.get_role_for_emoji(str(reaction.emoji))
                if role_name:
                    role_id = self.available_roles[role_name]["id"]
                    if role_id in roles_to_assign:
                        role = member.guild.get_role(role_id)
                        if role and role not in member.roles:
                            await member.add_roles(role)
                            roles_to_assign.remove(role_id)
        except nextcord.NotFound:
            await member.send("This message has expired. Please contact the administrators in case you don't have "
                              "roles yet.")
            # Handle cases where the DM is no longer accessible (e.g., member left the server or blocked the bot)
            pass
        except Exception as e:
            print(f"An error occurred: {type(e).__name__}: {str(e)}")

    def get_role_for_emoji(self, emoji):
        for role_name, role_data in self.available_roles.items():
            if emoji == role_data["emoji"]:
                return role_name
        return None


def setup(bot):
    bot.add_cog(RegistrationCog(bot))