from PIL import Image
from PIL import ImageFilter
from PIL import ImageOps

im = Image.open('Kirby.png').convert("RGB")
# im = Image.open('Kirby.png')

print(im.format, im.size, im.mode)

# im.show()

# box = (105, 110, 150, 150)
# region = im.crop(box)

# region = region.transpose(Image.ROTATE_180)
# im.paste(region, box)

# im.show()

# mod = im.resize((1000, 1000))
# mod.show()

# invert = ImageOps.invert(mod)
# invert.show()