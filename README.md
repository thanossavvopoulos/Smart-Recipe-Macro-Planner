# Smart Recipe - Macro Planner
📖 About

Smart Recipe & Macro Planner is an interactive command-line application built in Python.

Meal prepping usually means juggling three separate chores: choosing recipes, checking whether they fit your nutrition goals, and writing a shopping list. This tool combines them. Pick meals for any day of the week, scale the servings, see calories and macronutrients instantly, and export one consolidated grocery list grouped by store aisle.

✨ Features
-🍽️ Recipe catalogue with 9 built-in recipes and per-serving calories, protein, carbs and fat
-🗓️ Weekly meal planner: assign any recipe to any day, as many times as you like
-⚖️ Flexible serving sizes: whole or fractional servings (1.5), scaled automatically from the recipe's base yield
-📊 Macro tracking per meal, per day, and for the whole plan, including each day's calorie split (% from protein, carbs and fat)
-🛒 Smart grocery list that merges identical ingredients across all planned meals and groups them by category (Produce, Meat & Fish, Pantry, ...)
-💾 Export to .txt as a ready-to-use shopping checklist
-🧰 Forgiving input: pick recipes by number, full name or partial name; pick days by number, Mon or Monday; leave any prompt blank to cancel
-✅ Validated data: the program checks at startup that every recipe only uses known ingredients

🚀 Getting Started
Prerequisites
Python 3.9 or newer
pip
Installation
bash
# 1. Clone the repository
git clone https://github.com/thanossavvopoulos/smart-recipe-macro-planner.git
cd smart-recipe-macro-planner

# 2. (Optional) create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
Run
bash
python project.py
Run the tests
bash
pytest
🕹️ Usage

The program opens a numbered menu:

text
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

Option	What it does
1	Lists every recipe with its base yield and macros per serving
2	Adds a meal: choose a recipe (number or name), the number of servings, and a day
3	Shows each planned meal, daily totals, each day's calorie split, and the weekly split
4	Shows the merged grocery list, grouped by category
5	Saves the grocery list as a text checklist (.txt is appended automatically)
6	Removes a meal using its number from the plan table
7	Clears the whole plan after confirmation
0	Exits

Tips

Press Enter on a blank line at any prompt to cancel.
Recipes accept 5, chicken rice & broccoli, or just salmon (if the match is unique).
Days accept 1-7, mon, or Monday.
Servings can be fractional, from just above 0 up to 20.

🧠 Design Decisions
Data model

Every quantity in the program is stored in grams, and every nutrition value is stored per 100 g. This reduces all nutrition math to one formula:

nutrients = macros_per_100g × grams / 100

There are no unit conversions (cups, tablespoons, "1 egg"), which keeps the calculations simple, predictable and easy to test.

Type	Role
Macros	Immutable dataclass: calories, protein, carbs, fat. Supports + and .scaled(factor)
Food	A shopping category plus Macros per 100 g
Recipe	name, base_servings, and ingredients (ingredient name → grams for the base yield)
PlanEntry	One planned meal: day, recipe_name, servings

FOODS (ingredient database) and RECIPES (recipe catalogue) are plain dictionaries. Recipes refer to foods by name, so each food's nutrition data is defined in exactly one place. validate_data() checks this link at startup and refuses to run if a recipe uses an unknown ingredient.

Pure functions vs. I/O

The code separates logic from user interaction:

Pure functions take arguments and return values, with no print() or input(). They are trivial to unit test.
I/O functions (add_meal, view_plan, prompt_value, ...) handle prompts and tables, and call the pure functions to do the real work.
main() only validates the data and runs the menu loop.

The core pure functions:

python
scale_recipe(recipe, servings)            # recipe + servings   -> {ingredient: grams}
calculate_macros(ingredients, foods)      # {ingredient: grams} -> Macros
build_grocery_list(plan, recipes)         # meal plan           -> {ingredient: total grams}

Supporting pure helpers: parse_servings, parse_days, find_recipe, validate_data, plan_macros_by_day, calorie_split, format_grams, group_by_category, format_grocery_text.

Other choices
Frozen dataclasses make data objects immutable, which prevents accidental changes to shared recipe or food data.
Dispatch dictionary in main() maps menu choices to actions, which is cleaner than a long if/elif chain.
Calorie split uses the standard 4 / 4 / 9 kcal per gram for protein / carbs / fat.
Type hints everywhere, following PEP 8.

📁 Project Structure
text
.
├── project.py          # Application: data model, core logic, CLI
├── test_project.py     # pytest unit tests for the pure functions
├── requirements.txt    # Dependencies (tabulate, pytest)
└── README.md

🛠️ Built With
Python: standard library only (dataclasses, typing, math)
tabulate: formatted terminal tables
pytest: unit testing

⚠️ Notes & Limitations
Nutrition values are approximate (USDA-style figures) and refer to raw / dry weight as purchased. This tool is a planning aid, not medical or dietary advice.
The meal plan lives in memory and is not saved between sessions. Only the grocery list can be exported.
The recipe and food databases are built into project.py.

👤 Author
Athanasios Savvopoulos
Github name: thanossavvopoulos
