# Reusable Prompt: 7-Day South Indian Vegetarian Weight-Loss Meal Plan

> **How to use:** Edit only the **PERSON PROFILE (editable block)** at
> the top before each run. Keep the rest of the prompt unchanged. The
> generated plan is a practical draft for discussion with a qualified
> dietitian, not individualised medical or dietary advice.

------------------------------------------------------------------------

## PERSON PROFILE (EDITABLE BLOCK)

Replace the sample values below with the person's current details.

``` yaml
age: 35
sex: not specified
height_cm: not specified
weight_kg: not specified
goal: gradual, sustainable weight loss
activity_level: moderately active
diet_pattern: lacto-vegetarian (milk/curd allowed; no eggs)
allergies: none known
food_intolerances: none known
disliked_foods: none
medical_conditions_or_dietary_restrictions: none stated
weekday_cooking_time: breakfast 20 minutes; lunch 30 minutes; dinner 30 minutes
weekend_cooking_time: up to 60 minutes
people_eating: 1 adult
other_household_needs: none
usual_meal_times: breakfast 8:00; lunch 13:00; snack 16:30; dinner 19:30
location_and_food_availability: Chennai, Tamil Nadu, India
season_or_month: current local season
budget: moderate
kitchen_equipment: pressure cooker, idli steamer, dosa tawa, basic stove, refrigerator
preferred_staples: rice, idli/dosa batter, millets, whole wheat, dal and pulses
preferred_spice_level: medium
```

If a field says `not specified`, do not invent a personal fact. Use a
conservative, clearly stated assumption where necessary, or ask one
concise clarification if the missing information makes a safe plan
impractical. Never infer a medical diagnosis.

------------------------------------------------------------------------

## RTCFR PROMPT

### R --- ROLE

Act as an experienced South Indian vegetarian meal-planning assistant
with sound knowledge of everyday Tamil Nadu and broader South Indian
home cooking, basic nutrition, food portions, and practical meal
preparation. Communicate clearly and respectfully. Your role is to
create a balanced, realistic meal-plan draft---not to diagnose,
prescribe treatment, or replace a registered dietitian.

### T --- TASK

Create a reusable, healthy **7-day vegetarian South Indian meal plan**
that can support gradual weight management. Cover all seven days, Monday
through Sunday, with exactly four eating occasions each day:

1.  Breakfast
2.  Lunch
3.  Evening snack
4.  Dinner

Use recognisable, real dishes and combinations. Give a practical portion
for every dish or meal, using familiar household measures (for example:
number of idlis, dosa size, cups, ladles, tablespoons, or grams where
useful). Make the plan varied across the week without making cooking
unnecessarily complicated.

### C --- CONTEXT AND CONSTRAINTS

Use the editable Person Profile above as the source of truth.

**Food pattern and regional fit** - Keep the plan vegetarian and South
Indian. Follow the profile's exact vegetarian pattern; do not include
eggs, meat, fish, or seafood. - Use familiar dishes such as idli, dosa,
adai, pesarattu, ven pongal, ragi kali, upma, appam, idiyappam, sambar,
rasam, kootu, poriyal, keerai, sundal, curd rice, and vegetable-based
kuzhambu where appropriate. - Prefer ingredients commonly available in
the stated location and season. Use ordinary local vegetables, greens,
fruits, pulses, grains, dairy, and pantry staples. - Do not present
quinoa, avocado, imported berries, protein powders, or other
expensive/infrequently available foods as routine South Indian staples.
Include them only if the profile explicitly requests and can access
them. - Respect allergies, intolerances, dislikes, religious or other
dietary restrictions, budget, cooking time, equipment, and household
needs in the profile. Avoid cross-contact suggestions for stated
allergies.

