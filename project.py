"""Smart Recipe & Macro Planner: CS50P Final Project."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple, Mapping, Sequence, TypeVar
import math
from tabulate import tabulate

T = TypeVar("T")

DAYS: Tuple[str, ...] = (
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
)

MAX_SERVINGS: float = 20.0

TABLE_FORMAT : str = "rounded_outline"




@dataclass(frozen=True)
class Macros:
    calories: float = 0.0
    protein: float = 0.0
    carbs: float = 0.0
    fat: float = 0.0

    def __add__(self, other: Macros) -> Macros:
        return Macros(
            self.calories + other.calories,
            self.protein + other.protein,
            self.carbs + other.carbs,
            self.fat + other.fat
        )

    def scaled(self, factor: float) -> Macros:
        return Macros(
            self.calories * factor,
            self.protein * factor,
            self.carbs * factor,
            self.fat * factor
        )

@dataclass(frozen=True)
class Food:
    """A food item with its shopping category and macronutrients per 100 g."""
    category: str
    per_100g: Macros

@dataclass(frozen=True)
class Recipe:
    """A recipe with its base servings and ingredient grams."""
    name: str
    base_servings: float
    ingredients: dict[str, float]  # ingredient name -> grams

def scale_recipe(recipe: Recipe, servings: float) -> dict[str, float]:
    if servings <= 0:
        raise ValueError("Number of servings must be greater than zero.")

    scale_factor = servings / recipe.base_servings
    return {ingredient: grams * scale_factor for ingredient, grams in recipe.ingredients.items()}

def calculate_macros(ingredients: dict[str, float], foods: dict[str, Food]) -> Macros:
    total = Macros()
    for name, grams in ingredients.items():
        if grams < 0:
            raise ValueError(f"Negative weight for {name!r}.")
        if name not in foods:
            raise ValueError(f"Unknown ingredient: {name!r}.")
        total += foods[name].per_100g.scaled(grams / 100)
    return total  

FOODS: dict[str, Food] = {
    "chicken breast": Food("Meat & Fish", Macros(120, 22.5, 0.0, 2.6)),
    "lean ground beef": Food("Meat & Fish", Macros(152, 21.0, 0.0, 7.0)),
    "salmon fillet": Food("Meat & Fish", Macros(208, 20.0, 0.0, 13.0)),
    "tofu (firm)": Food("Meat & Fish", Macros(144, 17.0, 2.8, 8.7)),
    "eggs": Food("Dairy & Eggs", Macros(143, 12.6, 0.7, 9.5)),
    "milk (whole)": Food("Dairy & Eggs", Macros(61, 3.2, 4.8, 3.3)),
    "greek yogurt": Food("Dairy & Eggs", Macros(73, 10.0, 3.9, 1.9)),
    "parmesan": Food("Dairy & Eggs", Macros(431, 38.0, 4.1, 29.0)),
    "white rice": Food("Grains & Pasta", Macros(365, 7.1, 80.0, 0.7)),
    "rolled oats": Food("Grains & Pasta", Macros(389, 16.9, 66.3, 6.9)),
    "pasta": Food("Grains & Pasta", Macros(371, 13.0, 74.7, 1.5)),
    "quinoa": Food("Grains & Pasta", Macros(368, 14.1, 64.2, 6.1)),
    "whole wheat bread": Food("Grains & Pasta", Macros(247, 13.0, 41.0, 3.4)),
    "red lentils": Food("Pantry", Macros(352, 24.6, 63.0, 1.1)),
    "tomato sauce": Food("Pantry", Macros(29, 1.3, 5.8, 0.3)),
    "olive oil": Food("Pantry", Macros(884, 0.0, 0.0, 100.0)),
    "peanut butter": Food("Pantry", Macros(588, 25.0, 20.0, 50.0)),
    "broccoli": Food("Produce", Macros(34, 2.8, 6.6, 0.4)),
    "spinach": Food("Produce", Macros(23, 2.9, 3.6, 0.4)),
    "sweet potato": Food("Produce", Macros(86, 1.6, 20.1, 0.1)),
    "onion": Food("Produce", Macros(40, 1.1, 9.3, 0.1)),
    "bell pepper": Food("Produce", Macros(31, 1.0, 6.0, 0.3)),
    "banana": Food("Produce", Macros(89, 1.1, 22.8, 0.3)),
    "blueberries": Food("Produce", Macros(57, 0.7, 14.5, 0.3)),
    "avocado": Food("Produce", Macros(160, 2.0, 8.5, 14.7)),
}


RECIPES: dict[str, Recipe] = {
    r.name: r
    for r in (
        Recipe(
            "Peanut Butter Overnight Oats",
            1,
            {"rolled oats": 50, "milk (whole)": 150, "banana": 100,
             "peanut butter": 15},
        ),
        Recipe(
            "Spinach Scramble on Toast",
            1,
            {"eggs": 150, "spinach": 40, "whole wheat bread": 70,
             "olive oil": 5},
        ),
        Recipe(
            "Berry Yogurt Bowl",
            1,
            {"greek yogurt": 200, "blueberries": 80, "rolled oats": 30},
        ),
        Recipe(
            "Avocado Egg Toast",
            1,
            {"whole wheat bread": 70, "avocado": 100, "eggs": 100},
        ),
        Recipe(
            "Chicken, Rice & Broccoli",
            4,
            {"chicken breast": 600, "white rice": 240, "broccoli": 400,
             "olive oil": 20},
        ),
        Recipe(
            "Baked Salmon & Sweet Potato",
            2,
            {"salmon fillet": 300, "sweet potato": 400, "broccoli": 200,
             "olive oil": 10},
        ),
        Recipe(
            "Beef Bolognese Pasta",
            4,
            {"lean ground beef": 500, "pasta": 320, "tomato sauce": 400,
             "onion": 150, "parmesan": 30},
        ),
        Recipe(
            "Lentil Spinach Stew",
            4,
            {"red lentils": 300, "spinach": 200, "onion": 200,
             "tomato sauce": 200, "olive oil": 20},
        ),
        Recipe(
            "Tofu Quinoa Stir-Fry",
            2,
            {"tofu (firm)": 300, "quinoa": 120, "bell pepper": 200,
             "broccoli": 150, "olive oil": 15},
        ),
    )
}

@dataclass(frozen = True)
class PlanEntry:
    """A planned meal entry with day, recipe name, and number of servings."""
    day: str
    recipe_name: str
    servings: float


def build_grocery_list(plan: Sequence[PlanEntry], recipes: Mapping[str, Recipe]) -> Dict[str, float]:

    totals: Dict[str, float] = {}
    for entry in plan:
        if entry.recipe_name not in recipes:
            raise ValueError(f"Unknown recipe: {entry.recipe_name!r}.")
        recipe = recipes[entry.recipe_name]
        scaled_ingredients = scale_recipe(recipe, entry.servings)
        for ingredient, grams in scaled_ingredients.items():
            totals[ingredient] = totals.get(ingredient, 0) + grams
    return totals

def parse_servings(servings_str: str) -> float:
    """Converts a string to a valid float representing the number of servings."""
    try:
        value = float(servings_str.strip())
    except ValueError:
        raise ValueError("Please enter a number, e.g. 2 or 1.5.") from None
    if not math.isfinite(value) or not (0 < value <= MAX_SERVINGS):
        raise ValueError(f"Servings must be between 0 and {MAX_SERVINGS:g}.")
    return value

def parse_days(days_str: str) -> str:
    """Converts a string to a valid day of the week."""
    key = days_str.strip().lower()
    if key.isdigit() and 1 <= int(key) <= len(DAYS):
        return DAYS[int(key) - 1]

    for day in DAYS:
        if key in (day.lower(), day[:3].lower()):
            return day

    raise ValueError(f"Please enter a valid day of the week (1-7 MON-SUN).")

def find_recipe(query: str, recipes: Mapping[str, Recipe]) -> str:
    """Finds a recipe by name or partial name, returning the full recipe name."""
    q = query.strip().lower()
    names = list(recipes.keys())
    
    if q.isdigit():
        index = int(q)
        if 1 <= index <= len(names):
            return names[index - 1]
        raise ValueError(f"Choose a number between 1 and {len(names)}.")

    # Check for exact matches first
    for name in names:
        if name.lower() == q:
            return name

    # Check for partial matches
    matches = [name for name in names if q in name.lower()]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise ValueError("Matching multiple recipes. Please be more specific.")

    raise ValueError(f"No recipe found matching {query!r}.")

def validate_data(recipes: Mapping[str, Recipe], foods: Mapping[str, Food]) -> list[str]:
    """Returns a list of errors if any recipes contain ingredients not in FOODS."""
    errors : list[str] = []
    for recipe in recipes.values():
        if recipe.base_servings <= 0:
            errors.append(f"Recipe must have a positive number of base servings: {recipe.name!r}.")
        for ingredient in recipe.ingredients:
            if ingredient not in foods:
                errors.append(f"Recipe contains unknown ingredient: {ingredient!r}.")
    return errors

def plan_macros_by_day(plan: Sequence[PlanEntry], recipes: Mapping[str, Recipe], foods: Mapping[str, Food]) -> Dict[str, Macros]:
    """Calculates total macros for each day in the meal plan."""
    daily_macros: dict[str, Macros] = {}

    for entry in plan:
        scaled = scale_recipe(recipes[entry.recipe_name], entry.servings)
        if entry.day not in daily_macros:
            daily_macros[entry.day] = Macros()
        daily_macros[entry.day] += calculate_macros(scaled, foods)
    return daily_macros

def calorie_split(macros: Macros) -> str:
    """Returns a string showing the percentage of calories from protein, carbs, and fat."""
    p = macros.protein * 4
    c = macros.carbs * 4
    f = macros.fat * 9
    total = p + c + f

    if total == 0:
        return "0% protein, 0% carbs, 0% fat"

    p_percent = round(p / total * 100)
    c_percent = round(c / total * 100)
    f_percent = round(f / total * 100)
    return f"{p_percent}% protein, {c_percent}% carbs, {f_percent}% fat"

def format_grams(grams: float) -> str:
    """Formats the grocery list quantities in grams or kilograms for display."""
    if grams >= 1000:
        return f"{grams / 1000:.2f} kg"
    return f"{round(grams)} g"

def group_by_category(grocery_list: Mapping[str, float], foods: Mapping[str, Food]) -> dict[str, dict[str, float]]:
    """Groups grocery list items by their shopping category (sorted)."""
    categories: dict[str, dict[str, float]] = {}
    groups: dict[str, dict[str, float]] = {}    
    for ingredient, grams in grocery_list.items():
        if ingredient not in foods:
            raise ValueError(f"Unknown ingredient: {ingredient!r}.")
        category = foods[ingredient].category
        if category not in groups:
            groups[category] = {}
        groups[category][ingredient] = grams

    for category in sorted(groups):
        categories[category] = dict(sorted(groups[category].items()))
    return categories

def format_grocery_text(grocery_list: Mapping[str, float], foods: Mapping[str, Food]) -> str:
    """Formats the grocery list as a text string, grouped by category."""
    lines = ["SHOPPING LIST", "=============", ""]
    for category, items in group_by_category(grocery_list, foods).items():
        lines.append(category.upper())
        for name, grams in items.items():
            lines.append(f"  [ ] {name.title()}: {format_grams(grams)}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"



#-----------------------------------------------------------------------------------#
# IO HELPERS AND CLI MENU
#-----------------------------------------------------------------------------------#

def prompt_value(prompt: str, parse_func: Callable[[str], T]) -> T:
    """Prompts the user for input until it is valid and parses it using the provided function."""
    while True:
        raw = input(prompt).strip()
        if not raw:
            return None
        try:
            return parse_func(raw)
        except ValueError as error:
            print(f"Error: {error}")

def save_text_file(filename: str, content: str) -> str:
    """Saves the given content to a text file with the specified filename (Secures it will be a .txt file)."""
    if not filename.lower().endswith(".txt"):
        filename += ".txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return filename

def display_macros_table(macros: Macros) -> list[str]:
    return [
        f"{macros.calories:.0f} kcal",
        f"{macros.protein:.1f} g",
        f"{macros.carbs:.1f} g",
        f"{macros.fat:.1f} g",
    ]

def show_recipes(recipes: Mapping[str, Recipe], foods: Mapping[str, Food]) -> None:
    """Displays a table of recipes with their base servings and total macros per serving."""
    rows = []
    for number, recipe in enumerate(recipes.values(), start=1):
        per_serving = calculate_macros(scale_recipe(recipe, 1), foods)
        rows.append([number, recipe.name, recipe.base_servings, * display_macros_table(per_serving)])
    headers = ["#", "Recipe", "Makes", "kcal", "Protein g", "Carbs g", "Fat g"]
    print("\nRecipes (macros per 1 serving)")
    print(tabulate(rows, headers=headers, tablefmt=TABLE_FORMAT,
                   colalign=("right", "left", "right", "right", "right", "right", "right")))

def add_meal(plan: List[PlanEntry], recipes: Mapping[str, Recipe]) -> None:
    """Prompts the user to add a meal to the plan."""
    print("\nAdd a meal to the plan")
    show_recipes(recipes, FOODS)
    recipe_name = prompt_value("Enter recipe number or name (or blank to cancel): ", lambda s: find_recipe(s, recipes))
    if recipe_name is None:
        return
    servings = prompt_value(f"Enter number of servings for {recipe_name} (or blank to cancel): ", parse_servings)
    if servings is None:
        return
    day = prompt_value("Enter day of the week (1-7 MON-SUN) (or blank to cancel): ", parse_days)
    if day is None:
        return
    plan.append(PlanEntry(day, recipe_name, servings))
    print(f"Added {day} - {recipe_name} ({servings} servings) to the plan.")

def view_plan(plan: Sequence[PlanEntry], recipes: Mapping[str, Recipe], foods: Mapping[str, Food]) -> None:
    """Displays the weekly meal plan with total macros per day and overall."""
    if not plan:
        print("\nNo meals in the plan yet.")
        return

    rows = []
    for number, entry in enumerate(plan, start=1):
        scaled = scale_recipe(recipes[entry.recipe_name], entry.servings)
        macros = calculate_macros(scaled, foods)
        rows.append([number, entry.day, entry.recipe_name, entry.servings, *display_macros_table(macros)])
    
    headers = ["#", "Day", "Recipe", "Servings", "kcal", "Protein g", "Carbs g", "Fat g"]
    print("\nMeal Plan")
    print(tabulate(rows, headers=headers, tablefmt=TABLE_FORMAT,
                   colalign=("right", "left", "left", "right", "right", "right", "right", "right")))

    daily = plan_macros_by_day(plan, recipes, foods)
    day_rows = [[day, *display_macros_table(macros), calorie_split(macros)] for day, macros in daily.items()]
    print("\nDaily Macros")
    print(tabulate(day_rows, headers=["Day", "kcal", "Protein g", "Carbs g", "Fat g", "Calorie Split"], tablefmt=TABLE_FORMAT,
                   colalign=("left", "right", "right", "right", "right", "right")))

    total_macros = sum(daily.values(), Macros())
    print(f"\nCalorie Split for the week: {calorie_split(total_macros)}")

def view_grocery_list(plan: Sequence[PlanEntry], recipes: Mapping[str, Recipe], foods: Mapping[str, Food]) -> None:
    """Displays the consolidated grocery list for the meal plan."""
    if not plan:
        print("\nNo meals in the plan yet.")
        return

    grocery_list = build_grocery_list(plan, recipes)
    grouped = group_by_category(grocery_list, foods)
    
    rows = []
    for category, items in grouped.items():
        for name, grams in items.items():
            rows.append([category, name.title(), format_grams(grams)])

    print("\nGrocery List")
    print(tabulate(rows, headers=["Category", "Ingredient", "Amount"], tablefmt=TABLE_FORMAT,
                   colalign=("left", "left", "right")))

def remove_meal(plan: List[PlanEntry]) -> None:
    """Removes a meal  based on table's index number."""
    if not plan:
        print("\n No meals to remove.")
        return

    print("\nRemove a meal from the plan")

    index = prompt_value(f"Enter meal number to remove (1-{len(plan)}) (or blank to cancel): ", lambda s: int(s.strip()))
    if index is None:
        return
    
    if not (1 <= index <= len(plan)):
        print(f"Error: Please enter a number between 1 and {len(plan)}.")
        return

    removed = plan.pop(index - 1)
    print(f"Removed {removed.day} - {removed.recipe_name} from the plan.")

