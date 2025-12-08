import pygame
import sys
from assets2 import load_assets

pygame.init()

SCREEN_SIZE = (800, 600)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Home Menu")
clock = pygame.time.Clock()

assets = load_assets()

class Button:
    def __init__(self, text, x, y, width, height, font, image=None, callback=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.base_color = (70, 70, 200)
        self.hover_color = (120, 120, 255)
        self.current_color = self.base_color
        self.font = font
        self.scale = 1.0
        self.image = image
        self.callback = callback
        self._is_hover = False

    def draw(self, surface):
        # scale for hover effect
        scaled_w = max(1, int(self.rect.width * self.scale))
        scaled_h = max(1, int(self.rect.height * self.scale))
        scaled_x = int(self.rect.x - (scaled_w - self.rect.width) / 2)
        scaled_y = int(self.rect.y - (scaled_h - self.rect.height) / 2)
        scaled_rect = pygame.Rect(scaled_x, scaled_y, scaled_w, scaled_h)

        # --- DRAW IMAGE BUTTON ---
        if self.image:
            img = pygame.transform.smoothscale(self.image, (scaled_w, scaled_h))
            surface.blit(img, scaled_rect)

            # overlay when hovered
            if self._is_hover:
                overlay = pygame.Surface((scaled_w, scaled_h), pygame.SRCALPHA)
                overlay.fill((255, 255, 255, 40))
                surface.blit(overlay, scaled_rect)

            # TEXT ON IMAGE (✔ added)
            text_surf = self.font.render(self.text, True, (255, 255, 255))
            surface.blit(text_surf, text_surf.get_rect(center=scaled_rect.center))

        # --- DRAW NORMAL RECT BUTTON ---
        else:
            pygame.draw.rect(surface, self.current_color, scaled_rect, border_radius=10)
            text_surf = self.font.render(self.text, True, (255, 255, 255))
            surface.blit(text_surf, text_surf.get_rect(center=scaled_rect.center))

    def update(self, mouse_pos):
        # hover effect
        self._is_hover = self.rect.collidepoint(mouse_pos)
        if self._is_hover:
            self.current_color = self.hover_color
            self.scale = min(1.15, self.scale + 0.04)
        else:
            self.current_color = self.base_color
            self.scale = max(1.0, self.scale - 0.04)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()

# --- CALLBACKS ---
def start_game():
    print("START pressed - implement game start logic here")


# asset helper
def maybe_image(name):
    return assets.get(name)

# button generator
def create_row_buttons(labels, image_keys, callbacks, y=300, btn_w=180, btn_h=60, spacing=40):
    n = len(labels)
    total_w = n * btn_w + (n - 1) * spacing
    start_x = (SCREEN_SIZE[0] - total_w) // 2
    btns = []

    for i, label in enumerate(labels):
        x = start_x + i * (btn_w + spacing)
        img = maybe_image(image_keys[i]) if image_keys else None
        btn = Button(label, x, y, btn_w, btn_h, font=assets["font"], image=img, callback=callbacks[i])
        btns.append(btn)

    return btns

labels = ["START"]
image_keys = ["start_btn"]
callbacks = [start_game]

buttons = create_row_buttons(labels, image_keys, callbacks)

running = True
while running:
    events = pygame.event.get()
    mouse_pos = pygame.mouse.get_pos()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
        for b in buttons:
            b.handle_event(event)

    for b in buttons:
        b.update(mouse_pos)

    # background
    bg = assets.get("bg")
    if bg:
        if bg.get_size() != SCREEN_SIZE:
            bg_draw = pygame.transform.smoothscale(bg, SCREEN_SIZE)
        else:
            bg_draw = bg
        screen.blit(bg_draw, (0, 0))
    else:
        screen.fill((30, 30, 30))

    # draw buttons
    for b in buttons:
        b.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
