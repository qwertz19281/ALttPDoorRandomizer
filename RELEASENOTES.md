## New Features

## Restricted Item Placement Algorithm


The "Item Sorting" option or ```--algorithm``` has been updated with new placement algorithms. Older algorithms have been removed.
 
 When referenced below, Major Items include all Y items, all A items, all equipment (swords, shields, & armor) and Heart Containers. Dungeon items are considered major if shuffled outside of dungeons. Bomb and arrows upgrades are Major if shopsanity is turned on. The arrow quiver and universal small keys are Major if retro is turned on. Triforce Pieces are Major if that is the goal, and the Bomb Bag is Major if that is enabled.
 
 Here are the current fill options:

### Balanced 

This one stays the same as before and is recommended for the most random distribution of items.

### Equitable

This one is currently under development and may not fill correctly. It is a new method that should allow item and key logic to interact. (Vanilla key placement in PoD is theoretically possible, but isn't yet.)

### Vanilla Fill 

This fill attempts to place all items in their vanilla locations when possible. Obviously shuffling entrances or the dungeon interiors will often prevent items from being placed in their vanilla location. If the vanilla fill is not possible, then other locations are tried in sequence preferring "major" locations (see below), then heart piece locations, then the rest except for GT locations which are preferred last. Note the PoD small key that is normally found in the dark maze in vanilla is move to Harmless Hellway due to the placement algorithm limitation.

### Major Location Restriction

This fill attempts to place major items in major locations. Major locations are where the major items are found in the vanilla game. This includes the spot next to Uncle in the Sewers, and the Boomerang chest in Hyrule Castle.

This location pool is expanded to where dungeon items are locations if those dungeon items are shuffled. The Capacity Fairy locations are included if Shopsanity is on. If retro is enabled in addition to shopsanity, then the Old Man Sword Cave and one location in each retro cave is included. Key drop locations can be included if small or big key shuffle is on. This gives a very good balance between overworld and underworld locations though the dungeons ones will be on bosses and in big chests generally. Seeds do become more linear but usually easier to figure out.

### Dungeon Restriction

The fill attempts to place all major items in dungeons. It will overflow to the overworld if there are more items than locations (e.g. Triforce hunt.) This fill does attempt to run the GT trash fill when possible. Seeds are typically very linear but tend to be more difficult.

### District Restriction
 
The world is divided up into different regions or districts. Each dungeon is it's own district. The overworld consists of the following districts:

Light world:

* Kakariko (The main screen, blacksmith screen, and library/maze race screens)
* Northwest Hyrule (The lost woods and fortune teller all the way to the rive west of the potion shop)
* Central Hyrule (Hyrule castle, Link's House, the marsh, and the haunted grove)
* Desert (From the thief to the main desert screen)
* Lake Hylia (Around the lake)
* Eastern Hyrule (The eastern wild, the potion shop, and Zora's Domain)
* Death Mountain

Dark world:

* East Dark World (The pyramid, Palace of darkness, and Catfish)
* South Dark World (The dark lake, swamp area, to the dig game)
* Northwest Dark World (Village of Outcasts, to the Dark Sanctuary and screens in between)
* The Mire
* Dark Death Mountain

These districts are chosen at random and then filled with major items. If a location is part of a chosen district, but there are no more major items to place, a single green rupee is placed in the extra to indicate that as a placeholder. All other single green rupees are changed to be a blue rupee in order to not give false positives.

In entrance shuffle, what is shuffled to the entrances is considered instead of where the interior was originally. For example, if Blind's Hut is shuffled to the Dam, then the 5 chests in Blind's Hut are part of Central Hyrule instead of Kakariko.

Bombos Table, Lake Hylia Island, Bumper Cave Ledge, the Floating Island, Cave 45, the Graveyard Cave, Checkerboard Cave and Mimic Cave are considered part of the dark world region that you mirror from to get there (except in inverted where these are only accessible in the Light World). Note that Spectacle Rock is always part of light Death Mountain.

In multiworld, the districts chosen apply to all players.  

### CLI values:

```balanced, equitable, vanilla_fill, major_only, dungeon_only, district```

## New Hints

Based on the district algorithm above (whether it is enabled or not,) new hints can appear about that district or dungeon. For each district and dungeon, it is evaluated whether it contains vital items and how many. If it has not any vital item, items then it moves onto useful items. Useful items are generally safeties or convenience items: shields, mails, half magic, bottles, medallions that aren't required, etc. If it contains none of those and is an overworld district, then it check for a couple more things. First, if dungeons are shuffled, it looks to see if any are in the district, if so, one of those dungeons is picked for the hint. Then, if connectors are shuffled, it checks to see if you can get to unique region through a connector in that district. If none of the above apply, the district or dungeon is considered completely foolish. At least two "foolish" districts are chosen and the rest are random.


### Overworld Map shows dungeon location

Option to move indicators on overworld map to reference dungeon location. The non-default options include indicators for Hyrule Castle, Agahnim's Tower, and Ganon's Tower.

CLI ```--overworld_map```

#### Options

##### default

Status quo. Showing only the prize markers on the vanilla dungeon locations.

##### compass

The compass item controls whether the marker is moved to the dungeons locations. If you possess the compass but not the map, only a glowing X will be present regardless of dungeon prize type, if you only possess the map, the prizes will be shown in predicable locations at the bottom of the overworld map instead of the vanilla location. Light world dungeons on the light world map and dark world dungeons on the dark world map. If you posses both map and compass, then the prize of the dungeon and the location will be on the map.

If you do not shuffle the compass or map outside of the dungeon, the non-shuffled items are not needed to display the information. If a dungeon does not have a map or compass, it is not needed for the information. Talking to the bomb shop or Sahasrahla furnishes you with complete information as well as map information.

##### map

The map item plays double duty in this mode and only possession of the map will show both prize and location of the dungeon. If you do not shuffle maps or the dungeon does not have a map, the information will be displayed without needing to find any items.

## Restricted Dungeon Items on Bosses

You may now restrict the items that can appear on the boss, like the popular ambrosia preset does.

CLI: ```--restrict_boss_items <option>```

#### Options

##### none

As before, the boss may have any item including any dungeon item that could occur there.

##### mapcompass

The map and compass are logically required to defeat a boss. This prevents both of those from appearing on the dungeon boss. Note that this does affect item placement logic and the placement algorithm as maps and compasses are considered as required items to beat a boss.

##### dungeon

Same as above but both small keys and bigs keys of the dungeon are not allowed on a boss. (Note: this does not affect universal keys as they are not dungeon-specific)

## Notes and Bug Fixes

* 1.0.0.2
	* Include 1.0.1 fixes
	* District hint rework
* 1.0.0.1
	* Add Light Hype Fairy to bombbag mode as needing bombs
	
### From stable DoorDev

* 1.0.1
	* Fixed a bug with key doors not detecting one side of an interior door
	* Sprite selector fix for systems with SSL issues