def export_grocery_list(plan: Sequence[PlanEntry], recipes: Mapping[str, Recipe], foods: Mapping[str, Food]) -> None:
    """Exports the grocery list to a text file."""
    if not plan:
        print("\nPlan is empty.")
        return

    grocery_list = build_grocery_list(plan, recipes)
    text = format_grocery_text(grocery_list, foods)
    filename = input("Enter filename to save grocery list (or blank to cancel): ").strip()
    if not filename:
        print("Export canceled.")
        return
    saved_filename = save_text_file(filename, text)
    print(f"Grocery list saved to {saved_filename}.")

def clear_plan(plan: List[PlanEntry]) -> None:
    """Clears the entire meal plan after user confirmation."""
    if not plan:
        print("\nNo meals in the plan to clear.")
        return

    confirm = input("Are you sure you want to clear the entire plan? (y/n): ").strip().lower()
    if confirm == 'y' or confirm == 'yes':
        plan.clear()
        print("Meal plan cleared.")
    else:
        print("Clear plan canceled.")

MENU = """
---------------------------
Smart Recipe & Macro Planner
---------------------------
1. Browse Recipes
2. Add meal to the plan
3. View plan and macros
4. View grocery list
5. Save grocery list to file
6. Remove a meal
7. Clear the plan
0. Exit
"""

def main() -> None:
    problems = validate_data(RECIPES, FOODS)
    if problems:
        raise SystemExit("Invalid data in recipes or foods:\n" + "\n".join(problems))

    plan: List[PlanEntry] = []
    actions = {
        "1": lambda: show_recipes(RECIPES, FOODS),
        "2": lambda: add_meal(plan, RECIPES),
        "3": lambda: view_plan(plan, RECIPES, FOODS),
        "4": lambda: view_grocery_list(plan, RECIPES, FOODS),
        "5": lambda: export_grocery_list(plan, RECIPES, FOODS),
        "6": lambda: remove_meal(plan),
        "7": lambda: clear_plan(plan),
    }

    while True:
        print(MENU)
        try:
            choice = input("Choose an option (0-7): ").strip()
            if choice == "0":
                break 

            action = actions.get(choice)
            if action is None:
                print("Invalid choice. Please enter a number between 0 and 7.")
                continue
            action()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break
    print("Enjoy your meals! Goodbye.")

if __name__ == "__main__":
    main()