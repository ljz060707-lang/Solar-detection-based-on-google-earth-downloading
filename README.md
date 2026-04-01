# Google Earth adapter for SA_Solar

This patch adds a new imagery adapter layer and keeps the downstream workflow unchanged.

## What it does

- Adds a pluggable `ImageryAdapter`
- Keeps the current WMS path as the default source
- Adds a `google_earth_local` source that ingests locally exported imagery
- Normalizes all outputs into the existing `tiles/<GridID>/..._geo.tif` layout
- Optionally writes PNG previews for quick QA

## Why this fits the repo

The repository already treats `scripts/imagery/download_tiles.py` as the image-ingest stage, with `tiles/<GridID>/` as the shared tile root. `export_coco_dataset.py` then builds chips from those GeoTIFF tiles, so standardizing the new source at the tile-ingest stage preserves the rest of the pipeline.

## Suggested usage

```bash
python scripts/imagery/download_imagery.py \
  --grid-id G1190 \
  --source google_earth_local \
  --source-dir /path/to/google_earth_exports \
  --preview-dir /path/to/google_earth_exports/previews
```

The source directory should contain legally obtained Google Earth exports that are already georeferenced, for example:

- GeoTIFF files
- PNG/JPG files with world files
- files with sidecar georeferencing metadata

## Integration note

If you want to preserve the old command name, replace the body of
`scripts/imagery/download_tiles.py` with a small wrapper that imports
`main()` from `scripts/imagery/download_imagery.py`.
