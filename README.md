
# SageCNC FullBot v4.1 – /vectorize presets: colorful & bare

**/vectorize** now supports presets:
- `colorful` (default): keeps per-shape color **layers** and **true-color** on entities, gentle simplify, arc-fit on.
- `bare`: minimal editing later — stronger simplify, removes tiny bits, single layer, no arcs.
- `custom`: you control all parameters.

Examples:
- `/vectorize preset:colorful target_width_mm:600`
- `/vectorize preset:bare target_width_mm:600`
- `/vectorize preset:custom threshold:190 simplify:3.0 min_feature:200 arc_fit:true arc_tol:1.0 keep_color:true`

Still included:
- `/cutlist` → labels.pdf + cutlist.csv + preview + ZIP
- `/export prefix` → zip outputs in /tmp

Deploy:
```
pip install -r requirements.txt
cp .env.example .env  # add your token
python main.py
```
On Railway: set `DISCORD_TOKEN` in Variables and deploy.
