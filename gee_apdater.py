import ee
import geedim as gd
import rasterio
from rasterio.warp import reproject, Resampling
from shapely.geometry import box
import geopandas as gpd
import os
import yaml

def load_config(config_path: str = "imagery_sources.yaml") -> dict:
    """加载影像源配置"""
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def gee_download_tiles(config: dict) -> None:
    """从GEE下载影像并切割为瓦片"""
    ee.Initialize()
    source_config = config["sources"]["google_earth"]
    
    # 1. 定义下载区域（bbox转ee.Geometry）
    bbox = source_config["bbox"]  # [lon_min, lat_min, lon_max, lat_max]
    aoi = ee.Geometry.Rectangle(bbox)
    
    # 2. 选择影像（示例：Sentinel-2，云量<10%）
    image = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
             .filterDate("2024-01-01", "2024-12-31")
             .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 10))
             .filterBounds(aoi)
             .first())
    
    # 3. 初始化geedim下载器（绕过配额限制）
    gd_image = gd.MaskedImage.from_ee_image(image, aoi=aoi)
    
    # 4. 下载整幅影像（临时文件）
    temp_dir = "./temp_gee"
    os.makedirs(temp_dir, exist_ok=True)
    temp_tif = os.path.join(temp_dir, "full_image.tif")
    gd_image.download(temp_tif, scale=source_config["scale"] or 10)  # 10m分辨率
    
    # 5. 切割为瓦片（适配原有tiles目录结构）
    with rasterio.open(temp_tif) as src:
        # 重投影到WGS84（与现有流程一致）
        dst_crs = "EPSG:4326"
        meta = src.meta.copy()
        meta.update({
            "crs": dst_crs,
            "transform": rasterio.transform.from_bounds(*bbox, src.width, src.height)
        })
        
        # 瓦片切割（按256x256像素）
        tile_size = 256
        for i in range(0, src.width, tile_size):
            for j in range(0, src.height, tile_size):
                window = rasterio.windows.Window(i, j, tile_size, tile_size)
                tile_data = src.read(window=window)
                
                # 保存瓦片
                tile_bbox = box(
                    bbox[0] + (bbox[2]-bbox[0])*i/src.width,
                    bbox[1] + (bbox[3]-bbox[1])*j/src.height,
                    bbox[0] + (bbox[2]-bbox[0])*(i+tile_size)/src.width,
                    bbox[1] + (bbox[3]-bbox[1])*(j+tile_size)/src.height
                )
                tile_path = os.path.join(
                    source_config["output_dir"],
                    f"tile_{i//tile_size}_{j//tile_size}.tif"
                )
                
                with rasterio.open(tile_path, "w", **meta) as dst:
                    dst.write(tile_data)
        
        print(f"✅ 成功下载{src.width//tile_size * src.height//tile_size}个瓦片到{source_config['output_dir']}")

if __name__ == "__main__":
    config = load_config()
    gee_download_tiles(config)
