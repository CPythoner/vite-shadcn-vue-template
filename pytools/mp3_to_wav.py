from pydub import AudioSegment
import os
from pathlib import Path
import logging
import argparse
from tqdm import tqdm
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def convert_mp3_to_wav(mp3_path: str, output_dir: str = "WAV") -> bool:
    """
    转换单个MP3文件为WAV格式

    Args:
        mp3_path: MP3文件路径
        output_dir: WAV文件输出目录

    Returns:
        bool: 转换是否成功
    """
    try:
        mp3_path = Path(mp3_path)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        wav_path = output_dir / f"{mp3_path.stem}.wav"

        # 如果WAV文件已存在且比MP3新，则跳过
        if wav_path.exists() and wav_path.stat().st_mtime > mp3_path.stat().st_mtime:
            logger.info(f"跳过已存在的文件: {wav_path}")
            return True

        if not mp3_path.exists():
            logger.error(f"文件不存在: {mp3_path}")
            return False

        # 获取文件大小
        file_size = os.path.getsize(mp3_path)
        logger.info(f"正在转换: {mp3_path.name} ({file_size / 1024 / 1024:.1f} MB)")

        # 创建进度条
        with tqdm(total=3, desc="转换进度") as pbar:
            # 步骤 1: 加载音频
            pbar.set_description("加载音频")
            audio = AudioSegment.from_mp3(str(mp3_path))
            pbar.update(1)

            # 步骤 2: 设置参数
            pbar.set_description("设置参数")
            audio = audio.set_frame_rate(16000)  # 设置采样率为16kHz
            audio = audio.set_channels(1)        # 转换为单声道
            pbar.update(1)

            # 步骤 3: 导出文件
            pbar.set_description("导出文件")
            audio.export(str(wav_path), format="wav")
            pbar.update(1)

        logger.info(f"转换完成: {wav_path}")
        return True

    except Exception as e:
        logger.error(f"转换失败 {mp3_path.name}: {str(e)}")
        return False

def main():
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='将MP3文件转换为WAV格式')
    parser.add_argument('input', help='输入的MP3文件路径')
    parser.add_argument('-o', '--output-dir', default='WAV', help='输出目录 (默认: WAV)')

    # 解析命令行参数
    args = parser.parse_args()

    # 转换文件
    start_time = time.time()
    success = convert_mp3_to_wav(args.input, args.output_dir)
    end_time = time.time()

    # 打印结果
    if success:
        duration = end_time - start_time
        logger.info(f"转换成功，耗时: {duration:.1f} 秒")
    else:
        logger.error("转换失败")

if __name__ == "__main__":
    main()
