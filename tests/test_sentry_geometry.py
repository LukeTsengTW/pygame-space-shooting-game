import unittest

from sentry_geometry import sentry_barrel_centers, sentry_emitters


class SentryGeometryTests(unittest.TestCase):
    def test_sentry_gun_has_five_barrel_centers_with_center_laser(self):
        centers = sentry_barrel_centers(left=100, top=200, width=48)
        self.assertEqual(len(centers), 5)
        self.assertEqual(centers, ((109, 212), (115, 212), (124, 212), (133, 212), (139, 212)))

    def test_sentry_gun_marks_only_the_center_barrel_as_laser(self):
        emitters = sentry_emitters(left=100, top=200, width=48)
        self.assertEqual(
            emitters,
            (
                ("beam", (109, 212)),
                ("beam", (115, 212)),
                ("laser", (124, 212)),
                ("beam", (133, 212)),
                ("beam", (139, 212)),
            ),
        )


if __name__ == "__main__":
    unittest.main()
