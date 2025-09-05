from beefutilities.trellointegration import trelloclient

async def create_trello_card(name, desc, author):
    await trelloclient.push_trello_card(name, desc, author)

async def create_suggestion(interaction, name, desc):
    try:
        await create_trello_card(name, desc, interaction.user.name)
        await interaction.response.send_message(f"thanku for ur suggestion :) if its not implemented within a month ping jamie or jugg to tell them to get a move on", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"i tried to tell them ur suggestion but its not working sry :(\n{e}", ephemeral=True)