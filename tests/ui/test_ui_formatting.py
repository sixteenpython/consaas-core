from __future__ import annotations

from decision_studio.ui import _display_rows, _display_value, _format_inr


def test_indian_currency_formatting() -> None:
    assert _format_inr(1_200_000) == "₹12,00,000"
    assert _format_inr(-156_600) == "-₹1,56,600"


def test_metric_values_are_human_readable() -> None:
    assert _display_value("indicative total cost ₹", 1_200_000) == "₹12,00,000"
    assert _display_value("rental yield reference %", 3.25) == "3.2%"
    assert _display_value("source_ids", ["nirf_2025", "aishe_2023_24"]) == (
        "nirf_2025 · aishe_2023_24"
    )


def test_structured_mapping_becomes_display_rows() -> None:
    assert _display_rows({"starting salary reference ₹": 1_400_000}) == [
        {"Metric": "Starting salary reference", "Value": "₹14,00,000"}
    ]
