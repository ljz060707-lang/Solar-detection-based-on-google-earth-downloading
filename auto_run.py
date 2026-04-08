import subprocess
import time

def run_cmd(cmd, step):
    print(f"\n===== 执行步骤：{step} =====")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"❌ 步骤{step}失败！")
        exit(1)
    time.sleep(1)

# 全流程自动化命令
steps = [
    ("python download_tiles.py", "生成影像瓦片"),
    ("python building_filter.py", "建筑屋顶过滤"),
    ("python export_coco_dataset.py", "导出COCO数据集"),
    ("python train.py --epochs 5 --batch-size 2 --device cpu", "模型训练"),
    ("python detect_and_evaluate.py --model ./runs/train/exp/weights/best.pt", "推理评估")
]

for cmd, step in steps:
    run_cmd(cmd, step)

print("\n🎉 全流程自动化执行完成！")
