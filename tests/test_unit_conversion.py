"""Tests for completion functionality that don't require Wolfram|Alpha API calls."""

import collections

import pytest

from wolframalpha_mcp_server.server import (
    UNIT_CATEGORIES,
    handle_completion,
    unit_conversion,
)


class MockPromptRef:
    """Mock MCP PromptRef for testing."""

    def __init__(self, name):
        self.name = name


class MockArgument:
    """Mock MCP Argument for testing."""

    def __init__(self, name, value):
        self.name = name
        self.value = value


class MockContext:
    """Mock MCP Context for testing."""

    def __init__(self, **arguments):
        self.arguments = arguments


@pytest.mark.asyncio
async def test_non_unit_conversion_prompt():
    """Test that non-unit conversion prompts return None."""
    ref = MockPromptRef("other_prompt")
    argument = MockArgument("some_param", "value")

    result = await handle_completion(ref, argument, None)
    assert result is None


@pytest.mark.asyncio
async def test_unit_completion_empty_query():
    """Test unit completion with empty query returns many results."""
    ref = MockPromptRef("unit_conversion")
    argument = MockArgument("from_unit", "")

    result = await handle_completion(ref, argument, None)
    assert result is not None
    assert len(result.values) >= 20  # Should return many units


@pytest.mark.asyncio
async def test_unit_completion_ft_search():
    """Test unit completion with 'ft' query."""
    ref = MockPromptRef("unit_conversion")
    argument = MockArgument("to_unit", "ft")

    result = await handle_completion(ref, argument, None)
    assert result is not None
    # Expected from test.py: ["ft", "ft/s", "ftm"]
    expected_units = ["ft", "ft/s", "ftm"]
    for unit in expected_units:
        assert unit in result.values, f"Expected unit '{unit}' not found in results"


@pytest.mark.asyncio
async def test_unit_completion_meter_search():
    """Test unit completion with 'meter' query."""
    ref = MockPromptRef("unit_conversion")
    argument = MockArgument("from_unit", "meter")

    result = await handle_completion(ref, argument, None)
    assert result is not None
    # Expected from test.py: ["meter", "meters", "centimeter"]
    expected_units = ["meter", "meters", "centimeter"]
    for unit in expected_units:
        assert unit in result.values, f"Expected unit '{unit}' not found in results"


@pytest.mark.asyncio
async def test_unit_completion_feet_search():
    """Test unit completion with 'feet' (irregular plural)."""
    ref = MockPromptRef("unit_conversion")
    argument = MockArgument("to_unit", "feet")

    result = await handle_completion(ref, argument, None)
    assert result is not None
    # Expected from test.py: ["feet", "cubic_feet", "square_feet"]
    expected_units = ["feet", "cubic_feet", "square_feet"]
    for unit in expected_units:
        assert unit in result.values, f"Expected unit '{unit}' not found in results"


@pytest.mark.asyncio
async def test_unit_completion_with_valid_context():
    """Test unit completion with valid context (length category)."""
    ref = MockPromptRef("unit_conversion")
    argument = MockArgument("to_unit", "m")
    context = MockContext(from_unit="foot", value="100")

    result = await handle_completion(ref, argument, context)
    assert result is not None
    # Expected from test.py: ["meter", "meters", "m"]
    expected_units = ["meter", "meters", "m"]
    for unit in expected_units:
        assert unit in result.values, f"Expected unit '{unit}' not found in results"


@pytest.mark.asyncio
async def test_unit_completion_with_invalid_context():
    """Test unit completion with invalid context returns empty."""
    ref = MockPromptRef("unit_conversion")
    argument = MockArgument("to_unit", "m")
    context = MockContext(from_unit="invalid_unit_xyz", value="100")

    result = await handle_completion(ref, argument, context)
    assert result is not None
    assert len(result.values) == 0


@pytest.mark.asyncio
async def test_unit_completion_context_only_value():
    """Test unit completion with only value in context."""
    ref = MockPromptRef("unit_conversion")
    argument = MockArgument("from_unit", "fpm")
    context = MockContext(value="100")

    result = await handle_completion(ref, argument, context)
    assert result is not None
    # Expected from test.py: ["fpm"]
    expected_units = ["fpm"]
    for unit in expected_units:
        assert unit in result.values, f"Expected unit '{unit}' not found in results"


