"""Contrôle CI : un fond orange interdit la mise en production."""

import re
import unittest
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parents[1] / "home" / "templates" / "home" / "index.html"

ORANGE_VALUES = {
    "orange",
    "#ffa500",
    "#ff8c00",
    "rgb(255,165,0)",
    "rgb(255,140,0)",
}


def extract_body_background(template_text: str) -> str:
    """Retourne la valeur CSS background/background-color déclarée sur body."""
    body_rule = re.search(r"body\s*\{(?P<rules>.*?)\}", template_text, flags=re.IGNORECASE | re.DOTALL)
    if not body_rule:
        raise AssertionError("Aucune règle CSS 'body' trouvée dans le template.")

    declaration = re.search(
        r"background(?:-color)?\s*:\s*(?P<value>[^;]+)",
        body_rule.group("rules"),
        flags=re.IGNORECASE,
    )
    if not declaration:
        raise AssertionError("Aucune couleur de fond n'est déclarée sur body.")
    return re.sub(r"\s+", "", declaration.group("value").lower())


def test_background_is_not_orange() -> None:
    """Échoue explicitement lorsque la couleur de fond est orange."""
    color = extract_body_background(TEMPLATE.read_text(encoding="utf-8"))
    if color in ORANGE_VALUES:
        raise AssertionError(
            f"Déploiement bloqué : le fond '{color}' est orange. "
            "Utilisez un fond bleu ou une autre couleur autorisée."
        )


class BackgroundColorTest(unittest.TestCase):
    def test_background_is_not_orange(self):
        test_background_is_not_orange()


if __name__ == "__main__":
    unittest.main()
