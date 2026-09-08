import json
import unicodedata

def remove_accents(input_str):
    # Converts special characters like 'ā' into standard 'a'
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def translate_to_hindustani(carnatic_scale):
    mapping = {
        "S": "S", "R1": "r", "R2": "R", "G1": "R", "R3": "g", 
        "G2": "g", "G3": "G", "M1": "m", "M2": "M", "P": "P", 
        "D1": "d", "D2": "D", "N1": "D", "D3": "n", "N2": "n", "N3": "N"
    }
    notes = carnatic_scale.split(" ")
    translated = [mapping.get(note, note) for note in notes]
    return " - ".join(translated)

# 1. Load the raw Kaggle dataset
with open('Janaka Ragas.json', 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

clean_raga_db = {}

# 2. Iterate through the indices (0 to 71)
for index in raw_data["Ragam"]:
    # Grab the original name and normalize it (lowercase, no accents)
    original_name = raw_data["Ragam"][index]
    clean_name = remove_accents(original_name).lower().strip()
    
    # Grab scales
    asc_carnatic = raw_data["Ascending"][index]
    desc_carnatic = raw_data["Descending"][index]
    
    # Translate to Hindustani immediately
    clean_raga_db[clean_name] = {
        "ascending": translate_to_hindustani(asc_carnatic),
        "descending": translate_to_hindustani(desc_carnatic)
    }

# 3. Save the clean, ready-to-use database
with open('clean_ragas.json', 'w', encoding='utf-8') as f:
    json.dump(clean_raga_db, f, indent=4)

print("Database cleaned and translated. Saved as clean_ragas.json")