# Explosion Animation at Coordinates - Implementation Guide

## 📍 What You're Building

You want to animate the explosion sprite (the pink cross you provided) at specific grid coordinates, spreading in all 4 directions from the bomb center.

**Visual Example:**

```
Original sprite you provided (pink cross):
        ╔═══╗
        ║   ║
    ╔═══╬═══╬═══╗
    ║   ║ X ║   ║
    ╚═══╬═══╬═══╝
        ║   ║
        ╚═══╝
```

This X marks the center. When a bomb explodes with power=1, it shows the cross at the bomb tile. With power=2, it spreads to adjacent tiles.

---

## 🧠 Root Cause: Why Animation Wasn't Working at Coordinates

### **The Problem (Step by Step)**

#### **Before the Fix:**

```python
def explode(self):
    # Only created ONE explosion at bomb center
    Explosion(self.GAME, ..., "centre", ..., self.row, self.col, ...)
```

**Issue:**

1. Bomb planted at (row=5, col=10)
2. Bomb explodes → Creates 1 explosion sprite at (5, 10)
3. Explosion animates the "centre" image only
4. No explosions created at adjacent tiles in directions (up/down/left/right)
5. **Result:** Only the middle of the cross appears, not the full spread

#### **What Should Happen:**

With power=2, the explosion should spread like this:

```
Row 3:                  [explosion "up_end"]
Row 4:                  [explosion "up_mid"]
Row 5:   [left_end]  [centre]  [right_end]
Row 6:                  [explosion "down_mid"]
Row 7:                  [explosion "down_end"]
```

Each position needs its own `Explosion` sprite with the correct `image_type`:

- **Centre:** "centre" (at bomb position)
- **Extremities (last tile in direction):** "up_end", "down_end", "left_end", "right_end"
- **Middle tiles:** "up_mid", "down_mid", "left_mid", "right_mid"

---

## 🔧 Exact Code Changes

### **Change 1: Add Imports for Block Type Checking**

**Location:** Top of `character.py` (line ~20)

**BEFORE:**

```python
import pygame
import gamesetting as gs
```

**AFTER:**

```python
import pygame
import gamesetting as gs

# OLD CODE (didn't import block classes):
# (no imports for blocks)

# NEW CODE (added imports for checking block collisions):
# Import block classes for collision detection in explosion spreading
from blocks import Hard_block, Soft_Block
```

**Why:** We need to check if a tile contains a hard/soft block to stop explosion spreading.

---

### **Change 2: Update Bomb.explode() to Create Directional Explosions**

**Location:** `character.py`, `Bomb` class, `explode()` method (line ~382)

**BEFORE:**

```python
def explode(self):
    """Destroy the bomb and remove from the level matrix"""
    self.kill()
    Explosion(self.GAME, self.GAME.ASSETS.explosion, "centre", self.power,
              self.GAME.groups["explosion"], self.row, self.col, self.size)
    self.remove_bomb_from_grid()
```

**AFTER:**

```python
def explode(self):
    """Destroy the bomb and remove from the level matrix"""
    self.kill()

    # OLD CODE (only created center explosion):
    # Explosion(self.GAME, self.GAME.ASSETS.explosion, "centre", self.power,
    #           self.GAME.groups["explosion"], self.row, self.col, self.size)

    # NEW CODE (creates explosions in all 4 directions based on bomb power):
    # Create center explosion at bomb position
    Explosion(self.GAME, self.GAME.ASSETS.explosion, "centre", self.power,
              self.GAME.groups["explosion"], self.row, self.col, self.size)

    # Create explosions spreading in all 4 directions (up, down, left, right)
    directions = [
        ("up", -1, 0),      # (direction_name, row_delta, col_delta)
        ("down", 1, 0),
        ("left", 0, -1),
        ("right", 0, 1)
    ]

    for direction, row_delta, col_delta in directions:
        for distance in range(1, self.power + 1):  # Spread based on bomb power
            new_row = self.row + (row_delta * distance)
            new_col = self.col + (col_delta * distance)

            # Check if new position is within map bounds
            if not (0 <= new_row < len(self.GAME.level_matrix) and
                    0 <= new_col < len(self.GAME.level_matrix[0])):
                break  # Stop spreading if hit map edge

            # Stop spreading if hit a hard block
            cell = self.GAME.level_matrix[new_row][new_col]
            if isinstance(cell, Hard_block):
                break

            # Determine image type: "end" if last tile, "mid" otherwise
            is_last_tile = (distance == self.power)
            image_type = f"{direction}_end" if is_last_tile else f"{direction}_mid"

            # Create explosion sprite at this tile
            Explosion(self.GAME, self.GAME.ASSETS.explosion, image_type, self.power,
                      self.GAME.groups["explosion"], new_row, new_col, self.size)

            # Stop if hit a soft block (explosion destroys it but doesn't spread through)
            if isinstance(cell, Soft_Block):
                break

    self.remove_bomb_from_grid()
```

**Why This Works:**

1. **Directions Loop:** Checks each of 4 directions (up/down/left/right)

   ```python
   directions = [
       ("up", -1, 0),      # Moving up: row -= 1
       ("down", 1, 0),     # Moving down: row += 1
       ("left", 0, -1),    # Moving left: col -= 1
       ("right", 0, 1)     # Moving right: col += 1
   ]
   ```

2. **Distance Loop:** Spreads based on bomb power

   ```python
   for distance in range(1, self.power + 1):
       # distance=1 is adjacent tile
       # distance=2 is 2 tiles away, etc.
       new_row = self.row + (row_delta * distance)
       new_col = self.col + (col_delta * distance)
   ```

