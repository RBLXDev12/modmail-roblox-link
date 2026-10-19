import aiohttp
import discord
from discord.ext import commands

class RobloxLink(commands.Cog):
    """Automatically pulls and displays linked Roblox profiles on new tickets."""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_thread_ready(self, thread, creator, category, initial_message):
        # RoVer API endpoint for pulling user data by Discord ID
        url = f"https://rover.link{creator.id}"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        roblox_username = data.get("robloxUsername")
                        roblox_id = data.get("robloxId")
                        
                        if roblox_username and roblox_id:
                            profile_url = f"https://roblox.com{roblox_id}/profile"
                            
                            # Create a clean embed for the staff ticket channel
                            embed = discord.Embed(
                                title="🔗 Linked Roblox Account Found",
                                description=f"**Username:** [{roblox_username}]({profile_url})\n**Roblox ID:** `{roblox_id}`",
                                color=discord.Color.red() # Roblox Red
                            )
                            embed.set_footer(text="Verified via RoVer API")
                            
                            # Send strictly to the staff ticket thread channel
                            await thread.channel.send(embed=embed)
                    
                    elif response.status == 404:
                        # User is not verified/found in RoVer's database
                        embed = discord.Embed(
                            title="❌ No Roblox Account Found",
                            description="This user has not verified their account via RoVer.",
                            color=discord.Color.orange()
                        )
                        await thread.channel.send(embed=embed)
                        
            except Exception as e:
                # Fallback if the API is down or encounters an error
                print(f"[Roblox Plugin Error] Failed to fetch data: {e}")

def setup(bot):
    bot.add_cog(RobloxLink(bot))