@pytest.mark.asyncio
async def test_unit_completion_case_insensitive():
    """Test unit completion is case insensitive."""
    ref = MockPromptRef("unit_conversion")
    argument = MockArgument("from_unit", "METER")

    result = await handle_completion(ref, argument, None)
    assert result is not None
    assert len(result.values) > 0
    # Should find meter-related units despite uppercase input


def test_unit_categories():
    """Test unit category completeness and structure."""
    # Test that we have categories
    assert len(UNIT_CATEGORIES) > 0, "Should have at least one unit category"

    # Test total units count
    total_units = sum(len(units) for units in UNIT_CATEGORIES.values())
    assert total_units > 50, f"Should have many units, got {total_units}"

    # Test key irregular plurals
    key_plurals = [
        ("length", "foot", "feet"),
        ("volume", "cubic_foot", "cubic_feet"),
        ("area", "square_foot", "square_feet"),
        ("time", "century", "centuries"),
        ("time", "millennium", "millennia"),
        ("length", "nautical_mile", "nautical_miles"),
    ]

    for category, singular, plural in key_plurals:
        assert category in UNIT_CATEGORIES, f"Category '{category}' not found"
        units = UNIT_CATEGORIES[category]
        assert singular in units, f"Missing singular form '{singular}' in {category}"
        assert plural in units, f"Missing plural form '{plural}' in {category}"

    # Test abbreviation coverage
    abbreviations_found = []
    for _category, units in UNIT_CATEGORIES.items():
        short_units = [u for u in units if len(u) <= 3 and u.isalpha()]
        if short_units:
            abbreviations_found.extend(short_units[:3])  # Sample 3 from each

    assert len(abbreviations_found) > 10, "Should have many abbreviations available"


def test_unit_duplicates():
    """Test for duplicate units across categories."""
    # Collect all units and track which categories they appear in
    all_units = []
    unit_to_categories = collections.defaultdict(list)

    for category, units in UNIT_CATEGORIES.items():
        for unit in units:
            all_units.append(unit)
            unit_to_categories[unit].append(category)

    # Find duplicates
    duplicates = {
        unit: categories
        for unit, categories in unit_to_categories.items()
        if len(categories) > 1
    }

    assert len(all_units) > 0, "Should have some units"
    assert len(set(all_units)) > 0, "Should have unique units"

    # Check for duplicates - this should pass if units are properly organized
    if duplicates:
        duplicate_info = []
        for unit, categories in sorted(duplicates.items()):
            duplicate_info.append(f"'{unit}' appears in: {categories}")

        pytest.fail(
            f"Found {len(duplicates)} duplicate units across categories:\n"
            + "\n".join(duplicate_info[:10])  # Show first 10 duplicates
        )


def test_unit_conversion_prompt_basic_length():
    """Test basic length conversion prompt generation."""
    prompt = unit_conversion(100, "meter", "foot", None)

    assert "Value: 100" in prompt
    assert "From unit: meter" in prompt
    assert "To unit: foot" in prompt
    assert len(prompt) > 100  # Should have substantial content


def test_unit_conversion_prompt_with_precision():
    """Test unit conversion prompt with precision."""
    prompt = unit_conversion(75, "kg", "pound", 2)

    assert "Value: 75" in prompt
    assert "From unit: kg" in prompt
    assert "To unit: pound" in prompt
    assert "Precision: 2" in prompt or "2 decimal" in prompt


def test_unit_conversion_prompt_temperature():
    """Test temperature conversion prompt."""
    prompt = unit_conversion(32, "fahrenheit", "celsius", 1)

    assert "Value: 32" in prompt
    assert "From unit: fahrenheit" in prompt
    assert "To unit: celsius" in prompt
    assert isinstance(prompt, str)
    assert len(prompt) > 50


def test_unit_conversion_prompt_aviation():
    """Test aviation units conversion prompt."""
    prompt = unit_conversion(100, "nautical_mile", "kilometer", None)

    assert "Value: 100" in prompt
    assert "From unit: nautical_mile" in prompt
    assert "To unit: kilometer" in prompt
    assert isinstance(prompt, str)


def test_unit_conversion_prompt_irregular_plural():
    """Test conversion with irregular plural (foot to meters)."""
    prompt = unit_conversion(1, "foot", "meter", 3)

    assert "Value: 1" in prompt
    assert "From unit: foot" in prompt
    assert "To unit: meter" in prompt
    assert "Precision: 3" in prompt or "3 decimal" in prompt
