import requests

# Fetch API Data for link
def get_battle_armor_data():
    response = requests.get("https://pokeapi.co/api/v2/ability/battle-armor")
    # Ensure the request was successful
    response.raise_for_status()
    return response.json()

# Verify Response in JSON
def verify_json_object(data):
    return isinstance(data, dict)

# a. The key effect_changes is an empty array
def test_effect_changes_empty(data):
    return data.get('effect_changes') == []

# b. The key flavour_text_entries has at least one entry in the fr (French) language
def test_flavor_text_entries_has_french(data):
    entries = data.get('flavor_text_entries', [])
    french_entries = [entry for entry in entries if entry['language']['name'] == 'fr']
    return len(french_entries) > 0

# c. If the Kabuto Pokémon has the battle-armor ability
def test_kabuto_has_battle_armor():
    kabuto_response = requests.get("https://pokeapi.co/api/v2/pokemon/kabuto")
    # Ensure the request was successful
    kabuto_response.raise_for_status()
    kabuto_data = kabuto_response.json()
    abilities = [ability['ability']['name'] for ability in kabuto_data['abilities']]
    return 'battle-armor' in abilities

# d. If the Jigglypuff Pokémon has the battle-armor ability
def test_jigglypuff_has_battle_armor():
    jigglypuff_response = requests.get("https://pokeapi.co/api/v2/pokemon/jigglypuff")
    # Ensure the request was successful
    jigglypuff_response.raise_for_status()
    jigglypuff_data = jigglypuff_response.json()
    abilities = [ability['ability']['name'] for ability in jigglypuff_data['abilities']]
    return 'battle-armor' not in abilities

# Main function
def main():
    data = get_battle_armor_data()
    if not verify_json_object(data):
        print("The response is not a valid JSON object.")
        return

    # Check results
    result_a = test_effect_changes_empty(data)
    result_b = test_flavor_text_entries_has_french(data)
    result_c = test_kabuto_has_battle_armor()
    result_d = test_jigglypuff_has_battle_armor()

    # Print outcomes
    print(f"a. The key effect_changes is an empty array: {result_a}")
    print(f"b. The key flavour text entries has at least one entry in the fr (French) language: {result_b}")
    print(f"c. If the Kabuto Pokémon has the battle-armor ability: {result_c}")
    print(f"d. If the Jigglypuff Pokémon has the battle-armor ability: {result_d}")

if __name__ == "__main__":
    main()
