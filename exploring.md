# Map #

The player controls a group of characters who explore a map. This could be a cave, tomb, dungeon, castle, town, wilderness, country or world map. The map might be randomly generated, or it could be loaded from an SVG document, or we could have both options.

# Nodes #

The characters move from one node to another each turn. Nodes could be spaces on a grid, towns connected by roads, rooms connected by doors, ports connected by sea routes, etc. Paths between nodes could be represented by bezier curves which can either form straight paths or curved paths. In SVG format, nodes would be automatically placed at the end points of paths. If two or more endpoints are close together they will share a single node. A player can select places to travel by clicking on neighboring nodes with the mouse. To keep the keyboard controls simple, nodes can be connected to no more than 4 other nodes:

  * The path which is exits a node closest to due north is selected by pressing the up arrow key, 'e' key or numpad 8.
  * The remaining path which exits the node closest to due east is selected by pressing the right arrow key, 'f' key or numpad 6.
  * The remaining path which exits the node closest to due south is selected by pressing the down arrow key, 'd' key or numpad 2.
  * The remaining path is selected by pressing the left arrow key, 's' key or numpad 4.

Nodes and paths might be represented by lines or might be invisible (this could vary from map-to-map.) If the paths or nodes are already drawn on the map background, it is not necessary to draw them again. If the paths and nodes form a grid, it may not need to be shown.

# Party #

The characters all stay together as they move. The party could be represented by a group of animated characters (one for each character in the party.) When the player selects a new destination the characters travel along the path connecting the nodes at slight delays so they appear to follow a leader down the path.

# Visibility #

The player can see the current node, it's contents (empty or enemy), visited nodes and their contents, any paths connected to those nodes and any nodes at the ends of those paths which are occupied by non-hidden enemies.

Hidden enemies (traps) are not automatically visible. When the player chooses to walk into a trap, each rogue or dragon in the party has a chance to detect the trap. If any of them detect the trap, the trap becomes a regular enemy and the party stays in it's current position until the player selects that node again, so the player can decide whether the characters should avoid that route. If none of the character detect the trap they are forced to fight the hidden enemies at a disadvantage (the enemies get a free turn.)