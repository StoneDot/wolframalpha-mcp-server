"""Wolfram|Alpha MCP Server implementation."""

import os

import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Initialize the FastMCP server
mcp = FastMCP(name="wolframalpha-llm")

# Unit categories for completions
UNIT_CATEGORIES = {
    "length": [
        # Full names (singular and plural)
        "meter",
        "meters",
        "foot",
        "feet",
        "inch",
        "inches",
        "centimeter",
        "centimeters",
        "kilometer",
        "kilometers",
        "mile",
        "miles",
        "yard",
        "yards",
        "millimeter",
        "millimeters",
        "micrometer",
        "micrometers",
        "nanometer",
        "nanometers",
        "picometer",
        "picometers",
        "nautical_mile",
        "nautical_miles",
        "statute_mile",
        "statute_miles",
        "fathom",
        "fathoms",
        "furlong",
        "furlongs",
        "chain",
        "chains",
        "flight_level",
        "flight_levels",
        # Abbreviations
        "m",
        "ft",
        "in",
        "cm",
        "km",
        "mi",
        "yd",
        "mm",
        "μm",
        "nm",
        "pm",
        "nmi",
        "sm",
        "ftm",
        "FL",
    ],
    "weight": [
        # Full names (singular and plural)
        "kilogram",
        "kilograms",
        "gram",
        "grams",
        "ounce",
        "ounces",
        "ton",
        "tons",
        "stone",
        "stones",
        "milligram",
        "milligrams",
        "microgram",
        "micrograms",
        "metric_ton",
        "metric_tons",
        "short_ton",
        "short_tons",
        "long_ton",
        "long_tons",
        "grain",
        "grains",
        "carat",
        "carats",
        "troy_ounce",
        "troy_ounces",
        # Abbreviations
        "kg",
        "lb",
        "oz",
        "t",
        "st",
        "mg",
        "μg",
        "tonne",
    ],
    "temperature": [
        # Full names (singular and plural)
        "celsius",
        "fahrenheit",
        "kelvin",
        "rankine",
        "degree_celsius",
        "degrees_celsius",
        "degree_fahrenheit",
        "degrees_fahrenheit",
        # Abbreviations
        "K",
        "R",
        "°C",
        "°F",
        "°K",
        "°R",
    ],
    "time": [
        # Full names (singular and plural)
        "second",
        "seconds",
        "minute",
        "minutes",
        "hour",
        "hours",
        "day",
        "days",
        "week",
        "weeks",
        "month",
        "months",
        "year",
        "years",
        "millisecond",
        "milliseconds",
        "microsecond",
        "microseconds",
        "nanosecond",
        "nanoseconds",
        "decade",
        "decades",
        "century",
        "centuries",
        "millennium",
        "millennia",
        # Abbreviations
        "s",
        "min",
        "h",
        "d",
        "w",
        "mo",
        "yr",
        "ms",
        "μs",
        "ns",
    ],
    "volume": [
        # Full names (singular and plural)
        "liter",
        "liters",
        "gallon",
        "gallons",
        "quart",
        "quarts",
        "pint",
        "pints",
        "cup",
        "cups",
        "fluid_ounce",
        "fluid_ounces",
        "milliliter",
        "milliliters",
        "cubic_meter",
        "cubic_meters",
        "cubic_foot",
        "cubic_feet",
        "cubic_inch",
        "cubic_inches",
        "barrel",
        "barrels",
        "imperial_gallon",
        "imperial_gallons",
        "us_gallon",
        "us_gallons",
        "tablespoon",
        "tablespoons",
        "teaspoon",
        "teaspoons",
        "cubic_centimeter",
        "cubic_centimeters",
        # Abbreviations
        "L",
        "l",
        "qt",
        "pt",
        "fl_oz",
        "ml",
        "m³",
        "ft³",
        "in³",
        "bbl",
        "tbsp",
        "tsp",
        "cc",
        "cm³",
    ],
    "area": [
        # Full names (singular and plural)
        "square_meter",
        "square_meters",
        "square_foot",
        "square_feet",
        "acre",
        "acres",
        "hectare",
        "hectares",
        "square_inch",
        "square_inches",
        "square_mile",
        "square_miles",
        "square_kilometer",
        "square_kilometers",
        "square_centimeter",
        "square_centimeters",
        "square_millimeter",
        "square_millimeters",
        "square_yard",
        "square_yards",
        # Abbreviations
        "m²",
        "ft²",
        "ac",
        "ha",
        "in²",
        "mi²",
        "km²",
        "cm²",
        "mm²",
        "yd²",
    ],
    "pressure": [
        # Full names (singular and plural)
        "pascal",
        "pascals",
        "bar",
        "bars",
        "atmosphere",
        "atmospheres",
        "psi",
        "torr",
        "torrs",
        "mmHg",
        "inHg",
        "millibar",
        "millibars",
        "kilopascal",
        "kilopascals",
        "megapascal",
        "megapascals",
        "hectopascal",
        "hectopascals",
        # Abbreviations
        "Pa",
        "atm",
        "mbar",
        "kPa",
        "MPa",
        "hPa",
    ],
    "energy": [
        # Full names (singular and plural)
        "joule",
        "joules",
        "calorie",
        "calories",
        "kilowatt_hour",
        "kilowatt_hours",
        "btu",
        "btus",
        "erg",
        "ergs",
        "electron_volt",
        "electron_volts",
        "kilojoule",
        "kilojoules",
        "megajoule",
        "megajoules",
        "foot_pound",
        "foot_pounds",
        "therm",
        "therms",
        "kilocalorie",
        "kilocalories",
        # Abbreviations
        "J",
        "cal",
        "kWh",
        "BTU",
        "eV",
        "kJ",
        "MJ",
        "ft·lb",
        "kcal",
    ],
    "power": [
        # Full names (singular and plural)
        "watt",
        "watts",
        "horsepower",
        "kilowatt",
        "kilowatts",
        "btu_per_hour",
        "foot_pound_per_second",
        "metric_horsepower",
        "electrical_horsepower",
        "megawatt",
        "megawatts",
        "gigawatt",
        "gigawatts",
        # Abbreviations
        "W",
        "hp",
        "kW",
        "BTU/h",
        "ft·lb/s",
        "MW",
        "GW",
    ],
    "speed": [
        # Full names (singular and plural)
        "meter_per_second",
        "meters_per_second",
        "kilometer_per_hour",
        "kilometers_per_hour",
        "mile_per_hour",
        "miles_per_hour",
        "knot",
        "knots",
        "foot_per_second",
        "feet_per_second",
        "feet_per_minute",
        "mach",
        "speed_of_light",
        "speed_of_sound",
        # Abbreviations
        "m/s",
        "km/h",
        "mph",
        "kn",
        "kt",
        "ft/s",
        "fps",
        "fpm",
        "c",
    ],
    "angle": [
        # Full names (singular and plural)
        "degree",
        "degrees",
        "radian",
        "radians",
        "gradian",
        "gradians",
        "milliradian",
        "milliradians",
        "arcsecond",
        "arcseconds",
        "arcminute",
        "arcminutes",
        "turn",
        "turns",
        "revolution",
        "revolutions",
        # Abbreviations
        "°",
        "deg",
        "rad",
        "grad",
        "mrad",
        "arcsec",
        "arcmin",
        "rev",
    ],
    "electrical_current": [
        # Full names (singular and plural)
        "ampere",
        "amperes",
        "milliampere",
        "milliamperes",
        "microampere",
        "microamperes",
        "kiloampere",
        "kiloamperes",
        "nanoampere",
        "nanoamperes",
        # Abbreviations
        "A",
        "mA",
        "μA",
        "kA",
        "nA",
    ],
    "voltage": [
        # Full names (singular and plural)
        "volt",
        "volts",
        "millivolt",
        "millivolts",
        "microvolt",
        "microvolts",
        "kilovolt",
        "kilovolts",
        "megavolt",
        "megavolts",
        # Abbreviations
        "V",
        "mV",
        "μV",
        "kV",
        "MV",
    ],
    "electrical_resistance": [
        # Full names (singular and plural)
        "ohm",
        "ohms",
        "milliohm",
        "milliohms",
        "kiloohm",
        "kiloohms",
        "megaohm",
        "megaohms",
        "gigaohm",
        "gigaohms",
        # Abbreviations
        "Ω",
        "mΩ",
        "kΩ",
        "MΩ",
        "GΩ",
    ],
    "electrical_capacitance": [
        # Full names (singular and plural)
        "farad",
        "farads",
        "microfarad",
        "microfarads",
        "nanofarad",
        "nanofarads",
        "picofarad",
        "picofarads",
        "millifarad",
        "millifarads",
        # Abbreviations
        "F",
        "μF",
        "nF",
        "pF",
        "mF",
    ],
    "electrical_charge": [
        # Full names (singular and plural)
        "coulomb",
        "coulombs",
        "millicoulomb",
        "millicoulombs",
        "microcoulomb",
        "microcoulombs",
        "nanocoulomb",
        "nanocoulombs",
        "electron_charge",
        # Abbreviations
        "C",
        "mC",
        "μC",
        "nC",
        "e",
    ],
    "electrical_conductance": [
        # Full names (singular and plural)
        "siemens",
        "millisiemens",
        "microsiemens",
        "kilosiemens",
        # Abbreviations
        "S",
        "mS",
        "μS",
        "kS",
    ],
    "acceleration": [
        # Full names (singular and plural)
        "meter_per_second_squared",
        "meters_per_second_squared",
        "foot_per_second_squared",
        "feet_per_second_squared",
        "gal",
        "galileo",
        "galileos",
        "gravity",
        # Abbreviations
        "m/s²",
        "ft/s²",
        "g",
    ],
    "force": [
        # Full names (singular and plural)
        "newton",
        "newtons",
        "kilonewton",
        "kilonewtons",
        "meganewton",
        "meganewtons",
        "dyne",
        "dynes",
        "pound_force",
        "pounds_force",
        "kilogram_force",
        "kilograms_force",
        "ton_force",
        "tons_force",
        "ounce_force",
        "ounces_force",
        # Abbreviations
        "N",
        "kN",
        "MN",
        "dyn",
        "lbf",
        "kgf",
        "tonf",
        "ozf",
    ],
    "momentum": [
        # Full names (singular and plural)
        "kilogram_meter_per_second",
        "kilogram_meters_per_second",
        "newton_second",
        "newton_seconds",
        "pound_foot_per_second",
        "pound_feet_per_second",
        # Abbreviations
        "kg⋅m/s",
        "N⋅s",
        "lb⋅ft/s",
    ],
    "angular_acceleration": [
        # Full names (singular and plural)
        "radian_per_second_squared",
        "radians_per_second_squared",
        "degree_per_second_squared",
        "degrees_per_second_squared",
        "revolution_per_second_squared",
        "revolutions_per_second_squared",
        # Abbreviations
        "rad/s²",
        "deg/s²",
        "rev/s²",
    ],
    "magnetic_flux": [
        # Full names (singular and plural)
        "weber",
        "webers",
        "milliweber",
        "milliwebers",
        "microweber",
        "microwebers",
        "maxwell",
        "maxwells",
        # Abbreviations
        "Wb",
        "mWb",
        "μWb",
        "Mx",
    ],
    "magnetic_flux_density": [
        # Full names (singular and plural)
        "tesla",
        "teslas",
        "millitesla",
        "milliteslas",
        "microtesla",
        "microteslas",
        "nanotesla",
        "nanoteslas",
        "gauss",
        "kilogauss",
        # Abbreviations
        "T",
        "mT",
        "μT",
        "nT",
        "G",
        "kG",
    ],
    "inductance": [
        # Full names (singular and plural)
        "henry",
        "henries",
        "millihenry",
        "millihenries",
        "microhenry",
        "microhenries",
        "nanohenry",
        "nanohenries",
        "picohenry",
        "picohenries",
        # Abbreviations
        "H",
        "mH",
        "μH",
        "nH",
        "pH",
    ],
    "electric_field": [
        # Full names (singular and plural)
        "volt_per_meter",
        "volts_per_meter",
        "newton_per_coulomb",
        "newtons_per_coulomb",
        "kilovolt_per_meter",
        "kilovolts_per_meter",
        # Abbreviations
        "V/m",
        "N/C",
        "kV/m",
    ],
    "resistivity": [
        # Full names (singular and plural)
        "ohm_meter",
        "ohm_meters",
        "microohm_meter",
        "microohm_meters",
        "milliohm_meter",
        "milliohm_meters",
        # Abbreviations
        "Ω⋅m",
        "μΩ⋅m",
        "mΩ⋅m",
    ],
    "currency": [
        # Major currencies
        "dollar",
        "dollars",
        "euro",
        "euros",
        "yen",
        "pound",
        "pounds",
        "yuan",
        "franc",
        "francs",
        "ruble",
        "rubles",
        "rupee",
        "rupees",
        "won",
        "peso",
        "pesos",
        "real",
        "reals",
        "rand",
        "krona",
        "kronor",
        "shekel",
        "shekels",
        "dinar",
        "dinars",
        "dirham",
        "dirhams",
        # Abbreviations and symbols
        "USD",
        "EUR",
        "JPY",
        "GBP",
        "CNY",
        "CHF",
        "RUB",
        "INR",
        "KRW",
        "MXN",
        "BRL",
        "ZAR",
        "SEK",
        "ILS",
        "JOD",
        "AED",
        "$",
        "€",
        "¥",
        "£",
        "₹",
        "₽",
        "₩",
        "₨",
        "＄",
    ],
    "specific_heat": [
        # Full names (singular and plural)
        "joule_per_kilogram_kelvin",
        "joules_per_kilogram_kelvin",
        "calorie_per_gram_celsius",
        "calories_per_gram_celsius",
        "btu_per_pound_fahrenheit",
        "btus_per_pound_fahrenheit",
        # Abbreviations
        "J/(kg⋅K)",
        "cal/(g⋅°C)",
        "BTU/(lb⋅°F)",
    ],
    "thermal_conductivity": [
        # Full names (singular and plural)
        "watt_per_meter_kelvin",
        "watts_per_meter_kelvin",
        "calorie_per_second_centimeter_celsius",
        "calories_per_second_centimeter_celsius",
        # Abbreviations
        "W/(m⋅K)",
        "cal/(s⋅cm⋅°C)",
    ],
    "frequency": [
        # Full names (singular and plural)
        "hertz",
        "kilohertz",
        "megahertz",
        "gigahertz",
        "terahertz",
        "cycle_per_second",
        "cycles_per_second",
        # Abbreviations
        "Hz",
        "kHz",
        "MHz",
        "GHz",
        "THz",
        "cps",
    ],
    "angular_velocity": [
        # Full names (singular and plural)
        "radian_per_second",
        "radians_per_second",
        "degree_per_second",
        "degrees_per_second",
        "revolution_per_minute",
        "revolutions_per_minute",
        "revolution_per_second",
        "revolutions_per_second",
        # Abbreviations
        "rad/s",
        "deg/s",
        "rpm",
        "rps",
    ],
    "density": [
        # Full names (singular and plural)
        "kilogram_per_cubic_meter",
        "kilograms_per_cubic_meter",
        "gram_per_cubic_centimeter",
        "grams_per_cubic_centimeter",
        "pound_per_cubic_foot",
        "pounds_per_cubic_foot",
        "gram_per_milliliter",
        "grams_per_milliliter",
        "kilogram_per_liter",
        "kilograms_per_liter",
        "ounce_per_cubic_inch",
        "ounces_per_cubic_inch",
        # Abbreviations
        "kg/m³",
        "g/cm³",
        "lb/ft³",
        "g/mL",
        "kg/L",
        "oz/in³",
    ],
    "viscosity": [
        # Full names (singular and plural)
        "pascal_second",
        "pascal_seconds",
        "poise",
        "centipoise",
        "stoke",
        "stokes",
        "centistoke",
        "centistokes",
        # Abbreviations
        "Pa⋅s",
        "P",
        "cP",
        "St",
        "cSt",
    ],
    "torque": [
        # Full names (singular and plural)
        "newton_meter",
        "newton_meters",
        "foot_pound_torque",
        "foot_pounds_torque",
        "inch_pound",
        "inch_pounds",
        "kilogram_force_meter",
        "kilogram_force_meters",
        "dyne_centimeter",
        "dyne_centimeters",
        # Abbreviations
        "N⋅m",
        "in⋅lb",
        "kgf⋅m",
        "dyn⋅cm",
    ],
    "flow_rate": [
        # Full names (singular and plural)
        "cubic_meter_per_second",
        "cubic_meters_per_second",
        "liter_per_minute",
        "liters_per_minute",
        "gallon_per_minute",
        "gallons_per_minute",
        "cubic_foot_per_minute",
        "cubic_feet_per_minute",
        "barrel_per_day",
        "barrels_per_day",
        "liter_per_second",
        "liters_per_second",
        # Abbreviations
        "m³/s",
        "L/min",
        "gpm",
        "cfm",
        "bbl/day",
        "L/s",
    ],
    "concentration": [
        # Full names (singular and plural)
        "mole_per_liter",
        "moles_per_liter",
        "gram_per_liter",
        "grams_per_liter",
        "milligram_per_liter",
        "milligrams_per_liter",
        "part_per_million",
        "parts_per_million",
        "part_per_billion",
        "parts_per_billion",
        "percent",
        "percent_by_weight",
        "percent_by_volume",
        # Abbreviations
        "mol/L",
        "M",
        "g/L",
        "mg/L",
        "ppm",
        "ppb",
        "%",
        "wt%",
        "vol%",
    ],
    "luminous_intensity": [
        # Full names (singular and plural)
        "candela",
        "candelas",
        "lumen",
        "lumens",
        "lux",
        "foot_candle",
        "foot_candles",
        "candela_per_square_meter",
        "candela_per_square_foot",
        "lambert",
        "lamberts",
        # Abbreviations
        "cd",
        "lm",
        "lx",
        "fc",
        "cd/m²",
        "cd/ft²",
    ],
    "radioactivity": [
        # Full names (singular and plural)
        "becquerel",
        "becquerels",
        "curie",
        "curies",
        "millicurie",
        "millicuries",
        "microcurie",
        "microcuries",
        "sievert",
        "sieverts",
        "millisievert",
        "millisieverts",
        "gray",
        "grays",
        "rads",
        "rems",
        "roentgen",
        "roentgens",
        # Abbreviations
        "Bq",
        "Ci",
        "mCi",
        "μCi",
        "Sv",
        "mSv",
        "Gy",
    ],
    "surface_tension": [
        # Full names (singular and plural)
        "newton_per_meter",
        "newtons_per_meter",
        "dyne_per_centimeter",
        "dynes_per_centimeter",
        "millinewton_per_meter",
        "millinewtons_per_meter",
        # Abbreviations
        "N/m",
        "dyn/cm",
        "mN/m",
    ],
    "moment_of_inertia": [
        # Full names (singular and plural)
        "kilogram_square_meter",
        "kilogram_square_meters",
        "gram_square_centimeter",
        "gram_square_centimeters",
        "pound_square_foot",
        "pound_square_feet",
        "ounce_square_inch",
        "ounce_square_inches",
        # Abbreviations
        "kg⋅m²",
        "g⋅cm²",
        "lb⋅ft²",
        "oz⋅in²",
    ],
}

