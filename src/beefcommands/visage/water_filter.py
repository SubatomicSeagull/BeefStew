import math
from random import randint
import discord
from PIL import Image, ImageOps
from io import BytesIO
from beefutilities.IO.file_io import fetch_from_source
from beefutilities.IO import file_io


class WaveDeformer:

    def transform(self, x, y, amplitude, frequency, phase):
        x = x + amplitude*math.sin((y/frequency) + phase)
        return x, y

    def transform_rectangle(self, x0, y0, x1, y1, a, f, p):
        return (*self.transform(x0, y0, a, f, p),
                *self.transform(x0, y1, a, f, p),
                *self.transform(x1, y1, a, f, p),
                *self.transform(x1, y0, a, f, p),
                )

    def getmesh(self, img):
        self.w, self.h = img.size
        gridspace = 20

        target_grid = []
        for x in range(0, self.w, gridspace):
            for y in range(0, self.h, gridspace):
                target_grid.append((x, y, x + gridspace, y + gridspace))

        a = self.w*10/512
        f = randint(30, 60)
        p = randint(0, 100)

        source_grid = [self.transform_rectangle(*rect, a, f, p) for rect in target_grid]

        return [t for t in zip(target_grid, source_grid)]


async def distort(image):
    a = int(image.width*10/512)

    padded = Image.new("RGBA", (image.width+2*a, image.height))

    padded.paste(image, (a, 0))
    padded.paste(image.crop((image.width - a, 0, image.width, image.height)), (0, 0))
    padded.paste(image.crop((0, 0, a, image.height)), (image.width + a, 0))

    distorted = ImageOps.deform(padded, WaveDeformer())

    return distorted.crop((a, 0, a + image.width, image.height))


async def overlay_water(image):
    water_overlay = Image.open(file_io.construct_assets_path("pfp_manipulation", "water.png")).convert("RGBA")
    water_overlay = water_overlay.resize(image.size)

    final_image = Image.blend(image, water_overlay, 0.35)
    final_image = await distort(final_image)

    image_binary = BytesIO()
    final_image.save(image_binary, 'PNG')
    image_binary.seek(0)
    return image_binary

async def drown(interaction: discord.Interaction, source):
    await interaction.response.defer()

    try:
        image = await fetch_from_source(source)
        drowned = await overlay_water(image)
        await interaction.followup.send(file=discord.File(fp = drowned, filename = f"drowned.png"))
        drowned.close()
    except discord.HTTPException as e:
        await interaction.followup.send(f"file too big sorry :(")
    except AttributeError as e:
        await interaction.followup.send(f"that didnt work sry :// gotta be png or jpg")
    except Exception as e:
        await interaction.followup.send(f"uhhhhhhh something went wrong.... ({e})")
