from typing import Dict, List, Tuple, Any
import re
import json
import os
from difflib import get_close_matches


class ProductNameNormalizationService:
    """
    AI service for normalizing product names with learning capabilities.
    Fixes common Polish typos and learns from user corrections.
    """

    def __init__(self):
        """Initialize with Polish product corrections and load learned data."""
        self.built_in_typo_fixes = {
            "mlko": "mleko",
            "chlb": "chleb",
            "maslo": "masło",
            "jogrt": "jogurt",
            "kielbsa": "kiełbasa",
            "marchw": "marchew",
            "ziemniak": "ziemniaki",
            "pomidor": "pomidory",
            "banan": "banany",
            "jablko": "jabłka",
        }

        # Brand standardizations
        self.brands = {
            "coca cola": "Coca-Cola",
            "pepsi": "Pepsi",
            "sprite": "Sprite",
            "danone": "Danone",
        }

        # Path for learned data
        self.learned_data_path = "data/learned_typos.json"

        # Load learned typo fixes
        self.learned_typo_fixes = self._load_learned_typos()

        # Combined typo fixes (built-in + learned)
        self.typo_fixes = {**self.built_in_typo_fixes, **self.learned_typo_fixes}

    def normalize_name(self, name: str) -> Dict[str, Any]:
        """
        Normalize product name and return details.

        :param name: Original name
        :return: Dict with original, normalized name and changes
        """
        if not name:
            return {"original": "", "normalized": "", "improved": False, "changes": []}

        original = name
        changes = []

        # Step 1: Basic cleanup
        normalized = self._clean_whitespace(name)
        if normalized != name:
            changes.append("Fixed spacing")

        # Step 2: Fix typos
        normalized = self._fix_typos(normalized)
        if normalized != self._clean_whitespace(name):
            changes.append("Fixed typos")

        # Step 3: Fix brands
        normalized = self._fix_brands(normalized)

        # Step 4: Proper capitalization
        normalized = self._capitalize_properly(normalized)
        if normalized != self._fix_brands(
            self._fix_typos(self._clean_whitespace(name))
        ):
            changes.append("Fixed capitalization")

        return {
            "original": original,
            "normalized": normalized,
            "improved": original != normalized,
            "changes": changes,
        }

    def _clean_whitespace(self, text: str) -> str:
        """Remove extra whitespace."""
        return re.sub(r"\s+", " ", text.strip())

    def _fix_typos(self, text: str) -> str:
        """Fix common Polish typos."""
        words = text.lower().split()
        fixed_words = []

        for word in words:
            if word in self.typo_fixes:
                fixed_words.append(self.typo_fixes[word])
            else:
                fixed_words.append(word)

        return " ".join(fixed_words)

    def _fix_brands(self, text: str) -> str:
        """Fix brand names."""
        lower_text = text.lower()
        for brand_lower, brand_proper in self.brands.items():
            lower_text = lower_text.replace(brand_lower, brand_proper)
        return lower_text

    def _capitalize_properly(self, text: str) -> str:
        """Apply proper capitalization."""
        words = text.split()
        capitalized = []

        for i, word in enumerate(words):
            if i == 0 or word.lower() not in ["i", "w", "z", "na", "do", "od"]:
                capitalized.append(word.capitalize())
            else:
                capitalized.append(word.lower())

        return " ".join(capitalized)

    def find_similar_products(
        self, name: str, existing_names: List[str]
    ) -> List[Tuple[str, float]]:
        """Find similar product names (simple version)."""
        name_lower = name.lower()
        similar = []

        for existing in existing_names:
            existing_lower = existing.lower()

            # Simple similarity check
            if name_lower != existing_lower:
                if name_lower in existing_lower or existing_lower in name_lower:
                    similarity = min(len(name_lower), len(existing_lower)) / max(
                        len(name_lower), len(existing_lower)
                    )
                    if similarity > 0.7:
                        similar.append((existing, similarity))

        return sorted(similar, key=lambda x: x[1], reverse=True)[:3]

    def _load_learned_typos(self) -> Dict[str, str]:
        """Load learned typo fixes from file."""
        try:
            if os.path.exists(self.learned_data_path):
                with open(self.learned_data_path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    def _save_learned_typos(self):
        """Save learned typo fixes to file."""
        try:
            os.makedirs(os.path.dirname(self.learned_data_path), exist_ok=True)
            with open(self.learned_data_path, "w", encoding="utf-8") as f:
                json.dump(self.learned_typo_fixes, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def add_learned_typo(self, typo: str, correct: str):
        """
        Add a new typo correction to the learned dictionary.

        :param typo: The incorrect word
        :param correct: The correct word
        """
        typo_lower = typo.lower().strip()
        correct_formatted = correct.strip()

        if typo_lower and correct_formatted and typo_lower != correct_formatted.lower():
            self.learned_typo_fixes[typo_lower] = correct_formatted.lower()
            self.typo_fixes = {**self.built_in_typo_fixes, **self.learned_typo_fixes}
            self._save_learned_typos()

    def find_typo_suggestions(
        self, word: str, max_suggestions: int = 3
    ) -> List[Tuple[str, float]]:
        """
        Find potential typo corrections using AI fuzzy matching.

        :param word: Word to find corrections for
        :param max_suggestions: Maximum number of suggestions
        :return: List of (correction, confidence) tuples
        """
        word_lower = word.lower().strip()

        # First check direct matches
        if word_lower in self.typo_fixes:
            return [(self.typo_fixes[word_lower], 1.0)]

        # Get all possible correct words (values from typo_fixes + common words)
        all_correct_words = list(set(self.typo_fixes.values()))
        all_correct_words.extend(
            [
                "mleko",
                "chleb",
                "masło",
                "jogurt",
                "kiełbasa",
                "marchew",
                "ziemniaki",
                "pomidory",
                "banany",
                "jabłka",
                "cebula",
                "czosnek",
            ]
        )

        # Use difflib to find close matches
        close_matches = get_close_matches(
            word_lower, all_correct_words, n=max_suggestions, cutoff=0.6
        )

        # Calculate confidence scores
        suggestions = []
        for match in close_matches:
            # Simple confidence calculation based on similarity
            max_len = max(len(word_lower), len(match))
            min_len = min(len(word_lower), len(match))
            confidence = min_len / max_len if max_len > 0 else 0.0

            # Boost confidence for exact substring matches
            if word_lower in match or match in word_lower:
                confidence = min(confidence + 0.2, 1.0)

            suggestions.append((match, confidence))

        return sorted(suggestions, key=lambda x: x[1], reverse=True)

    def find_smart_suggestions(
        self, name: str, max_suggestions: int = 5
    ) -> List[Tuple[str, float, str]]:
        """
        Find smart suggestions for entire product name using advanced AI logic.

        :param name: Full product name to analyze
        :param max_suggestions: Maximum number of suggestions
        :return: List of (suggestion, confidence, reason) tuples
        """
        name_lower = name.lower().strip()
        words = name_lower.split()

        suggestions = []

        # Check each word for potential improvements
        for word in words:
            word_suggestions = self.find_typo_suggestions(word, max_suggestions)

            for suggestion, confidence in word_suggestions:
                if (
                    confidence > 0.7 and suggestion != word
                ):  # High confidence suggestions
                    # Create full name suggestion by replacing the word
                    suggested_name = name_lower.replace(word, suggestion)
                    reason = f"'{word}' → '{suggestion}'"
                    suggestions.append((suggested_name, confidence, reason))

        # Remove duplicates and sort by confidence
        unique_suggestions: Dict[str, Tuple[str, float, str]] = {}
        for suggestion, confidence, reason in suggestions:
            if (
                suggestion not in unique_suggestions
                or unique_suggestions[suggestion][1] < confidence
            ):
                unique_suggestions[suggestion] = (suggestion, confidence, reason)

        return sorted(unique_suggestions.values(), key=lambda x: x[1], reverse=True)[
            :max_suggestions
        ]

    def has_potential_typos(self, name: str, confidence_threshold: float = 0.6) -> bool:
        """
        Quick check if a name potentially has typos.

        :param name: Product name to check
        :param confidence_threshold: Minimum confidence for suggestions
        :return: True if potential typos found
        """
        words = name.lower().split()

        for word in words:
            suggestions = self.find_typo_suggestions(word, 1)
            if suggestions and suggestions[0][1] > confidence_threshold:
                return True

        return False

    def get_word_suggestions_details(self, name: str) -> Dict[str, Any]:
        """
        Get detailed analysis of each word in the name.

        :param name: Product name to analyze
        :return: Dictionary with word analysis details
        """
        words = name.lower().split()
        word_analysis = {}

        for word in words:
            suggestions = self.find_typo_suggestions(word, 3)
            word_analysis[word] = {
                "suggestions": suggestions,
                "has_suggestions": len(suggestions) > 0 and suggestions[0][1] > 0.6,
                "best_suggestion": suggestions[0] if suggestions else None,
            }

        return {
            "original_name": name,
            "words": word_analysis,
            "has_any_suggestions": any(
                details["has_suggestions"] for details in word_analysis.values()
            ),
        }

    def get_learning_stats(self) -> Dict[str, Any]:
        """
        Get statistics about learned typos.

        :return: Dictionary with learning statistics
        """
        return {
            "built_in_typos": len(self.built_in_typo_fixes),
            "learned_typos": len(self.learned_typo_fixes),
            "total_typos": len(self.typo_fixes),
            "learned_examples": list(self.learned_typo_fixes.items())[
                :10
            ],  # Show first 10
        }
