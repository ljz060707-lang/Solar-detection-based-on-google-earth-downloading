# Solar Detection Based on Google Earth Downloading

End-to-end geospatial workflow for rooftop solar panel detection using Google Earth imagery, tile normalization, building filtering, COCO dataset generation, model training, and geospatial inference.

---

# Overview

This repository provides a complete remote sensing pipeline for solar panel detection:

* Import Google Earth or WMS imagery
* Convert imagery into georeferenced tiles
* Filter roof candidate regions
* Export COCO training dataset
* Train detection model
* Run geospatial inference and evaluation

---

# Workflow

```text id="6b8w13"
Imagery Source (Google Earth / WMS)
        ↓
download_imagery.py
        ↓
GeoTIFF tiles
        ↓
building_filter.py
        ↓
Roof candidate regions
        ↓
export_coco_dataset.py
        ↓
COCO dataset
        ↓
train.py
        ↓
Detection model
        ↓
detect_and_evaluate.py
        ↓
GeoJSON + metrics
```

---

# Repository Structure

```text id="9m8j2a"
.
├── scripts/
│   └── imagery/
│       ├── download_tiles.py
│       ├── download_imagery.py
│       └── imagery_adapters.py
│
├── core/
│   └── grid_utils.py
│
├── configs/
│   └── datasets/
│       └── imagery_sources.example.yaml
│
├── data/
│   ├── annotations/
│   ├── coco/
│   └── previews/
│
├── tiles/
│
├── building_filter.py
├── export_coco_dataset.py
├── train.py
├── detect_and_evaluate.py
└── README.md
```

---

# Installation

## Clone repository

```bash id="5qk7rw"
git clone https://github.com/ljz060707-lang/Solar-detection-based-on-google-earth-downloading.git
cd Solar-detection-based-on-google-earth-downloading
```

## Install dependencies

```bash id="27zvpx"
pip install -r requirements.txt
```

Recommended environment:

* Python 3.10+
* rasterio
* geopandas
* shapely
* numpy
* opencv-python
* ultralytics

---

# Step 1 — Prepare Imagery

## Google Earth local imagery

```bash id="tt8mbd"
python scripts/imagery/download_imagery.py \
  --grid-id G1190 \
  --source google_earth_local \
  --source-dir ./google_earth_exports \
  --preview-dir ./data/previews
```

## WMS imagery

```bash id="a7jck5"
python scripts/imagery/download_imagery.py \
  --grid-id G1190 \
  --source wms
```

Output:

```text id="fd4wnk"
tiles/G1190/*.tif
```

Requirements:

* CRS must be EPSG:4326
* GeoTIFF recommended

Supported input:

* `.tif`
* `.tiff`
* `.png + world file`
* `.jpg + world file`

---

# Step 2 — Building Filtering

Reduce search space to roof regions.

```bash id="7lv7ot"
python building_filter.py
```

Input:

```text id="gk5rmb"
tiles/<GridID>/
```

Output:

* roof masks
* filtered building candidates

---

# Step 3 — Export COCO Dataset

Generate chips and annotations.

```bash id="4q9n2w"
python export_coco_dataset.py
```

Output:

```text id="y0w8sh"
data/coco/
├── images/
├── annotations.json
```

---

# Step 4 — Train Model

Train detection model.

```bash id="9w0m6p"
python train.py
```

Output:

```text id="w4pbj7"
weights/best.pt
```

Recommended:

* First pass: 640 px
* Second pass: 1024 px

---

# Step 5 — Detection and Evaluation

Run inference on new tiles.

```bash id="1f0z3e"
python detect_and_evaluate.py
```

Output:

```text id="prk5hn"
detections.geojson
metrics.csv
```

---

# Input Data

## Tiles

All tiles must be stored in:

```text id="89t4ap"
tiles/<GridID>/
```

## Annotations

Store annotations in:

```text id="2lryeu"
data/annotations/
```

Supported formats:

* GPKG
* GeoJSON

---

# Recommended Execution Order

```bash id="s3e0fj"
download_imagery.py
→ building_filter.py
→ export_coco_dataset.py
→ train.py
→ detect_and_evaluate.py
```

---

# Output Products

The pipeline produces:

* GeoTIFF imagery tiles
* roof candidate masks
* COCO dataset
* trained weights
* detection GeoJSON
* evaluation metrics

---

# Recommended Future Extensions

* roof segmentation before detection
* solar area estimation
* panel density mapping
* multi-grid batch inference

---

# Citation

If you use this repository in research, please cite the repository URL and related dataset source.

---