WOLFRAM_BASE_URL = "https://www.wolframalpha.com/api/v1/llm-api"


class WolframResult(BaseModel):
    """Structured result from Wolfram|Alpha API query."""

    success: bool
    query: str
    result: str | None = None
    characters: int | None = None
    error: str | None = None
    status_code: int | None = None
    suggestion: str | None = None
    response_text: str | None = None


def get_app_id() -> str:
    """Get Wolfram|Alpha App ID from environment variable."""
    app_id = os.getenv("WOLFRAM_APP_ID")
    if not app_id:
        raise ValueError("WOLFRAM_APP_ID environment variable is required")
    return app_id


@mcp.tool()
def query_wolfram(
    query: str,
    maxchars: int | None = None,
    units: str | None = None,
    location: str | None = None,
) -> WolframResult:
    """
    Query the Wolfram|Alpha LLM API for computational results and knowledge.

    IMPORTANT USAGE GUIDELINES:

    SUPPORTED TOPICS:
    - Mathematics: calculations, derivatives, integrals, equations, statistics
    - Physics: constants, formulas, unit conversions, physical properties
    - Chemistry: elements, compounds, reactions, molecular properties
    - Geography: countries, cities, populations, geographic data
    - History: dates, events, historical figures, timelines
    - Art: artists, artworks, cultural information
    - Astronomy: celestial objects, astronomical data, space facts
    - General knowledge: facts, comparisons, data analysis

    QUERY OPTIMIZATION:
    - Convert complex questions to simple keyword queries when possible
      Example: "How many people live in France?" → "France population"
    - Use English only - translate non-English queries before sending
    - Keep queries concise and specific for best results
    - For multiple data properties, make separate calls for each property

    MATHEMATICAL NOTATION:
    - Always use proper exponent notation: "6*10^14" (NEVER "6e14")
    - Use single-letter variable names only (e.g., x, y, n, n1, n_1)
    - Use named physical constants without substitution (e.g., "speed of light")
    - Include spaces in compound units (e.g., "Ω m" for ohm*meter)
    - For equations with units, consider solving without units first

    OUTPUT HANDLING:
    - Results may include image URLs - display with Markdown: ![URL]
    - Mathematical formulas use proper Markdown formatting
    - Never mention knowledge cutoff dates (Wolfram may have recent data)
    - If results seem irrelevant, the API may suggest alternative assumptions

    TROUBLESHOOTING:
    - Invalid queries return suggestions for corrections
    - Authentication errors indicate App ID issues
    - Status 501 means query couldn't be interpreted (may include suggestions)

    Args:
        query: Natural language query in English (mathematical, scientific, factual)
        maxchars: Maximum response characters (default: 6800, can be reduced for shorter answers)
        units: Unit system preference ("metric", "imperial", etc.)
        location: Geographic context for location-dependent queries

    Returns:
        WolframResult object with structured response data including 'success' boolean and either 'result' (string) or 'error' details

    Examples:
        query_wolfram("derivative of x^2")
        query_wolfram("population of Tokyo", maxchars=1000)
        query_wolfram("speed of light in km/s")
        query_wolfram("solve x^2 + 3x + 2 = 0")
        query_wolfram("weather in Paris", location="Paris, France")
        query_wolfram("10 largest countries by area")
    """
    try:
        app_id = get_app_id()

        # Build parameters
        params = {"input": query, "appid": app_id}

        if maxchars is not None:
            params["maxchars"] = str(maxchars)
        if units:
            params["units"] = units
        if location:
            params["location"] = location

        # Make the API request
        response = requests.get(WOLFRAM_BASE_URL, params=params, timeout=30)

        # Handle different HTTP status codes
        if response.status_code == 200:
            return WolframResult(
                success=True,
                query=query,
                result=response.text,
                characters=len(response.text),
            )
        elif response.status_code == 501:
            return WolframResult(
                success=False,
                error="Input could not be interpreted",
                status_code=501,
                query=query,
                suggestion=response.text if response.text else None,
            )
        elif response.status_code == 400:
            return WolframResult(
                success=False,
                error="Bad request - missing or invalid input parameter",
                status_code=400,
                query=query,
            )
        elif response.status_code in [401, 403]:
            error_text = response.text.lower()
            if "invalid appid" in error_text:
                error_msg = "Invalid App ID"
            elif "appid missing" in error_text:
                error_msg = "App ID missing"
            else:
                error_msg = "Authentication error"

            return WolframResult(
                success=False,
                error=error_msg,
                status_code=response.status_code,
                query=query,
            )
        else:
            return WolframResult(
                success=False,
                error=f"Unexpected status code: {response.status_code}",
                status_code=response.status_code,
                query=query,
                response_text=response.text,
            )

    except requests.exceptions.Timeout:
        return WolframResult(
            success=False, error="Request timed out after 30 seconds", query=query
        )
    except requests.exceptions.RequestException as e:
        return WolframResult(
            success=False, error=f"Network error: {str(e)}", query=query
        )
    except ValueError as e:
        return WolframResult(success=False, error=str(e), query=query)
    except Exception as e:
        return WolframResult(
            success=False, error=f"Unexpected error: {str(e)}", query=query
        )


