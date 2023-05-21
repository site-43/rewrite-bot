from interactions import Extension, extension_command, extension_listener, option, CommandContext, VoiceState
from interactions.ext.tasks import create_task, IntervalTrigger
from interactions.ext.lavalink import Lavalink, Player
from utils.embeds import *

currentNodes = 0

class Music(Extension):
    def __init__(self, client):
        self.client = client
        self.lavalink: Lavalink = None
        

    @extension_listener()
    async def on_start(self):
        # Initialize lavalink instance
        self.lavalink: Lavalink = Lavalink(self.client)

        self.task.start(self)
        # Connect to lavalink server
        self.lavalink.add_node("192.168.0.34", 2333, "Saturna19", "eu", resume_timeout=10, reconnect_attempts=1)

    @create_task(IntervalTrigger(60))
    async def task(self):
        if len(self.lavalink.client.node_manager.available_nodes) == 0:
            print("Trying to connect to lavalink")
            self.lavalink.add_node("192.168.0.34", 2333, "Saturna19", "eu", resume_timeout=10, reconnect_attempts=1)
        

    @extension_command(scope=[655335475057393679])
    @option()
    async def play(self, ctx: CommandContext, query: str):
        await ctx.defer()

        if len(self.lavalink.client.node_manager.available_nodes) == 0:
            return await ctx.send(embeds=[new_notify_embed("Le module de musique n'est pas disponible pour le moment.\n```\nNodes Available: 0/0\nSelfhost = Disabled\nCanPlay = False```")])
        # Getting user's voice state
        voice_state: VoiceState = ctx.author.voice_state
        if not voice_state or not voice_state.joined:
            return await ctx.send("Vous n'êtes pas connecté dans un vocal !")

        # Connecting to voice channel and getting player instance
        player = await self.lavalink.connect(voice_state.guild_id, voice_state.channel_id)
        if player.is_connected == True:
            await ctx.send(embeds=[new_embed("Connection", f"Je suis bien connecté au salon <#{player.channel_id}>")])

        # Getting tracks from youtube
        tracks = await player.search_youtube(query)
        # Selecting first founded track
        track = tracks[0]
        # Adding track to the queue
        player.add(requester=int(ctx.author.id), track=track)

        # Check if already playing
        if player.is_playing:
            return await ctx.send(f"La piste `{track.title}` a été ajoutée à la queue en position {str(len(player.queue) + 1)}.")

        # Starting playing track
        await player.play()
        await ctx.send(f"Piste en cours de lecture: `{track.title}`")

    @extension_command(scope=[655335475057393679])
    async def leave(self, ctx: CommandContext):
        # Disconnect from voice channel and remove player
        await self.lavalink.disconnect(ctx.guild_id)

        await ctx.send("Déconnecté !", ephemeral=True)


    @extension_command(scope=[655335475057393679])
    async def clearqueue(self, ctx: CommandContext):
        """Je suis sur que je peux tout delete."""
        player = self.lavalink.get_player(ctx.guild_id)
        if player and player.is_playing:
            if ctx.member.voice_state.channel_id != player.channel_id:
                return await ctx.send(embeds=[create_error_embed("Vous ne pouvez pas clear la queue si vous n'êtes pas dans le vocal.")])
            if player.queue == 0:
                return await ctx.send(embeds=[create_error_embed("Il n'y a aucun élément à supprimer de la queue.")])
            player.queue.clear()
            await ctx.send(new_notify_embed("La queue a été vidée."))
        else:
            await ctx.send(embeds=[create_error_embed("Le bot n'est pas actif.")])

    @extension_command(scope=[655335475057393679])
    async def getqueue(self, ctx: CommandContext):
        """WHAT ARE YOU WATCHING ??? BRO I'M THE BEST BOT IN THE WORLD"""
        player = self.lavalink.get_player(ctx.guild_id)
        if player and player.is_playing:
            if len(player.queue) == 0:
                return await ctx.send(embeds=[create_error_embed("Aucun son n'est dans la queue.")])
            await ctx.send(embeds=[new_embed(
                title="File d'attente de la Musique", 
                description=f"Nombre de pistes dans la file d'attente: {len(player.queue)}\nVoici les pistes en file d'attente:",
                fields=[[f"`{str(track.position+1)}`- {track.title}", f"Demandée par: <@!{track.requester}>", False] for track in player.queue]
            )])
        else:
            await ctx.send(embeds=[create_error_embed("Il n'y a aucun élément dans la file d'attente, ou le bot n'est pas connecté.")])

    @extension_command(scope=[655335475057393679])
    async def currenttrack(self, ctx: CommandContext):
        """WHAT ARE YOU LISTENING ??? BRO I'M THE BEST BOT IN THE WORLD"""
        player = self.lavalink.get_player(ctx.guild_id)
        print(player.current)
        if player and player.is_playing:
            await ctx.send(embeds=[new_embed(
                title="Titre en cours d'écoute",
                description=f"<a:MusicBeat:1107356051608707133> {player.current.title})",
                fields=[["Aider à héberger le Lavalink", "[Héberger un Lavalink est cher et de l'aide est appréciée :)](https://paypal.me/saturna19dev)"]])
            ])

    @extension_command(scope=[655335475057393679])
    async def skip(self, ctx: CommandContext):
        """Passer la musique en cours"""
        player = self.lavalink.get_player(ctx.guild_id)
        if player and player.is_playing:
            await player.skip()
            await ctx.send("OK!", ephemeral=True)

def setup(client):
    Music(client)
