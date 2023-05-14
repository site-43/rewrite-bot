from interactions import Extension, extension_command, extension_listener, option, CommandContext, VoiceState
from interactions.ext.lavalink import Lavalink


class Music(Extension):
    def __init__(self, client):
        self.client = client
        self.lavalink: Lavalink = None

    @extension_listener()
    async def on_start(self):
        # Initialize lavalink instance
        self.lavalink: Lavalink = Lavalink(self.client)

        # Connect to lavalink server
        self.lavalink.add_node("192.168.0.34", 2333, "Saturna19", "eu")

    @extension_command(scope=[655335475057393679])
    @option()
    async def play(self, ctx: CommandContext, query: str):
        await ctx.defer()

        # Getting user's voice state
        voice_state: VoiceState = ctx.author.voice_state
        if not voice_state or not voice_state.joined:
            return await ctx.send("You're not connected to the voice channel!")

        # Connecting to voice channel and getting player instance
        player = await self.lavalink.connect(voice_state.guild_id, voice_state.channel_id)

        # Getting tracks from youtube
        tracks = await player.search_youtube(query)
        # Selecting first founded track
        track = tracks[0]
        # Adding track to the queue
        player.add(requester=int(ctx.author.id), track=track)

        # Check if already playing
        if player.is_playing:
            return await ctx.send(f"Added to queue: `{track.title}`")

        # Starting playing track
        await player.play()
        await ctx.send(f"Now playing: `{track.title}`")

    @extension_command(scope=[655335475057393679])
    async def leave(self, ctx: CommandContext):
        # Disconnect from voice channel and remove player
        await self.lavalink.disconnect(ctx.guild_id)

        await ctx.send("Disconnected", ephemeral=True)


def setup(client):
    Music(client)
