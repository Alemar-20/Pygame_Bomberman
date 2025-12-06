# Explosion Animation Coordinates - Quick Reference

## 🎯 What Was Changed

You wanted to animate the explosion sprite at grid coordinates with proper spreading in all 4 directions.

## 📍 The Fix

### **2 Code Changes Made:**

#### **1. Added Imports (line ~22)**

```python
from blocks import Hard_block, Soft_Block  # For collision detection
```

#### **2. Updated Bomb.explode() Method (line ~382)**

**Changed from:**

- Only creating ONE explosion at center
- No spreading to adjacent tiles

**Changed to:**

- Creates center explosion
- Loops through 4 directions (up, down, left, right)
- For each direction, spreads outward based on bomb power
- Uses correct image type for each tile position
- Stops at walls and blocks

## 🧮 How Coordinates Work

```
Grid Positions (Row, Col):
        0    1    2    3    4
    0  [ ]  [ ]  [ ]  [ ]  [ ]
    1  [ ]  [ ]  [ ]  [ ]  [ ]
    2  [ ]  [ ] [B]  [ ]  [ ]   ← Bomb at (2, 2)
    3  [ ]  [ ]  [ ]  [ ]  [ ]
    4  [ ]  [ ]  [ ]  [ ]  [ ]

With Power=2, spreads to:
        0    1    2    3    4
    0  [ ]  [ ] [E]  [ ]  [ ]   ← up_end
    1  [ ]  [ ] [E]  [ ]  [ ]   ← up_mid
    2  [ ] [E] [B] [E]  [ ]   ← left/centre/right
    3  [ ]  [ ] [E]  [ ]  [ ]   ← down_mid
    4  [ ]  [ ] [E]  [ ]  [ ]   ← down_end
```

## 📐 Direction Vectors

```python
"up":    (row_delta=-1, col_delta=0)   # y decreases
"down":  (row_delta=+1, col_delta=0)   # y increases
"left":  (row_delta=0,  col_delta=-1)  # x decreases
"right": (row_delta=0,  col_delta=+1)  # x increases
```

## 🎨 Image Types Used

```
Centre tile:      "centre"
End tiles (last):  "up_end", "down_end", "left_end", "right_end"
Mid tiles:         "up_mid", "down_mid", "left_mid", "right_mid"
```

## 🔄 Animation Flow

```
1. Bomb explodes (LEFT CTRL pressed)
2. Create Explosion at (bomb_row, bomb_col) with "centre"
3. For each direction:
   - For each distance 1 to power:
     - Create Explosion at (new_row, new_col) with correct type
     - Stop if hit wall
     - Stop if hit block
4. Each Explosion animates for ~4 frames
5. All Explosions disappear after animation
```

## ✅ Test It

```
1. Plant bomb (SPACE)
2. Press LEFT CTRL
3. Watch the pink cross explosion spread out from center
4. See it stop at walls/blocks
5. Watch animation play then disappear
```

---

**Paano ito gumagana sa Tagalog:**

**Pagsasaad ng Problema:**

- Ang explosive ay lumilitaw lang sa gitna, hindi kumalat sa lahat ng directions

**Solusyon (2 Hakbang):**

1. I-import ang block classes para malaman kung may hadlang
2. Baguhin ang explode() method:
   - Gumawa ng center explosion
   - Loop sa 4 directions (pataas, pababa, pakaliwa, pakanan)
   - Para sa bawat direction, kumalat base sa bomb power
   - Gamitin ang tamang sprite image para sa bawat tile
   - Huminto kung may wall o block

**Resulta:**

- Ang explosion ay kumalat nang tama sa lahat ng 4 directions
- Humihinto sa walls at blocks
- Nag-animate ng makintab-intab tungkol 4 frames
- Pagkatapos ay nawala na

---

✅ **Implemented and Ready!**
