# Evidence format / evidence 字段说明

Status: proposed serialization of the current manuscript's E fields. The included records are authored examples, not detector outputs recovered from a run. Version: `1.0.0-demo`.

| JSON path | Representation and meaning |
|---|---|
| `sample_id` | Pairing identifier; demo identifiers are `demo-001` through `demo-008`, not public-dataset image IDs |
| `provenance.kind` | `synthetic_authored` for every supplied example |
| `provenance.model_inference_run` | `false` for every supplied example |
| `image.width_px`, `image.height_px` | Positive image dimensions used to explain coordinate normalization |
| `image.original_image_path`, `heatmap.path` | Package-relative asset path when available; null in this text-only demonstration |
| `heatmap.normalized_range` | `[0,1]`; does not mean a real heatmap is supplied |
| `anomaly.decision` | `normal` or `anomalous`, as the fixed detector decision |
| `anomaly.score` | Detector anomaly score s on `[0,1]` |
| `region.mask_empty` | Whether post-processing yields no candidate component |
| `region.principal_component_id` | Identifier of the largest candidate component; null for an empty mask |
| `region.principal_centroid_normalized` | `[x,y]`, with x increasing rightward and y downward, divided by image width/height |
| `region.grid_location` | Principal component's fixed 3×3 cell; null for an empty mask |
| `region.bounding_box_normalized` | Principal component's `[xmin,ymin,xmax,ymax]` on `[0,1]`; null for an empty mask |
| `region.area_fraction` | Total retained candidate-mask pixels / total image pixels, not just the principal box or component; null for an empty mask |
| `visual_grade` | Detector-mapping appearance grade; demo vocabulary is illustrative, not a verified empirical grade mapping |
| `versions` | Evidence mapping, audit and prompt versions, plus checkpoint revision when established |

## Units and geometry

Use the same grid mapping for detector and independent annotation regions. Rows are upper/middle/lower, columns left/middle/right; the middle cell is `center`. An internal boundary belongs to its rightward or downward cell. For a normalized centroid, column is `min(floor(3*x),2)` and row is `min(floor(3*y),2)`.

The principal component is the largest connected component. Actual runs must freeze their coordinate-priority tie break. This package has one authored component per nonempty example and neither establishes nor exercises an empirical tie-break setting.

Bounding-box coordinates describe the principal component. Area describes the total candidate mask. Neither is a volume measurement. Visual grade describes mapped appearance; it does not establish functional failure severity. `0.036` area fraction equals `3.6%` image coverage.

## Empty masks and immutable evidence

For an empty mask, principal component, centroid, grid location, box and area are all JSON null. The report must explicitly state the inapplicable fields rather than substitute an invented region or a numeric area. An empty mask alone is not a proof that the public image label is normal.

E is constructed once. Each R0/R1 example references the SHA-256 of the same E JSON bytes. Real I and H must also remain unchanged in an actual reporting loop; no such visual assets are present or validated here.

The schema expresses types and empty-mask constraints. `scripts/check_materials.py` checks demo-specific provenance and domain relationships such as centroid/grid consistency. It is not a general-purpose JSON Schema engine.