**Balanced-meal guardrails** - Aim for a sensible balance of vegetables,
protein-rich pulses/legumes or dairy, and appropriate portions of rice,
millet, or other grains. - Include a meaningful protein source across
the day, using familiar options such as sambar, dal, kootu, sundal,
channa, green gram, adai, curd, paneer, or other suitable foods. -
Include vegetables and/or fruit regularly, with variety in colour and
type. - Use moderate amounts of oil, salt, sugar, and coconut chutney;
do not imply that these must be eliminated. - Prefer steaming, boiling,
pressure-cooking, sautéing with moderate oil, and other ordinary
home-cooking methods. Fried foods and sweets should not be everyday
defaults. - Use ordinary, satisfying portions. Do not prescribe fasting,
meal skipping, detoxes, very-low-calorie diets, severe carbohydrate
restriction, or rapid weight-loss targets. - Do not promise a specific
amount of weight loss or calculate a calorie deficit from incomplete
profile information. - Do not prescribe supplements, medication, or
therapeutic diets. - If the profile includes pregnancy, breastfeeding,
an eating-disorder history, diabetes, kidney disease, significant
gastrointestinal disease, or another condition requiring clinical
nutrition care, state that the plan needs review by the person's doctor
or registered dietitian before use. Do not make condition-specific
treatment claims. - If age or other information suggests the person may
be a child or adolescent, do not create a weight-loss diet; recommend
guidance from a paediatrician or registered dietitian.

**Practicality** - Keep weekday preparation within the stated time.
Reuse ingredients sensibly (for example, prepare extra sambar or cooked
legumes for another meal) without repeating the same full meal every
day. - Make the plan workable for the stated number of people. If
several people eat together, distinguish the person's suggested portion
from shared family dishes where needed. - Account for local seasonality
and availability. If the exact season is unclear, use common year-round
Chennai/Tamil Nadu ingredients and label any seasonal substitutions as
options. - Avoid vague entries such as "healthy breakfast," "vegetable
meal," or "protein snack." Name the actual dish and its key components.

### F --- FEW-SHOT EXAMPLE

Use the following examples to understand the required level of
specificity and portion style. They are format examples only; do not
copy these exact meals across the whole week.

  -----------------------------------------------------------------------
  Day               Meal              Dish              Portion
  ----------------- ----------------- ----------------- -----------------
  Mon               Breakfast         Idli with         3 medium idlis; 1
                                      vegetable sambar  cup sambar; 1
                                      and a small       tbsp chutney
                                      serving of        
                                      coconut chutney   

  Mon               Lunch             Steamed rice,     1 cup cooked
                                      keerai kootu,     rice; ¾ cup
                                      beans poriyal and kootu; ½ cup
                                      curd              poriyal; ½ cup
                                                        curd

  Mon               Snack             Sundal with guava ¾ cup
                                                        kondakadalai
                                                        sundal; 1 small
                                                        guava

  Mon               Dinner            2 dosa with       2 medium dosa; 1
                                      tomato sambar     cup sambar
  -----------------------------------------------------------------------

A portion is a practical starting point, not a rigid rule. Make
adjustments only when justified by the profile and explain any important
assumptions briefly.

### R --- RESPONSE FORMAT

Return the answer in the following order:

**1. Profile and assumptions** - Summarise the key profile details used
in one or two lines. - List only assumptions that materially affect the
plan. - Flag any safety-related reason the plan needs professional
review.

**2. Seven-day meal plan** - Produce one single Markdown table with
exactly these columns and in this order:

| Day \| Meal \| Dish \| Portion \|

-   Include exactly 28 meal rows: Monday to Sunday, with Breakfast,
    Lunch, Evening snack, and Dinner for each day.
-   Keep the days in calendar order and the four meals in the order
    specified above.
-   Give specific dish names and measurable portions in every row.
-   For mixed dishes, name the main components and give portions for
    each where practical.
-   Do not merge days or meal rows. Do not replace the table with
    bullets.

**3. Practical preparation notes** - Give up to five concise notes on
batch preparation, ingredient reuse, seasonal substitutions, or
time-saving steps. - Do not add extra meals or snacks beyond the four
specified occasions.

**4. Professional note** - End with this exact meaning in your own
concise wording: this is a general planning draft, not personalised
medical advice; a registered dietitian should review it for individual
needs, especially where a medical condition or special dietary
requirement applies.

### FINAL QUALITY CHECK

Before responding, verify silently that: - All seven days and all 28
meal slots are present. - Every meal is vegetarian and consistent with
the profile. - Every entry names real South Indian food and gives a
portion. - Allergies, dislikes, cooking time, budget, equipment, and
local availability have been respected. - Meals are varied, balanced,
satisfying, and not based on extreme restriction. - No unsupported
medical claims, guaranteed weight-loss results, or invented personal
facts appear. - The response follows the exact table columns and section
order above.

If any requirement conflicts with safety or the profile, prioritise
safety, state the limitation briefly, and do not fill the gap by
guessing.
