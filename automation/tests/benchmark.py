#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
パフォーマンステスト - システムの処理能力を測定
"""

import os
import time
import multiprocessing
import logging
from datetime import timedelta

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def test_cpu():
    """CPU性能テスト"""
    logger.info("=" * 70)
    logger.info("💻 CPU性能テスト")
    logger.info("=" * 70)
    
    cpu_count = multiprocessing.cpu_count()
    logger.info(f"CPU コア数: {cpu_count}")
    
    # CPUモデル名を取得（Windows）
    try:
        import platform
        import subprocess
        result = subprocess.run(['wmic', 'cpu', 'get', 'name'], capture_output=True, text=True)
        cpu_name = result.stdout.split('\n')[1].strip()
        logger.info(f"CPU モデル: {cpu_name}")
    except:
        pass
    
    # 簡易ベンチマーク
    logger.info("\n⏱️ 演算速度テスト（1000万回計算）...")
    start = time.time()
    _ = sum(i * i for i in range(10000000))
    elapsed = time.time() - start
    logger.info(f"所要時間: {elapsed:.2f}秒")
    
    if elapsed < 1.0:
        logger.info("評価: ⭐⭐⭐⭐⭐ 非常に高速")
    elif elapsed < 2.0:
        logger.info("評価: ⭐⭐⭐⭐ 高速")
    elif elapsed < 3.0:
        logger.info("評価: ⭐⭐⭐ 標準")
    else:
        logger.info("評価: ⭐⭐ 低速")
    
    logger.info("")


def test_gpu():
    """GPU性能テスト"""
    logger.info("=" * 70)
    logger.info("🎮 GPU性能テスト")
    logger.info("=" * 70)
    
    import subprocess
    
    try:
        # ffmpegのエンコーダー一覧を取得
        result = subprocess.run(['ffmpeg', '-encoders'], capture_output=True, text=True, timeout=5)
        encoders = result.stdout.lower()
        
        detected = []
        
        if 'h264_nvenc' in encoders:
            detected.append("NVIDIA NVENC")
            logger.info("✅ NVIDIA GPU検出")
            
            # NVIDIA GPU情報
            try:
                nvidia_info = subprocess.run(['nvidia-smi', '--query-gpu=name,driver_version,memory.total', '--format=csv,noheader'], 
                                            capture_output=True, text=True, timeout=5)
                if nvidia_info.returncode == 0:
                    logger.info(f"   {nvidia_info.stdout.strip()}")
            except:
                pass
        
        if 'h264_amf' in encoders:
            detected.append("AMD AMF")
            logger.info("✅ AMD GPU検出")
        
        if 'h264_qsv' in encoders:
            detected.append("Intel QuickSync")
            logger.info("✅ Intel QuickSync検出")
        
        if not detected:
            logger.info("❌ GPU エンコーダー未検出")
            logger.info("   → CPUエンコードを使用します")
        else:
            logger.info(f"\n🚀 利用可能な高速化: {', '.join(detected)}")
        
    except FileNotFoundError:
        logger.info("❌ ffmpeg が見つかりません")
        logger.info("   → GPU検出不可")
    except Exception as e:
        logger.info(f"⚠️ GPU検出エラー: {e}")
    
    logger.info("")


def test_storage():
    """ストレージ性能テスト"""
    logger.info("=" * 70)
    logger.info("💾 ストレージ性能テスト")
    logger.info("=" * 70)
    
    test_file = "output/benchmark_test.tmp"
    os.makedirs("output", exist_ok=True)
    
    # 100MB書き込みテスト
    logger.info("📝 書き込み速度テスト（100MB）...")
    data = b'0' * (1024 * 1024)  # 1MB
    
    start = time.time()
    with open(test_file, 'wb') as f:
        for _ in range(100):
            f.write(data)
    write_time = time.time() - start
    write_speed = 100 / write_time
    
    logger.info(f"書き込み: {write_speed:.1f} MB/s")
    
    # 読み込みテスト
    logger.info("📖 読み込み速度テスト（100MB）...")
    start = time.time()
    with open(test_file, 'rb') as f:
        _ = f.read()
    read_time = time.time() - start
    read_speed = 100 / read_time
    
    logger.info(f"読み込み: {read_speed:.1f} MB/s")
    
    # 評価
    logger.info("")
    if write_speed > 500:
        logger.info("評価: ⭐⭐⭐⭐⭐ NVMe SSD級")
    elif write_speed > 300:
        logger.info("評価: ⭐⭐⭐⭐ SATA SSD")
    elif write_speed > 100:
        logger.info("評価: ⭐⭐⭐ 高速HDD")
    else:
        logger.info("評価: ⭐⭐ 標準HDD")
    
    # テストファイル削除
    try:
        os.remove(test_file)
    except:
        pass
    
    logger.info("")


def estimate_performance():
    """推定パフォーマンス"""
    logger.info("=" * 70)
    logger.info("📊 推定処理時間")
    logger.info("=" * 70)
    
    import subprocess
    
    cpu_count = multiprocessing.cpu_count()
    
    # GPU検出
    gpu_detected = False
    try:
        result = subprocess.run(['ffmpeg', '-encoders'], capture_output=True, text=True, timeout=5)
        if 'nvenc' in result.stdout.lower():
            gpu_detected = True
            gpu_type = "NVIDIA NVENC"
        elif 'amf' in result.stdout.lower():
            gpu_detected = True
            gpu_type = "AMD AMF"
        elif 'qsv' in result.stdout.lower():
            gpu_detected = True
            gpu_type = "Intel QuickSync"
    except:
        pass
    
    if gpu_detected:
        logger.info(f"🎮 GPU高速化: {gpu_type}")
        logger.info("")
        logger.info("推定処理時間（GPU）:")
        logger.info("  - 25分動画: 約30秒")
        logger.info("  - 3時間動画: 約2分")
        logger.info("  - 8時間動画: 約3〜4分")
        logger.info("  - 10時間動画: 約4〜5分")
    else:
        logger.info(f"💻 CPUエンコード: {cpu_count}コア")
        logger.info("")
        logger.info("推定処理時間（CPU）:")
        
        if cpu_count >= 8:
            logger.info("  - 25分動画: 約3分")
            logger.info("  - 3時間動画: 約15分")
            logger.info("  - 8時間動画: 約25分")
            logger.info("  - 10時間動画: 約30分")
        elif cpu_count >= 4:
            logger.info("  - 25分動画: 約5分")
            logger.info("  - 3時間動画: 約25分")
            logger.info("  - 8時間動画: 約45分")
            logger.info("  - 10時間動画: 約60分")
        else:
            logger.info("  - 25分動画: 約8分")
            logger.info("  - 3時間動画: 約45分")
            logger.info("  - 8時間動画: 約120分")
            logger.info("  - 10時間動画: 約150分")
    
    logger.info("")
    logger.info("💡 ヒント:")
    if not gpu_detected:
        logger.info("  - GPU搭載で5〜10倍高速化")
    logger.info("  - 夜間に生成して朝には完成")
    logger.info("  - 週末にまとめて5本生成")
    
    logger.info("")


def main():
    logger.info("")
    logger.info("╔" + "=" * 68 + "╗")
    logger.info("║" + " " * 15 + "🔥 システムベンチマーク 🔥" + " " * 15 + "║")
    logger.info("╚" + "=" * 68 + "╝")
    logger.info("")
    
    test_cpu()
    test_gpu()
    test_storage()
    estimate_performance()
    
    logger.info("=" * 70)
    logger.info("✅ ベンチマーク完了")
    logger.info("=" * 70)
    logger.info("")
    logger.info("このシステムで快適に動画を生成できます！")
    logger.info("")


if __name__ == "__main__":
    main()

