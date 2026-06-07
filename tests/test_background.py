import unittest

from background import ScrollingBackground


class FakeSurface:
    def __init__(self, height):
        self.height = height

    def get_height(self):
        return self.height


class FakeScreen:
    def __init__(self):
        self.calls = []

    def blit(self, surface, position):
        self.calls.append((surface, position))


class ScrollingBackgroundTests(unittest.TestCase):
    def test_advance_wraps_at_image_height(self):
        scroller = ScrollingBackground(FakeSurface(1536), speed=2)
        scroller.offset = 1535

        scroller.advance()

        self.assertEqual(scroller.offset, 1)

    def test_draw_places_two_images_exactly_one_height_apart(self):
        surface = FakeSurface(1536)
        screen = FakeScreen()
        scroller = ScrollingBackground(surface, speed=2)
        scroller.offset = 100

        scroller.draw(screen)

        self.assertEqual(
            screen.calls,
            [(surface, (0, -1436)), (surface, (0, 100))],
        )

    def test_set_surface_preserves_scroll_phase(self):
        first = FakeSurface(1000)
        second = FakeSurface(2000)
        scroller = ScrollingBackground(first, speed=2)
        scroller.offset = 250

        scroller.set_surface(second)

        self.assertEqual(scroller.offset, 500)
