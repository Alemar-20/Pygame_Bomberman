# Explosion Animation Visual Diagrams

## 📍 Coordinate System

### Grid Layout (Row, Col)

```
     Col→ 0   1   2   3   4   5   6   7   8
Row↓
0      [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]
1      [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]
2      [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]
3      [ ] [ ] [ ] [ ] [ ][B][ ] [ ] [ ]   ← Bomb at (3,5)
4      [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]
5      [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]
6      [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]
```

---

## 💣 Explosion Spread Animation

### Scenario: Bomb Power = 2

```
STEP 1: Center Explosion
───────────────────────
     Col   0   1   2   3   4   5   6   7

2    [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]
3    [ ] [ ] [ ] [ ] [ ][X][ ] [ ] [ ]   X = centre
4    [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]

(Only the pink cross center appears)


STEP 2: UP Spread (direction_name="up", row_delta=-1)
───────────────────────────────────────────────────
distance=1: new_row=1, new_col=5, image_type="up_mid"
distance=2: new_row=0, new_col=5, image_type="up_end"

     Col   0   1   2   3   4   5   6   7

0    [ ] [ ] [ ] [ ] [ ][E][ ] [ ] [ ]   E = up_end
1    [ ] [ ] [ ] [ ] [ ][M][ ] [ ] [ ]   M = up_mid
2    [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]
3    [ ] [ ] [ ] [ ] [ ][X][ ] [ ] [ ]   X = centre
4    [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]


STEP 3: DOWN Spread (direction_name="down", row_delta=+1)
──────────────────────────────────────────────────────
distance=1: new_row=4, new_col=5, image_type="down_mid"
distance=2: new_row=5, new_col=5, image_type="down_end"

     Col   0   1   2   3   4   5   6   7

0    [ ] [ ] [ ] [ ] [ ][E][ ] [ ] [ ]
1    [ ] [ ] [ ] [ ] [ ][M][ ] [ ] [ ]
2    [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]
3    [ ] [ ] [ ] [ ] [ ][X][ ] [ ] [ ]
4    [ ] [ ] [ ] [ ] [ ][M][ ] [ ] [ ]
5    [ ] [ ] [ ] [ ] [ ][E][ ] [ ] [ ]


STEP 4: LEFT Spread (direction_name="left", col_delta=-1)
──────────────────────────────────────────────────────
distance=1: new_row=3, new_col=4, image_type="left_mid"
distance=2: new_row=3, new_col=3, image_type="left_end"

     Col   0   1   2   3   4   5   6   7

0    [ ] [ ] [ ] [ ] [ ][E][ ] [ ] [ ]
1    [ ] [ ] [ ] [ ] [ ][M][ ] [ ] [ ]
2    [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]
3    [ ] [ ] [ ][E][M][X][ ] [ ] [ ]
4    [ ] [ ] [ ] [ ] [ ][M][ ] [ ] [ ]
5    [ ] [ ] [ ] [ ] [ ][E][ ] [ ] [ ]


STEP 5: RIGHT Spread (direction_name="right", col_delta=+1)
─────────────────────────────────────────────────────────
distance=1: new_row=3, new_col=6, image_type="right_mid"
distance=2: new_row=3, new_col=7, image_type="right_end"

     Col   0   1   2   3   4   5   6   7

0    [ ] [ ] [ ] [ ] [ ][E][ ] [ ] [ ]
1    [ ] [ ] [ ] [ ] [ ][M][ ] [ ] [ ]
2    [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]
3    [ ] [ ] [ ][E][M][X][M][E][ ]      ← FULL EXPLOSION
4    [ ] [ ] [ ] [ ] [ ][M][ ] [ ] [ ]
5    [ ] [ ] [ ] [ ] [ ][E][ ] [ ] [ ]

Legend:
X = centre       (at bomb position)
E = end          (last tile in direction)
M = mid          (middle tile in direction)
```

---

## 🔄 Animation Timeline

```
Frame 0:   Plant bomb (pressing SPACE)
  └─ Bomb at (3,5) starts blinking animation

Frame N:   Trigger explosion (pressing LEFT CTRL)
  ├─ Kill bomb sprite
  ├─ Create 9 Explosion sprites:
  │  ├─ centre at (3,5)
  │  ├─ up_mid at (1,5)
  │  ├─ up_end at (0,5)
  │  ├─ down_mid at (4,5)
  │  ├─ down_end at (5,5)
  │  ├─ left_mid at (3,4)
  │  ├─ left_end at (3,3)
  │  ├─ right_mid at (3,6)
  │  └─ right_end at (3,7)
  └─ All explosions start animating

Frame N+1 to N+10:   Animation frame 0 of each explosion
Frame N+11 to N+20:  Animation frame 1 of each explosion
Frame N+21 to N+30:  Animation frame 2 of each explosion
Frame N+31 to N+40:  Animation frame 3 of each explosion

Frame N+41:  All explosions call .kill() and disappear
  └─ Game returns to normal state

Frame N+42:  Player can plant new bomb (SPACE)
```

