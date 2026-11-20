import pytest

from project import (
    FOODS,
    RECIPES,
    Food,
    Macros,
    PlanEntry,
    Recipe,
    build_grocery_list,
    calculate_macros,
    calorie_split,
    find_recipe,
    format_grams,
    group_by_category,
    parse_days,
    parse_servings,
    scale_recipe,
    validate_data,
)


def test_scale_recipe():
    recipe = Recipe(
        name="Test Pasta",
        base_servings=2,
        ingredients={"pasta": 200.0, "tomato sauce": 100.0},
    )

    assert scale_recipe(recipe, 4) == {"pasta": 400.0, "tomato sauce": 200.0}
    assert scale_recipe(recipe, 1) == {"pasta": 100.0, "tomato sauce": 50.0}
    assert scale_recipe(recipe, 1.5) == {"pasta": 150.0, "tomato sauce": 75.0}

    with pytest.raises(ValueError):
        scale_recipe(recipe, 0)
    with pytest.raises(ValueError):
        scale_recipe(recipe, -1.5)


def test_calculate_macros():
    foods = {
        "chicken": Food("Meat", Macros(calories=120.0, protein=20.0, carbs=0.0, fat=2.0)),
        "rice": Food("Grains", Macros(calories=130.0, protein=2.0, carbs=28.0, fat=0.5)),
    }

    result = calculate_macros({"chicken": 200.0, "rice": 100.0}, foods)
    assert result.calories == pytest.approx(370.0)
    assert result.protein == pytest.approx(42.0)
    assert result.carbs == pytest.approx(28.0)
    assert result.fat == pytest.approx(4.5)

    assert calculate_macros({}, foods) == Macros(0.0, 0.0, 0.0, 0.0)

    with pytest.raises(ValueError):
        calculate_macros({"chicken": -10.0}, foods)
    with pytest.raises(ValueError):
        calculate_macros({"chocolate": 50.0}, foods)


def test_build_grocery_list():
    recipes = {
        "Chicken Rice": Recipe("Chicken Rice", 1, {"chicken": 200.0, "rice": 100.0}),
        "Chicken Salad": Recipe("Chicken Salad", 2, {"chicken": 300.0, "spinach": 100.0}),
    }
    plan = [
        PlanEntry("Monday", "Chicken Rice", 2),    # 400g chicken, 200g rice
        PlanEntry("Tuesday", "Chicken Salad", 1),  # 150g chicken, 50g spinach
    ]

    grocery = build_grocery_list(plan, recipes)
    assert grocery == {"chicken": 550.0, "rice": 200.0, "spinach": 50.0}
    assert list(grocery.keys()) == ["chicken", "rice", "spinach"]

    assert build_grocery_list([], recipes) == {}

    with pytest.raises(ValueError):
        build_grocery_list([PlanEntry("Monday", "Nonexistent", 1)], recipes)


def test_builtin_data():
    assert validate_data(RECIPES, FOODS) == []


def test_parsers():
    # parse_days
    assert parse_days("1") == "Monday"
    assert parse_days("tue") == "Tuesday"
    assert parse_days("  FRIDAY ") == "Friday"
    with pytest.raises(ValueError):
        parse_days("8")
    with pytest.raises(ValueError):
        parse_days("Τunday")

    # parse_servings
    assert parse_servings("2.5") == 2.5
    with pytest.raises(ValueError):
        parse_servings("0")
    with pytest.raises(ValueError):
        parse_servings("25")
    with pytest.raises(ValueError):
        parse_servings("abc")

    # find_recipe
    sample_recipes = {
        "Spinach Scramble on Toast": Recipe("Spinach Scramble on Toast", 1, {"eggs": 100}),
        "Avocado Egg Toast": Recipe("Avocado Egg Toast", 1, {"eggs": 100}),
        "Baked Salmon & Sweet Potato": Recipe("Baked Salmon & Sweet Potato", 2, {"salmon": 300}),
    }
    assert find_recipe("3", sample_recipes) == "Baked Salmon & Sweet Potato"
    assert find_recipe("salmon", sample_recipes) == "Baked Salmon & Sweet Potato"
    with pytest.raises(ValueError):
        find_recipe("toast", sample_recipes)
    with pytest.raises(ValueError):
        find_recipe("pizza", sample_recipes)


def test_stats_and_formatting():
    # 4-4-9: 25g protein (100 kcal), 25g carbs (100 kcal), 22.22g fat (200 kcal)
    split_text = calorie_split(Macros(calories=400, protein=25, carbs=25, fat=200 / 9))
    assert split_text == "25% protein, 25% carbs, 50% fat"
    assert calorie_split(Macros()) == "0% protein, 0% carbs, 0% fat"

    # format_grams
    assert format_grams(450.4) == "450 g"
    assert format_grams(1250) == "1.25 kg"

    # group_by_category
    foods = {
        "banana": Food("Produce", Macros()),
        "chicken": Food("Meat & Fish", Macros()),
        "eggs": Food("Dairy & Eggs", Macros()),
    }
    grouped = group_by_category({"chicken": 300, "banana": 150, "eggs": 100}, foods)
    assert list(grouped.keys()) == ["Dairy & Eggs", "Meat & Fish", "Produce"]

    with pytest.raises(ValueError):
        group_by_category({"salt": 5}, foods)