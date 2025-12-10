import pygame
import os

def load_image(path, use_alpha=True):

    if not os.path.isfile(path):
        raise FileNotFoundError(f"Asset not found: {path}")

    ext = os.path.splitext(path)[1].lower()
    inferred_alpha = ext in (".png", ".webp")
    use_alpha = bool(use_alpha and inferred_alpha)

    img = pygame.image.load(path)
    if use_alpha:
        return img.convert_alpha()
    else:
        img = img.convert()
        bg_color = img.get_at((0, 0))
        img.set_colorkey(bg_color)
        return img

def _make_fallback_surface(size, color=(70, 70, 200)):
    surf = pygame.Surface(size, pygame.SRCALPHA)
    surf.fill(color)
    return surf

def load_assets():
    assets = {}

    try:
        assets["bg"] = load_image("homeMenu_bg.jpg", use_alpha=False)
    except Exception:
        assets["bg"] = _make_fallback_surface((800, 600), color=(30, 30, 30))

    # NOTE: make sure this is a sequence of tuples — not a bare tuple chain.
    # The correct form is either a list of tuples or a tuple of tuples, for example:
    for key, filename in (
        ("start_btn",  "start_btn.jpg"),
    ):
        try:
            assets[key] = load_image(filename, use_alpha=False)
        except Exception:
            assets[key] = _make_fallback_surface((180, 60), color=(70, 70, 200))

    try:
        assets["font"] = pygame.font.Font("assets/geometry_dash_font.ttf", 40)
    except Exception:
        assets["font"] = pygame.font.SysFont("Arial", 40)

    return assets