---

## 🗂️ Collision Detection During Spreading

### Scenario: Power=3, but Hard Block at (3,7)

```
BEFORE SPREADING:
     Col   0   1   2   3   4   5   6   7   8

0    [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]
1    [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]
2    [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]
3    [ ] [ ] [ ] [ ] [ ][B][ ] [W][ ]   B=bomb, W=wall(hardblock)
4    [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]
5    [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]


SPREADING RIGHT (col_delta=+1, power=3):
  distance=1: new_col=6, check level_matrix[3][6]
    → Empty "_", create right_mid at (3,6) ✓

  distance=2: new_col=7, check level_matrix[3][7]
    → Hard_block found! isinstance(cell, Hard_block) = True
    → break ✓ (stop spreading)

  distance=3: NOT REACHED (we broke out)


RESULT:
     Col   0   1   2   3   4   5   6   7   8

3    [ ] [ ] [ ] [ ][M][X][M][W][ ]

Only reaches to (3,6), stops before the wall at (3,7)
```

---

## 🎨 Image Type Selection Logic

```python
# Pseudo-code
for direction in [up, down, left, right]:
    for distance in range(1 to power+1):

        is_last_tile = (distance == power)

        if is_last_tile:
            image_type = f"{direction}_end"
            # Examples: "up_end", "down_end", "left_end", "right_end"
        else:
            image_type = f"{direction}_mid"
            # Examples: "up_mid", "down_mid", "left_mid", "right_mid"
```

### Example with power=2:

```
UP spread:
  distance=1 (not last): "up_mid"
  distance=2 (IS last):  "up_end"

DOWN spread:
  distance=1 (not last): "down_mid"
  distance=2 (IS last):  "down_end"

LEFT spread:
  distance=1 (not last): "left_mid"
  distance=2 (IS last):  "left_end"

RIGHT spread:
  distance=1 (not last): "right_mid"
  distance=2 (IS last):  "right_end"
```

---

## 🖼️ Pixel Coordinate Conversion

```
Grid Coordinates → Pixel Coordinates

Bomb at grid (3, 5):
  pixel_x = col * SIZE = 5 * 64 = 320 pixels
  pixel_y = (row * SIZE) + Y_OFFSET = (3 * 64) + 92 = 284 pixels

Explosion spread to grid (1, 5):
  pixel_x = 5 * 64 = 320 pixels
  pixel_y = (1 * 64) + 92 = 156 pixels

Explosion spread to grid (3, 7):
  pixel_x = 7 * 64 = 448 pixels
  pixel_y = (3 * 64) + 92 = 284 pixels

On screen (with camera offset):
  screen_x = pixel_x - camera_x
  screen_y = pixel_y - camera_y
```

---

## 🔗 Data Flow Diagram

```
1. PLANT PHASE
   Player presses SPACE
   └─ Character.input() checks bomb condition
      └─ if bomb_planted < bomb_limit:
         └─ Create Bomb(row, col, power=1, remote=True)
            └─ Bomb.insert_bomb_into_grid()
               └─ bomb_planted += 1

2. ANIMATE PHASE
   Each frame:
   ├─ Bomb.update() calls animation()
   │  └─ Blink animation frames
   └─ Game.update() updates all sprites
      └─ Bomb animates on screen

3. TRIGGER PHASE
   Player presses LEFT CTRL
   └─ Character.input() calls bomb.explode()
      └─ Bomb.explode():
         ├─ self.kill() (remove bomb sprite)
         ├─ Create Explosion at center
         └─ For each direction:
            └─ For each distance:
               └─ Create Explosion at (new_row, new_col)

4. ANIMATE PHASE 2
   Each frame:
   └─ Explosion.update() calls animate()
      ├─ Advance frame index
      ├─ When index reaches max: self.kill()
      └─ Game.draw() renders all explosions with animation

5. CLEANUP PHASE
   └─ All explosions removed after animation
      └─ Bomb.remove_bomb_from_grid()
         └─ bomb_planted -= 1
            └─ Player can plant new bomb!
```

---

## ✅ Summary

| Aspect                | Behavior                                          |
| --------------------- | ------------------------------------------------- |
| **Coordinate System** | Grid-based (row, col) → auto-converted to pixels  |
| **Spreading**         | 4 directions × bomb power tiles                   |
| **Image Types**       | centre, \_end (last), \_mid (middle)              |
| **Collision**         | Stops at edges, hard blocks; destroys soft blocks |
| **Animation**         | 4 frames × 75ms each = 300ms total                |
| **Cleanup**           | All explosions disappear after animation          |

---

🎮 **Now You Can Animate Explosions at Any Coordinate with Proper Spreading!**