@mcp.prompt()
def unit_conversion(
    value: float, from_unit: str, to_unit: str, precision: int | None = None
) -> str:
    """
    Generate a prompt for unit conversion using Wolfram|Alpha.

    This prompt will instruct the user to use the query_wolfram tool to perform
    accurate unit conversions.

    Args:
        value: The numerical value to convert
        from_unit: The source unit (e.g., "meter", "pound", "celsius")
        to_unit: The target unit (e.g., "foot", "kilogram", "fahrenheit")
        precision: Optional number of decimal places for the result

    Returns:
        A formatted prompt string for unit conversion
    """
    prompt = f"""Please perform a unit conversion:

Value: {value}
From unit: {from_unit}
To unit: {to_unit}"""

    if precision is not None:
        prompt += f"\nPrecision: {precision} decimal places"

    prompt += f"""

Use the `query_wolfram` tool to perform this conversion by searching for:
"{value} {from_unit} to {to_unit}"

Please format the result as:
- Conversion result: [value] [unit]
- Calculation details: [if provided by Wolfram|Alpha]

Example usage:
query_wolfram("{value} {from_unit} to {to_unit}")"""

    return prompt


@mcp.completion()
async def handle_completion(ref, argument, context):
    """
    Handle completions for unit conversion prompts.

    Args:
        ref: PromptReference or ResourceTemplateReference
        argument: CompletionArgument with name and partial value
        context: Optional CompletionContext with previously resolved arguments

    Returns:
        Completion object with values list and hasMore flag
    """
    from mcp.types import Completion

    # Handle unit_conversion prompt completions
    # Three completion patterns:
    # 1. No context → return all units (769 units across 40 categories)
    # 2. Valid context → return units from same physical quantity category only
    # 3. Invalid context → return empty result (unit not found in any category)
    if hasattr(ref, "name") and ref.name == "unit_conversion":
        if argument.name in ["from_unit", "to_unit"]:
            query = argument.value.lower().strip() if argument.value else ""

            # Determine target units based on context
            target_units = []
            context_provided = False

            # Pattern 2 & 3: Check if context contains the other unit argument
            if context and hasattr(context, "arguments"):
                other_arg_name = (
                    "to_unit" if argument.name == "from_unit" else "from_unit"
                )
                other_unit = None

                for arg in context.arguments:
                    if arg.name == other_arg_name and arg.value:
                        other_unit = arg.value.strip()
                        context_provided = True
                        break

                if other_unit:
                    # Find which physical quantity category the other unit belongs to
                    target_category = None
                    for category, units in UNIT_CATEGORIES.items():
                        if other_unit in units:
                            target_category = category
                            break

                    if target_category:
                        # Pattern 2: Valid context - restrict to same category
                        # e.g., from_unit="foot" (length) → to_unit suggestions limited to length units
                        target_units = UNIT_CATEGORIES[target_category]
                    else:
                        # Pattern 3: Invalid context - return empty to avoid confusion
                        # e.g., from_unit="invalid_xyz" → no suggestions for to_unit
                        return Completion(values=[], hasMore=False)

            # Pattern 1: No context provided - offer all available units
            if not context_provided:
                for category_units in UNIT_CATEGORIES.values():
                    target_units.extend(category_units)

            # Handle empty query
            if not query:
                sorted_units = sorted(target_units)
                return Completion(
                    values=sorted_units[:20], hasMore=len(sorted_units) > 20
                )

            # Filter units that contain the query string
            matching_units = [unit for unit in target_units if query in unit.lower()]

            # Sort by relevance (exact matches first, then starts with, then contains)
            exact_matches = [unit for unit in matching_units if unit.lower() == query]
            starts_with = [
                unit
                for unit in matching_units
                if unit.lower().startswith(query) and unit.lower() != query
            ]
            contains = [
                unit
                for unit in matching_units
                if query in unit.lower() and not unit.lower().startswith(query)
            ]
            result = exact_matches + sorted(starts_with) + sorted(contains)
            return Completion(
                values=result[:20],  # Limit to 20 results
                hasMore=len(result) > 20,
            )

    return None


def main():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
