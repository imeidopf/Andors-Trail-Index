import os, glob, pytmx, pygame, xml.etree.ElementTree as ET

def generateMapImages(resPath, globFilter):
    globPath = glob.glob(resPath + globFilter) # Glob path to get all files that ends with .xml.
    print('Map files found: ' + str(len(globPath)))
    print('Generating map resources...')

    for file in globPath:
        # Parse the file and set width and height attributes. The script will fail if these are missing.
        tree = ET.parse(file)
        images = tree.findall('.//image')
        
        for image in images:
            image.set('width', '256')
            image.set('height', '256')

        tree.write(file)

        tiled_map = pytmx.TiledMap(file)
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

        filename = os.path.basename(file)
        pygame.image.save(finalImage, filename.split('.')[0])
    
    print('Finished map image generation...')