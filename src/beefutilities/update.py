import discord
import os
import re
from beefutilities.IO import file_io

async def update_info(interaction: discord.Interaction, bot):
    await interaction.response.defer()

    # retrieve the info from the patch notes
    try:
        info = await parse_update_file()
    except Exception as e:
        await interaction.followup.send("Couldn't find the patch notes :(")
        return

    version = info["version"]
    features = info["features"]
    fixes = info["fixes"]
    misc = info["misc"]
    comments = info["comments"]

    img_path = file_io.construct_assets_path("profile/update.png")

    # embed header
    update_embed = discord.Embed(title="Beefstew has been updated!", description=f"# Version {version} is here!\n ## Here's whats changed:", color=discord.Color.lighter_grey())
    update_embed.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)

    # embed body
    # list all the new features
    if features:
        update_embed.add_field(name="Features:", value="", inline=False)
        for feature in features:
            update_embed.add_field(name="", value=feature, inline=False)
    else:
        update_embed.add_field(name="No new features this time", value="", inline=False)

    # list all the bug fixes
    if fixes:
        update_embed.add_field(name="Fixes:", value="", inline=False)
        for fix in fixes:
            update_embed.add_field(name="", value=fix, inline=False)
    else:
        update_embed.add_field(name="General stability fixes and stuff", value="", inline=False)
    update_embed.add_field(name="", value="- removed herobrine", inline=False)

    # list all the misc changes
    if misc:
        update_embed.add_field(name="Other Changes:", value="", inline=False)
        for change in misc:
            update_embed.add_field(name="", value=change, inline=False)
    else:
        update_embed.add_field(name="...and that's it!", value="", inline=False)

    # list comments
    if comments != "":
        update_embed.add_field(name="Comments:", value=comments, inline=False)

    # embed footer
    file = discord.File(img_path,filename="update.png")
    update_embed.set_image(url="attachment://update.png")
    await interaction.followup.send(content="@here", file=file, embed=update_embed, allowed_mentions=discord.AllowedMentions(everyone=True))

async def parse_update_file():
    # construct the file path to patchnotes.md
    markdown_path = file_io.construct_root_path("patchnotes.md")

    with open(markdown_path, "r") as file:
        lines = file.read().splitlines()

    version = ""
    features = []
    fixes = []
    misc = []
    comments = []

    current_section = None

    for line in lines:
        stripped = line.strip()

        # extract version from header
        if stripped.startswith("## Beefstew version"):

            # match the version
            version_match = re.search(r'version\s+(\d+(?:\.\d+){0,2})', stripped, re.IGNORECASE)
            if version_match:
                version = version_match.group(1)
            continue

        # detect section headers
        if stripped == "## Features:":
            current_section = "features"
            continue
        elif stripped == "## Fixes:":
            current_section = "fixes"
            continue
        elif stripped == "## Misc:":
            current_section = "misc"
            continue
        elif stripped == "## Comments:":
            current_section = "comments"
            continue

        # add each point to the section
        if current_section:
            if stripped.startswith("- "):
                item = stripped[2:].strip()
                if current_section == "features":
                    features.append(f"- {item}")
                elif current_section == "fixes":
                    fixes.append(f"- {item}")
                elif current_section == "misc":
                    misc.append(f"- {item}")

            # everything else gets pushed to comments
            elif stripped:
                comments.append(stripped)

        # anything before is pushed to comments too
        elif stripped and not stripped.startswith("#"):
            comments.append(stripped)

    # merge comments
    comments_str = "\n".join(comments) if comments else ""

    return {
        "version": version,
        "features": features,
        "fixes": fixes,
        "misc": misc,
        "comments": comments_str
    }
