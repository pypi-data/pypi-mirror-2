#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""mian - Mine analysis - Graph block types to height in a Minecraft save game
<http://github.com/l0b0/mian>

Default syntax:

mian [-b|--blocks=<list>] [-l|--list] <World directory>

Options:

-b, --blocks    Specify block types to include as a comma-separated list, using
                either the block types or hex values from the list.
-l, --list      List available block types (from
                <http://www.minecraftwiki.net/wiki/Data_values>).
-n, --nether    Graph The Nether instead of the ordinary world.

Description:

Creates a file with a graph of how much the given materials occur at each
layer of the map.

Examples:

$ mian ~/.minecraft/saves/World1
Creates World1.png in the current directory with the graph.

$ mian -b 01,dirt,09,sand ~/.minecraft/saves/World1
Ditto, showing only the specified block types.

$ mian -b 56,57,58,59,5a,5b -n ~/.minecraft/saves/World1
Graph all the materials new to The Nether.

$ mian --list
Show a list of block types which can be searched for.
"""

__author__ = 'Pepijn de Vos, Victor Engmark'
__copyright__ = 'Copyright (C) 2010 Pepijn de Vos, Victor Engmark'
__credits__ = ['Pepijn de Vos', 'Victor Engmark']
__maintainer__ = 'Victor Engmark'
__email__ = 'victor.engmark@gmail.com'
__license__ = 'GPL v3 or newer'

from binascii import unhexlify
from getopt import getopt, GetoptError
from glob import glob
import matplotlib.pyplot as plt
from nbt.nbt import NBTFile
from os.path import join, split
from signal import signal, SIGPIPE, SIG_DFL
import sys
import warnings

HEXDIGITS = '0123456789abcdef'

# The first name is the canocical one (for the moment).
# Subsequent names are synonyms.
BLOCK_TYPES = {
    '\x00': ['Air'],
    '\x01': ['Stone'],
    '\x02': ['Grass'],
    '\x03': ['Dirt'],
    '\x04': ['Cobblestone'],
    '\x05': [
        'Wood',
        'Log'],
    '\x06': ['Sapling'],
    '\x07': [
        'Bedrock',
        'Adminium'],
    '\x08': ['Water'],
    '\x09': ['Stationary water'],
    '\x0a': ['Lava'],
    '\x0b': ['Stationary lava'],
    '\x0c': ['Sand'],
    '\x0d': ['Gravel'],
    '\x0e': ['Gold ore'],
    '\x0f': ['Iron ore'],
    '\x10': ['Coal ore'],
    '\x11': ['Log'],
    '\x12': ['Leaves'],
    '\x13': ['Sponge'],
    '\x14': ['Glass'],
    '\x15': ['Red cloth'],
    '\x16': ['Orange cloth'],
    '\x17': ['Yellow cloth'],
    '\x18': ['Lime cloth'],
    '\x19': ['Green cloth'],
    '\x1a': ['Aqua green cloth'],
    '\x1b': ['Cyan cloth'],
    '\x1c': ['Blue cloth'],
    '\x1d': ['Purple cloth'],
    '\x1e': ['Indigo cloth'],
    '\x1f': ['Violet cloth'],
    '\x20': ['Magenta cloth'],
    '\x21': ['Pink cloth'],
    '\x22': ['Black cloth'],
    '\x23': ['Gray / white cloth'],
    '\x24': ['White cloth'],
    '\x25': ['Yellow flower'],
    '\x26': ['Red rose'],
    '\x27': ['Brown mushroom'],
    '\x28': ['Red mushroom'],
    '\x29': ['Gold block'],
    '\x2a': ['Iron block'],
    '\x2b': [
        'Double slab',
        'Double step'],
    '\x2c': [
        'Stone slab',
        'Step'],
    '\x2d': ['Brick'],
    '\x2e': ['TNT'],
    '\x2f': ['Bookshelf'],
    '\x30': [
        'Moss Stone',
        'Mossy cobblestone'],
    '\x31': ['Obsidian'],
    '\x32': ['Torch'],
    '\x33': ['Fire'],
    '\x34': [
        'Monster spawner',
        'Mob spawner'],
    '\x35': ['Wooden stairs'],
    '\x36': ['Chest'],
    '\x37': ['Redstone wire'],
    '\x38': ['Diamond ore'],
    '\x39': ['Diamond block'],
    '\x3a': ['Workbench'],
    '\x3b': ['Crops'],
    '\x3c': ['Soil'],
    '\x3d': ['Furnace'],
    '\x3e': ['Burning furnace'],
    '\x3f': ['Sign post'],
    '\x40': ['Wooden door'],
    '\x41': ['Ladder'],
    '\x42': [
        'Minecart tracks',
        'Rails'],
    '\x43': ['Cobblestone stairs'],
    '\x44': ['Wall sign'],
    '\x45': ['Lever'],
    '\x46': ['Stone pressure plate'],
    '\x47': ['Iron door'],
    '\x48': ['Wooden pressure plate'],
    '\x49': ['Redstone ore'],
    '\x4a': ['Glowing redstone ore'],
    '\x4b': ['Redstone torch [off]'],
    '\x4c': ['Redstone torch [on]'],
    '\x4d': ['Stone button'],
    '\x4e': ['Snow'],
    '\x4f': ['Ice'],
    '\x50': ['Snow block'],
    '\x51': ['Cactus'],
    '\x52': ['Clay'],
    '\x53': [
        'Reed',
        'Bamboo',
        'Papyrus'],
    '\x54': ['Jukebox'],
    '\x55': ['Fence'],
    '\x56': ['Pumpkin'],
    '\x57': [
        'Netherrack',
        'Bloodstone',
        'Hellstone',
        'Netherstone',
        'Red Mossy Cobblestone'],
    '\x58': [
        'Soul Sand',
        'Hell mud',
        'Mud',
        'Nethermud',
        'Slow sand'],
    '\x59': [
        'Lightstone',
        'Brittle gold',
        'Brightstone',
        'Australium',
        'Brimstone'],
    '\x5a': ['Portal'],
    '\x5b': ['Jack-o-lantern']}

DEFAULT_BLOCK_TYPES = [
    'clay',
    'coal ore',
    'diamond ore',
    'gold ore',
    'iron ore',
    'obsidian',
    '49']

CHUNK_SIZE_Y = 128
CHUNK_SIZE_Z = 16
CHUNK_SIZE_X = CHUNK_SIZE_Y * CHUNK_SIZE_Z

signal(SIGPIPE, SIG_DFL)
"""Avoid 'Broken pipe' message when canceling piped command."""


def lookup_block_type(block_type):
    """
    Find block types based on input string.

    @param block_type: Name or hex ID of a block type.
    @return: Subset of BLOCK_TYPES.keys().
    """

    if block_type is None or len(block_type) == 0:
        warnings.warn('Empty block type')
        return set([])

    block_type = block_type.lower()

    if len(block_type) == 2 and all(char in HEXDIGITS for char in block_type):
        # Look up single block type by hex value
        for block_hex, block_names in BLOCK_TYPES.iteritems():
            if block_hex == unhexlify(block_type):
                return set([block_hex])

    # Name substring search, could have multiple results
    result = set([])
    for block_hex, block_names in BLOCK_TYPES.iteritems(): # Block
        for block_name in block_names: # Synonyms
            if block_name.lower().find(block_type) != -1:
                result.add(block_hex)

    if result == set([]):
        warnings.warn('Unknown block type %s' % block_type)
    return result


def print_block_types():
    """Print the block block_names and hexadecimal IDs"""
    for block_hex, block_names in BLOCK_TYPES.iteritems():
        print hex(ord(block_hex))[2:].upper().zfill(2), block_names.join(', ')


def plot(counts, bt_hexes, title):
    """
    Actual plotting of data.

    @param counts: Integer counts per layer.
    @param bt_hexes: Subset of BLOCK_TYPES.keys().
    """
    fig = plt.figure() 
    fig.canvas.set_window_title(title)

    for index, block_counts in enumerate(counts):
        plt.plot(
            block_counts,
            label = BLOCK_TYPES[bt_hexes[index]][0],
            linewidth = 1)

    plt.legend()
    plt.ylabel('Count')
    plt.xlabel('Y (world height)')

    plt.show()


def mian(world_dir, bt_hexes, nether):
    """
    Runs through the DAT files and gets the layer counts for the plot.

    @param world_dir: Path to existing Minecraft world directory.
    @param bt_hexes: Subset of BLOCK_TYPES.keys().
    @param nether: Whether or not to graph The Nether.
    """

    title = split(world_dir)[1]

    # All world blocks are stored in DAT files
    if nether:
        paths = glob(join(world_dir, 'DIM-1/*/*/*.dat'))
        title += ' Nether'
    else:
        paths = glob(join(world_dir, '*/*/*.dat'))

    # Unpack block format
    # <http://www.minecraftwiki.net/wiki/Alpha_Level_Format#Block_Format>
    raw_blocks = ''
    for path in paths:
        nbtfile = NBTFile(path, 'rb')

        raw_blocks += nbtfile['Level']['Blocks'].value

        nbtfile.file.close()

    layers = [raw_blocks[i::128] for i in xrange(127)]
    
    counts = [[] for i in xrange(len(bt_hexes))]
    for bt_index in range(len(bt_hexes)):
        bt_hex = bt_hexes[bt_index]
        for layer in layers:
            counts[bt_index].append(layer.count(bt_hex))

    plot(counts, bt_hexes, title)


def main(argv = None):
    """Argument handling."""

    if argv is None:
        argv = sys.argv

    # Defaults
    block_type_names = DEFAULT_BLOCK_TYPES
    nether = False

    try:
        opts, args = getopt(
            argv[1:],
            'b:ln',
            ['blocks=', 'list', 'nether'])
    except GetoptError, err:
        sys.stderr.write(str(err) + '\n')
        return 2

    for option, value in opts:
        if option in ('-b', '--blocks'):
            block_type_names = value.split(',')
        elif option in ('-n', '--nether'):
            nether = True
        elif option in ('-l', '--list'):
            print_block_types()
            return 0
        else:
            sys.stderr.write('Unhandled option %s\n' % option)
            return 2

    assert len(args) == 1, 'You need to specify exactly one save directory.'
    world_dir = args[0]

    # Look up block_types
    bt_hexes = []
    for name in block_type_names:
        bt_hexes.extend(lookup_block_type(name))

    mian(world_dir, bt_hexes, nether)


if __name__ == '__main__':
    sys.exit(main())
