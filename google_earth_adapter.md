Drop-in file pack for the SA_Solar repository.

Files:
- scripts/imagery/download_imagery.py
- scripts/imagery/imagery_adapters.py
- configs/datasets/imagery_sources.example.yaml
- docs/google_earth_adapter.md

Recommended integration:
1. Add the new files above.
2. Update `scripts/imagery/download_tiles.py` to call `download_imagery.py` or to import the new adapter.
3. Keep downstream scripts unchanged; they already consume the shared `tiles/<GridID>/` outputs.
