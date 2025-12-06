# Bug Fix: Cannot Plant New Bomb After Explosion

## 🐛 Problem Statement

**Symptom:** After planting a bomb, triggering it to explode (LEFT CTRL), and trying to plant a new bomb (SPACE), the new bomb is rejected and cannot be placed.

**Expected Behavior:** Player should be able to plant a new bomb immediately after the previous bomb explodes.

**Actual Behavior:** Second bomb cannot be planted. The SPACE key does nothing.

---

## 🔍 Root Cause Analysis (Step by Step)

### State Tracking Variable: `bomb_planted`

The player has a counter: `self.bomb_planted` that tracks how many bombs are currently active.

```python
# In Character.__init__():
self.bomb_limit = 1      # Max 1 bomb at a time
self.bomb_planted = 0    # Currently 0 bombs planted
```

### The Bug Flow

#### **Step 1: Initial State**

```
bomb_planted = 0
bomb_limit = 1
```

#### **Step 2: Player Plants First Bomb (Press SPACE)**

```python
# Code in character.input():
if self.GAME.level_matrix[row][col] == "_" and self.bomb_planted < self.bomb_limit:
    # Check: 0 < 1 → TRUE ✅
    Bomb(...)  # Create bomb
```

The Bomb's `insert_bomb_into_grid()` runs:

```python
def insert_bomb_into_grid(self):
    self.GAME.level_matrix[self.row][self.col] = self
    self.GAME.PLAYER.bomb_planted += 1  # Increment: 0 → 1
```

**After Bomb Planted:**

```
bomb_planted = 1
bomb_limit = 1
```

#### **Step 3: Player Triggers Explosion (Press LEFT CTRL)**

```python
bomb_list[-1].explode()
```

Inside `Bomb.explode()`:

```python
def explode(self):
    self.kill()
    Explosion(...)
    self.remove_bomb_from_grid()  # Called here!
```

Inside `remove_bomb_from_grid()` (THE BUG):

```python
def remove_bomb_from_grid(self):
    self.GAME.level_matrix[self.row][self.col] = "_"
    self.GAME.PLAYER.bomb_planted += 1  # ❌ INCREMENTS AGAIN: 1 → 2
```

**After Bomb Explodes:**

```
bomb_planted = 2  ← WRONG! Should be 0
bomb_limit = 1
```

#### **Step 4: Player Tries to Plant Second Bomb (Press SPACE)**

```python
if self.GAME.level_matrix[row][col] == "_" and self.bomb_planted < self.bomb_limit:
    # Check: 2 < 1 → FALSE ❌
    # Bomb NOT created!
```

**Result:** Player is stuck and cannot plant another bomb!

---

## 🧠 Plain English Explanation

Think of `bomb_planted` like a **scoreboard counting active bombs**:

1. **Game starts:** Scoreboard = 0 bombs active
2. **Plant bomb:** Scoreboard incremented to 1 (add bomb)
3. **Bomb explodes:** Scoreboard should go back to 0 (remove bomb)
4. **But instead:** Scoreboard is incremented to 2! (addition instead of subtraction)
5. **Try to plant:** System says "you already have 2 bombs, max is 1" → REJECTED

**The Bug:** The `remove_bomb_from_grid()` method is **adding** to the counter when it should be **subtracting**.

---

## ✅ The Fix

### Location

**File:** `character.py`  
**Class:** `Bomb`  
**Method:** `remove_bomb_from_grid()`  
**Line Range:** ~370–378

### Code Change

#### **BEFORE (Buggy Code):**

```python
def remove_bomb_from_grid(self):
    """Remove the bomb object from the level matrix"""
    self.GAME.level_matrix[self.row][self.col] = "_"
    self.GAME.PLAYER.bomb_planted += 1  # ❌ WRONG: Increments when it should decrement
```

#### **AFTER (Fixed Code):**

```python
def remove_bomb_from_grid(self):
    """Remove the bomb object from the level matrix"""
    self.GAME.level_matrix[self.row][self.col] = "_"
    # OLD CODE (BUG - incremented instead of decremented):
    # self.GAME.PLAYER.bomb_planted += 1

    # NEW CODE (FIX - decrement to reflect bomb removal):
    self.GAME.PLAYER.bomb_planted -= 1  # Subtract 1 so player can plant again
```

