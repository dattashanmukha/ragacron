import json

# 1. Load the scraped bhajans and the translated scales
with open('bhajan_database.json', 'r', encoding='utf-8') as f:
    bhajans = json.load(f)

with open('clean_ragas.json', 'r', encoding='utf-8') as f:
    ragas_db = json.load(f)

ready_for_mongo = []
needs_manual_fixing = []

for bhajan in bhajans:
    if "Ragam" not in bhajan:
        continue
        
    raga_name = bhajan["Ragam"].lower().strip()
    
    if raga_name in ragas_db:
        bhajan["Ascending (Hindustani)"] = ragas_db[raga_name]["ascending"]
        bhajan["Descending (Hindustani)"] = ragas_db[raga_name]["descending"]
        ready_for_mongo.append(bhajan)
    else:
        needs_manual_fixing.append(bhajan)

# Save the perfect matches for the app
with open('ready_for_mongo.json', 'w', encoding='utf-8') as f:
    json.dump(ready_for_mongo, f, indent=4)

# Save the failures for later
with open('fix_later.json', 'w', encoding='utf-8') as f:
    json.dump(needs_manual_fixing, f, indent=4)

print(f"Perfect matches ready for database: {len(ready_for_mongo)}")
print(f"Bhajans set aside: {len(needs_manual_fixing)}")