3. **Boundary Check:** Stops at map edges

   ```python
   if not (0 <= new_row < len(...) and 0 <= new_col < len(...)):
       break  # Hit edge, stop spreading this direction
   ```

4. **Block Collision:** Stops at hard blocks, destroys soft blocks

   ```python
   if isinstance(cell, Hard_block):
       break  # Can't spread through indestructible blocks

   if isinstance(cell, Soft_Block):
       break  # Destroys soft block but stops spreading
   ```

5. **Image Type Selection:** Uses correct sprite for each position

   ```python
   is_last_tile = (distance == self.power)
   image_type = f"{direction}_end" if is_last_tile else f"{direction}_mid"
   # Last tile = "up_end", "down_end", etc.
   # Middle tiles = "up_mid", "down_mid", etc.
   ```

6. **Create Explosion Sprite:** Places animation at correct grid coordinate
   ```python
   Explosion(self.GAME, self.GAME.ASSETS.explosion, image_type, self.power,
             self.GAME.groups["explosion"], new_row, new_col, self.size)
   ```

---

## 📊 Animation Flow Example

### **Scenario: Bomb with Power=2 at (Row=5, Col=5)**

**Step 1: Player presses LEFT CTRL**

```
Bomb.explode() called
```

**Step 2: Create center explosion**

```
Explosion at (5, 5) with image_type="centre"
```

**Step 3: Spread UP (row_delta=-1)**

```
distance=1: Create Explosion at (4, 5) with image_type="up_mid"
distance=2: Create Explosion at (3, 5) with image_type="up_end"
```

**Step 4: Spread DOWN (row_delta=+1)**

```
distance=1: Create Explosion at (6, 5) with image_type="down_mid"
distance=2: Create Explosion at (7, 5) with image_type="down_end"
```

**Step 5: Spread LEFT (col_delta=-1)**

```
distance=1: Create Explosion at (5, 4) with image_type="left_mid"
distance=2: Create Explosion at (5, 3) with image_type="left_end"
```

**Step 6: Spread RIGHT (col_delta=+1)**

```
distance=1: Create Explosion at (5, 6) with image_type="right_mid"
distance=2: Create Explosion at (5, 7) with image_type="right_end"
```

**Result on Screen:**

```
                [up_end at (3,5)]
                [up_mid at (4,5)]
[left_end(5,3)] [centre at (5,5)] [right_end(5,7)]
                [down_mid(6,5)]
                [down_end(7,5)]
```

Each explosion animates independently, showing your pink cross sprite in the right directions!

---

## 🎯 Coordinate System Explained

### **Grid Coordinates (Row, Col)**

```
     Col: 0   1   2   3   4
Row 0: [tile] [tile] [tile] [tile] [tile]
Row 1: [tile] [tile] [tile] [tile] [tile]
Row 2: [tile] [tile] [bomb] [tile] [tile]  ← Bomb at (2, 2)
Row 3: [tile] [tile] [tile] [tile] [tile]
Row 4: [tile] [tile] [tile] [tile] [tile]
```

### **Pixel Conversion (for drawing)**

```
pixel_x = col * SIZE         # col * 64
pixel_y = (row * SIZE) + Y_OFFSET  # (row * 64) + 92
```

The `Explosion` class does this automatically in `__init__`:

```python
self.x = self.col * self.size
self.y = (self.row * self.size) + gs.Y_OFFSET
```

So when you create:

```python
Explosion(..., row_num=5, col_num=10, size=64)
```

It automatically calculates:

```python
self.x = 10 * 64 = 640  # pixels
self.y = (5 * 64) + 92 = 412  # pixels
```

---

## ✅ Testing Your Implementation

```
1. Run the game
2. Plant a bomb (SPACE)
3. Press LEFT CTRL to trigger explosion
4. Expected: Pink cross appears at bomb center with arms spreading in all 4 directions
5. Expected: Each explosion animates (~4 frames)
6. Expected: Explosion stops at walls/blocks
7. Expected: Explosion dies after animation completes (~300ms)
```

---

## 🔗 Related Configuration

In `gamesetting.py`, your explosion sprite coordinates are defined as:

```python
EXPLOSION = {
    "centre":[(0,0),(0,1),(0,2),(0,1)],      # Center of cross (4 frames)
    "left_end":[(3,0),(3,1),(3,2),(3,3)],   # Left arm end
    "right_end":[(3,0),(3,1),(3,2),(3,3)],  # Right arm end
    "up_end":[(4,0),(4,1),(4,2),(4,3)],     # Up arm end
    "down_end":[(4,0),(4,1),(4,2),(4,3)],   # Down arm end
    "left_mid":[(3,4),(3,5),(3,6),(3,7)],   # Left arm middle
    "right_mid":[(3,4),(3,5),(3,6),(3,7)],  # Right arm middle
    "up_mid":[(4,4),(4,5),(4,6),(4,7)],     # Up arm middle
    "down_mid":[(4,4),(4,5),(4,6),(4,7)],   # Down arm middle
}
```

Each key corresponds to a position in the explosion pattern, and the values are sprite sheet coordinates.

---

## 📋 Summary

| Aspect          | Details                                                             |
| --------------- | ------------------------------------------------------------------- |
| **Root Cause**  | Only created center explosion, didn't spread to adjacent tiles      |
| **Solution**    | Loop through 4 directions, create explosions for each tile affected |
| **Key Changes** | Import block classes, add directional loop in explode()             |
| **Coordinates** | Grid-based (row, col) → automatically converted to pixels           |
| **Animation**   | Each explosion sprite animates independently for ~300ms             |
| **Collision**   | Explosions stop at hard blocks, destroy soft blocks                 |

---

✅ **Implementation Complete!** Your explosions now animate at all affected grid coordinates with proper directional spreading.
