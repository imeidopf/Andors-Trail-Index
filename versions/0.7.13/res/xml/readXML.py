# import base64, struct, zlib, sys
# from xml.dom import minidom

# template = 'home.tmx'
# document = minidom.parse(template)
# tilesets = document.getElementsByTagName('tileset')
# layers = document.getElementsByTagName('layer')

# # for tileset in tilesets:
# #     print(tileset)

# for layer in layers:
#     attr_text = layer.getElementsByTagName('data')[0].childNodes[0].data
#     width = int(layer.getAttribute('width'))
#     height = int(layer.getAttribute('height'))
#     data = zlib.decompress(base64.b64decode(attr_text))
#     numbers = struct.unpack ('<'+('I'*width*height), data)
#     map = document.getElementsByTagName('map')[0]
#     print(numbers)
#     print("\n")

import pytmx, pygame

tiled_map = pytmx.TiledMap('home.tmx')
mapWidth = tiled_map.width * tiled_map.tilewidth
mapHeight = tiled_map.height * tiled_map.tileheight
levelSize = (mapWidth, mapHeight)

tile = tiled_map.get_tile_image_by_gid

finalImage = pygame.Surface(levelSize)

for layer in tiled_map.layers:
    if layer.name == 'Walkable':
        continue
    if isinstance(layer, pytmx.TiledTileLayer):
        for x, y, gid in layer:
            tileData = tile(gid)
            if not tileData is None:
                spritesheet = pygame.image.load(tileData[0])
                finalImage.blit(spritesheet, (x * tiled_map.tilewidth, y * tiled_map.tileheight), tileData[1])

pygame.image.save(finalImage, "home.png")