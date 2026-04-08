import os
import yaml
import argparse
import numpy as np
import rasterio
from rasterio.transform import from_bounds

def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def generate_test_tiles(config):
    """生成测试瓦片（跳过网络下载，快速验证流程）"""
    output_dir = config['sources']['google_earth']['output_dir']
    bbox = config['sources']['google_earth']['bbox']
    os.makedirs(output_dir, exist_ok=True)

    # 生成1张模拟GeoTIFF瓦片
    tile_path = os.path.join(output_dir, "test_tile.tif")
    width, height = 256, 256
    transform = from_bounds(*bbox, width, height)

    with rasterio.open(
        tile_path, 'w',
        driver='GTiff',
        height=height, width=width,
        count=3, dtype=np.uint8,
        crs='EPSG:4326',
        transform=transform
    ) as dst:
        dst.write(np.random.randint(0,255,(3,height,width), dtype=np.uint8))
    print(f"✅ 测试瓦片生成完成：{tile_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='imagery_sources.yaml')
    args = parser.parse_args()
    config = load_config(args.config)
    generate_test_tiles(config)