**Change Summary:**

- Changed: `+=` to `-=` (increment to decrement)
- Why: When a bomb is removed/exploded, the counter should go down, not up
- Result: Player can plant new bombs after explosions

---

## 📊 State Transitions After Fix

| Event            | bomb_planted | bomb_limit | Can Plant? | Check         |
| ---------------- | ------------ | ---------- | ---------- | ------------- |
| Game Start       | 0            | 1          | ✅ YES     | 0 < 1         |
| Plant Bomb #1    | 1            | 1          | ❌ NO      | 1 < 1 = FALSE |
| Bomb Explodes    | 0            | 1          | ✅ YES     | 0 < 1         |
| Plant Bomb #2    | 1            | 1          | ❌ NO      | 1 < 1 = FALSE |
| Bomb #2 Explodes | 0            | 1          | ✅ YES     | 0 < 1         |

Now the cycle works correctly! ✅

---

## 🧪 How to Test the Fix

### Test 1: Plant → Explode → Plant Again

```
1. Run game
2. Move to empty tile
3. Press SPACE → bomb appears ✅
4. Press LEFT CTRL → explosion appears ✅
5. Press SPACE → NEW bomb appears ✅ (FIXED!)
6. Press LEFT CTRL → NEW explosion appears ✅
```

### Test 2: Rapid Explosions

```
1. Plant bomb #1
2. Immediately press LEFT CTRL
3. Immediately press SPACE
4. Expected: New bomb placed while explosion is still animating ✅
```

### Test 3: Multiple Locations

```
1. Plant bomb at tile (5, 5)
2. Explode it
3. Move to tile (10, 10)
4. Plant bomb at new location ✅
5. Explode it
6. Move to tile (5, 5) again
7. Plant bomb there again ✅
```

---

## 🔗 Related Code (For Reference)

**Character class initialization:**

```python
self.bomb_limit = 1      # Can have 1 bomb active at a time
self.bomb_planted = 0    # Counter for active bombs
```

**Bomb planting check (in Character.input()):**

```python
if self.GAME.level_matrix[row][col] == "_" and self.bomb_planted < self.bomb_limit:
    Bomb(...)  # Only plant if bomb_planted < bomb_limit
```

**Insert bomb (increments counter):**

```python
def insert_bomb_into_grid(self):
    self.GAME.level_matrix[self.row][self.col] = self
    self.GAME.PLAYER.bomb_planted += 1  # ✅ Correct: add 1 when bomb placed
```

**Remove bomb (NOW decrements counter with fix):**

```python
def remove_bomb_from_grid(self):
    self.GAME.level_matrix[self.row][self.col] = "_"
    self.GAME.PLAYER.bomb_planted -= 1  # ✅ Fixed: subtract 1 when bomb removed
```

---

## 💡 Why This Bug Happened

The developer likely copy-pasted the `insert_bomb_into_grid()` logic to `remove_bomb_from_grid()` without changing the `+=` to `-=`. This is a common mistake—the structure of both methods is similar, but the operations should be inverse:

- **Insert:** Add bomb → increment counter
- **Remove:** Delete bomb → decrement counter

Both used `+= 1` instead of one being `+= 1` and the other being `-= 1`.

---

## ✨ Summary

| Aspect             | Details                                                              |
| ------------------ | -------------------------------------------------------------------- |
| **Bug**            | `remove_bomb_from_grid()` increments counter instead of decrementing |
| **Effect**         | After 1st explosion, bomb_planted > bomb_limit, blocking new bombs   |
| **Fix**            | Change `+= 1` to `-= 1` in `remove_bomb_from_grid()`                 |
| **Impact**         | Player can now plant new bombs after explosions                      |
| **Files Modified** | `character.py` (1 line changed)                                      |
| **Testing**        | Plant → Explode → Plant → Explode (cycle should repeat infinitely)   |

---

✅ **Fix Applied and Ready to Test!**
