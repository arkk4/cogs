from .stalkify import Stalkify


async def setup(bot):
    await bot.add_cog(Stalkify(bot))
