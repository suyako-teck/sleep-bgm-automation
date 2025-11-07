#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""動画生成モジュール"""

import os
import logging
import multiprocessing
from moviepy.editor import AudioFileClip, ImageClip, TextClip, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFilter

logger = logging.getLogger(__name__)

# CPU最適化：利用可能なコア数を取得
CPU_COUNT = multiprocessing.cpu_count()
OPTIMAL_THREADS = max(1, CPU_COUNT - 1)  # 1コアはシステム用に残す

logger.info(f"💻 CPU情報: {CPU_COUNT}コア検出、{OPTIMAL_THREADS}スレッド使用")


class VideoCreator:
    """動画生成クラス"""
    
    def __init__(self):
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def create_video(self, audio_path, background, resolution, fps, title, channel_name="", output_name="final_video.mp4"):
        """動画を生成（CPU/GPU最適化）"""
        logger.info("🎬 動画生成中...")
        logger.info(f"💻 マルチスレッド: {OPTIMAL_THREADS}スレッド使用")
        
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        duration_hours = duration / 3600
        
        # 背景
        if not background or not os.path.exists(background):
            background = self._create_default_background(resolution)
        
        bg_clip = ImageClip(background).set_duration(duration)
        
        # タイトル（最初の5秒）
        try:
            txt_clip = TextClip(title, fontsize=50, color='white', size=(resolution[0]-100, None), method='caption')
            txt_clip = txt_clip.set_position('center').set_duration(5).fadeout(1)
            video = CompositeVideoClip([bg_clip, txt_clip], size=resolution)
        except:
            video = bg_clip
        
        video = video.set_audio(audio)
        
        output_path = os.path.join(self.output_dir, output_name)
        
        # 最適化されたエンコード設定
        encode_params = self._get_optimized_encode_params(duration_hours, resolution)
        
        logger.info(f"⚙️ エンコード設定:")
        logger.info(f"  - プリセット: {encode_params['preset']}")
        logger.info(f"  - ビットレート: {encode_params['bitrate']}")
        logger.info(f"  - スレッド数: {encode_params['threads']}")
        if encode_params['gpu']:
            logger.info(f"  - GPU高速化: 有効 ({encode_params['gpu']})")
        
        # エンコード実行（エラー時はフォールバック）
        try:
            video.write_videofile(
                output_path,
                fps=fps,
                codec=encode_params['codec'],
                audio_codec='aac',
                preset=encode_params['preset'],
                bitrate=encode_params['bitrate'],
                threads=encode_params['threads'],
                logger=None
            )
        except Exception as e:
            error_msg = str(e)
            
            # GPUエンコードエラーの場合、CPUにフォールバック
            if 'nvenc' in error_msg.lower() or 'nvcuda' in error_msg.lower() or \
               'amf' in error_msg.lower() or 'qsv' in error_msg.lower():
                logger.warning(f"⚠️ GPUエンコードエラー: CPUにフォールバック")
                logger.info(f"💻 CPUエンコード（libx264）で再試行...")
                
                # CPUエンコードで再試行
                video.write_videofile(
                    output_path,
                    fps=fps,
                    codec='libx264',
                    audio_codec='aac',
                    preset=encode_params['preset'],
                    bitrate=encode_params['bitrate'],
                    threads=encode_params['threads'],
                    logger=None
                )
                logger.info(f"✓ CPUエンコードで完了")
            else:
                # その他のエラーは再スロー
                raise
        
        logger.info(f"✓ 動画生成完了: {output_path}")
        return output_path
    
    def _get_optimized_encode_params(self, duration_hours, resolution):
        """動画の長さと解像度に応じた最適なエンコード設定"""
        width, height = resolution
        pixels = width * height
        
        # GPU対応チェック（NVIDIA, AMD, Intel）
        gpu_codec = self._detect_gpu_encoder()
        
        # 基本設定
        params = {
            'codec': gpu_codec if gpu_codec else 'libx264',
            'preset': 'medium',
            'bitrate': '5000k',
            'threads': OPTIMAL_THREADS,
            'gpu': gpu_codec
        }
        
        # 長尺動画の最適化（4時間以上）
        if duration_hours >= 4:
            params['preset'] = 'fast'  # 高速化優先
            params['bitrate'] = '3000k'  # ビットレート削減
            logger.info(f"🚀 長尺動画最適化: 高速エンコード有効")
        
        # 超長尺動画の最適化（8時間以上）
        elif duration_hours >= 8:
            params['preset'] = 'veryfast'  # さらに高速化
            params['bitrate'] = '2500k'
            logger.info(f"🚀 超長尺動画最適化: 超高速エンコード有効")
        
        # 高解像度の最適化
        if pixels >= 2073600:  # 1920x1080以上
            if not gpu_codec:
                # GPUなしの場合はビットレート調整
                params['bitrate'] = '4000k'
        
        return params
    
    def _detect_gpu_encoder(self):
        """利用可能なGPUエンコーダーを検出（実動作確認付き）"""
        import subprocess
        
        try:
            # ffmpegのエンコーダー一覧を取得
            result = subprocess.run(
                ['ffmpeg', '-encoders'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            encoders = result.stdout.lower()
            
            # 検出された各エンコーダーを実際にテスト
            # NVIDIA GPU (NVENC)
            if 'h264_nvenc' in encoders:
                if self._test_encoder('h264_nvenc'):
                    logger.info("🎮 NVIDIA GPU検出: NVENCエンコーダー使用")
                    return 'h264_nvenc'
                else:
                    logger.warning("⚠️ NVENCエンコーダーは利用不可（ドライバー問題）")
            
            # AMD GPU (AMF)
            if 'h264_amf' in encoders:
                if self._test_encoder('h264_amf'):
                    logger.info("🎮 AMD GPU検出: AMFエンコーダー使用")
                    return 'h264_amf'
                else:
                    logger.warning("⚠️ AMFエンコーダーは利用不可")
            
            # Intel GPU (QuickSync)
            if 'h264_qsv' in encoders:
                if self._test_encoder('h264_qsv'):
                    logger.info("🎮 Intel GPU検出: QuickSyncエンコーダー使用")
                    return 'h264_qsv'
                else:
                    logger.warning("⚠️ QuickSyncエンコーダーは利用不可")
            
            logger.info("💻 GPU未検出: CPUエンコード使用")
            return None
            
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
            logger.warning(f"⚠️ GPUチェック失敗: CPUエンコード使用")
            return None
    
    def _test_encoder(self, encoder_name):
        """エンコーダーが実際に動作するかテスト"""
        import subprocess
        import tempfile
        
        try:
            # 1秒の簡単なテスト動画を生成
            test_output = os.path.join(tempfile.gettempdir(), "test_encode.mp4")
            
            cmd = [
                'ffmpeg', '-y',
                '-f', 'lavfi', '-i', 'color=c=black:s=320x240:d=1',
                '-c:v', encoder_name,
                '-t', '1',
                test_output
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=10)
            
            # ファイルが生成されたか確認
            success = result.returncode == 0 and os.path.exists(test_output)
            
            # テストファイル削除
            try:
                os.remove(test_output)
            except:
                pass
            
            return success
            
        except Exception:
            return False
    
    def _create_default_background(self, resolution):
        """デフォルト背景生成"""
        img = Image.new('RGB', resolution, color=(15, 26, 58))
        draw = ImageDraw.Draw(img)
        
        for i in range(resolution[1]):
            ratio = i / resolution[1]
            r = int(15 + (31 - 15) * ratio)
            g = int(26 + (43 - 26) * ratio)
            b = int(58 + (91 - 58) * ratio)
            draw.line([(0, i), (resolution[0], i)], fill=(r, g, b))
        
        img = img.filter(ImageFilter.GaussianBlur(radius=20))
        
        os.makedirs("backgrounds", exist_ok=True)
        bg_path = "backgrounds/default_bg.png"
        img.save(bg_path)
        
        return bg_path

