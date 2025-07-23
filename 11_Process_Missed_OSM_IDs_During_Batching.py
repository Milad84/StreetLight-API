import os
import sys
import json

# --------- Set working directory to script location ---------
target_dir = r"G:\ATD\ACTIVE TRANS\Vision Zero\GIS\StreetLight"
os.chdir(target_dir)
print("Changed working directory to:", os.getcwd(), flush=True)
print("Files in directory:", os.listdir(target_dir), flush=True)

# Make sure the directory is in sys.path
if target_dir not in sys.path:
    sys.path.append(target_dir)
    print(f"Added {target_dir} to sys.path", flush=True)

# --------- Try to import the OSM id list ----------
try:
    from OSM_id_list_AFP import osm_id_list
    print("Imported OSM IDs. Example:", osm_id_list[:5], flush=True)
except Exception as e:
    print("Failed to import osm_id_list:", e, flush=True)
    sys.exit(1)

batch_size = 500

# Load the failed batches log
with open("failed_batches_log.json") as f:
    failed_batches = json.load(f)

# Get all failed batch indices (1-based index in your log)
failed_indices = [batch['batch'] for batch in failed_batches]

# For each failed batch, recover the corresponding OSM IDs
failed_osm_ids = []
for idx in failed_indices:
    start = (idx - 1) * batch_size
    end = start + batch_size
    failed_osm_ids.extend(osm_id_list[start:end])

print(f"Number of failed OSM IDs: {len(failed_osm_ids)}", flush=True)
# Save for re-submission
with open("osm_ids_failed_batches.json", "w") as f:
    json.dump(failed_osm_ids, f)
print("Failed OSM IDs saved to osm_ids_failed_batches.json", flush=True)
