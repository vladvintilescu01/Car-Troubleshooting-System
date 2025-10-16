#inference_engine
from difflib import get_close_matches

# alternative phrases for symptoms
SYNONYMS = {
    # Engine does not start
    "engine does not start": "engine_does_not_start",
    "engine won't start": "engine_does_not_start",
    "engine won't turn on": "engine_does_not_start",
    "engine no power": "engine_does_not_start",
    "car won't start": "engine_does_not_start",
    "engine fails to start": "engine_does_not_start",
    "cannot start engine": "engine_does_not_start",

    # Car pulls to one side
    "car pulls to one side": "car_pulls_to_one_side",
    "car drifts to one side": "car_pulls_to_one_side",
    "vehicle leans to one side": "car_pulls_to_one_side",
    "steering pulls": "car_pulls_to_one_side",
    "car veers to left": "car_pulls_to_one_side",
    "car veers to right": "car_pulls_to_one_side",

    # Engine overheats
    "engine overheats": "engine_overheats",
    "engine is too hot": "engine_overheats",
    "engine temperature high": "engine_overheats",
    "car overheating": "engine_overheats",

    # Headlights dim
    "headlights dim": "headlights_dim",
    "headlights are dim": "headlights_dim",
    "lights are weak": "headlights_dim",
    "dimming headlights": "headlights_dim",

    # Strange noise from brakes
    "strange noise from brakes": "strange_noise_from_brakes",
    "brakes make noise": "strange_noise_from_brakes",
    "weird sound when braking": "strange_noise_from_brakes",
    "squeaky brakes": "strange_noise_from_brakes",
    "grinding brakes": "strange_noise_from_brakes",

    # Exhaust smoke black
    "exhaust smoke black": "exhaust_smoke_black",
    "black smoke from exhaust": "exhaust_smoke_black",
    "car emits black smoke": "exhaust_smoke_black",

    # Exhaust smoke blue
    "exhaust smoke blue": "exhaust_smoke_blue",
    "blue smoke from exhaust": "exhaust_smoke_blue",
    "car emits blue smoke": "exhaust_smoke_blue",

    # Steering wheel vibrates
    "steering wheel vibrates": "steering_wheel_vibrates",
    "steering shakes": "steering_wheel_vibrates",
    "wheel vibration": "steering_wheel_vibrates",
    "steering wobble": "steering_wheel_vibrates",

    # Air conditioner not cooling
    "air conditioner not cooling": "air_conditioner_not_cooling",
    "ac not cold": "air_conditioner_not_cooling",
    "ac not working": "air_conditioner_not_cooling",
    "air conditioning fails": "air_conditioner_not_cooling",

    # Check engine light on
    "check engine light on": "check_engine_light_on",
    "engine warning light on": "check_engine_light_on",
    "engine light on": "check_engine_light_on",
    "service engine soon": "check_engine_light_on",

    # Poor acceleration
    "poor acceleration": "poor_acceleration",
    "car accelerates slowly": "poor_acceleration",
    "slow acceleration": "poor_acceleration",
    "engine lacks power": "poor_acceleration",

    # Car not moving in gear
    "car not moving in gear": "car_not_moving_in_gear",
    "car stuck in gear": "car_not_moving_in_gear",
    "transmission problem": "car_not_moving_in_gear",
    "gear engaged but car doesn't move": "car_not_moving_in_gear",
}

#normalize input
def normalize(symptom):
    """Return the input of user normalized for conditions from knowledge base """
    all_conditions = {"engine_does_not_start", "car_pulls_to_one_side", "engine_overheats", "headlights_dim", "strange_noise_from_brakes",
                      "exhaust_smoke_black", "exhaust_smoke_blue", "steering_wheel_vibrates",
                      "air_conditioner_not_cooling", "check_engine_light_on", "poor_acceleration",
                      "car_not_moving_in_gear"} | set(SYNONYMS.keys())
    symptom = symptom.strip().lower().replace("-", "_").replace(" ", "_")

    if symptom in SYNONYMS:
        return SYNONYMS[symptom]

    symptom_matched = get_close_matches(symptom,list(all_conditions), 1)
    if symptom_matched:
        return SYNONYMS.get(symptom_matched[0],symptom_matched[0])

    return symptom

#load rules
def load_rules():
    """Return all rules known by system"""
    rules_loaded = []
    file_rules = "rules.txt"
    with open(file_rules, "r") as file:
        for each_line in file:
            if each_line.strip() and each_line.startswith("IF"):
              line_divided = each_line.split("THEN")
              condition = line_divided[0].replace("IF", "").strip()
              result = line_divided[1].replace("CHECK", "").strip()
              rules_loaded.append((condition,result))

    return rules_loaded

def forward_chain(symptom, rules, visited=None):
    """Return full chain of causes for a symptom"""
    if visited is None:
        visited = set()

    chains = []
    for condition, result in rules:
        if condition.lower() == symptom.lower() and result.lower() not in visited:
            visited.add(result.lower())
            # Recursively find next steps
            sub_chains = forward_chain(result, rules, visited.copy())
            if sub_chains:
                for sub in sub_chains:
                    chains.append(f"{result} -> {sub}")
            else:
                chains.append(result)
    return chains



def find_causes_with_chain(symptom, rules):
    """Return possible causes with inference chain integrated"""
    causes = []
    direct_causes = [result for condition, result in rules if symptom.lower() in condition.lower()]

    for cause in direct_causes:
        chain = forward_chain(cause, rules)
        if chain:
            causes.append(f"{cause} -> " + " -> ".join(chain))
        else:
            causes.append(cause)
    return causes