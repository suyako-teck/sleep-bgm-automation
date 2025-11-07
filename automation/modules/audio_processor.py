#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""音声処理モジュール"""

import os
import logging
from pydub import AudioSegment

logger = logging.getLogger(__name__)


class AudioProcessor:
    """音声処理クラス"""
    
    def __init__(self):
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def process_audio(self, segments, fade_in, fade_out, crossfade, target_volume, output_name="final_audio.mp3", target_duration_minutes=None):
        """複数音源を結合（target_duration_minutesが指定されていれば自動ループ）"""
        logger.info(f"🔧 {len(segments)}個の音源を結合...")
        
        combined = AudioSegment.empty()
        
        # 全音源を結合
        for i, segment_path in enumerate(segments):
            audio = AudioSegment.from_file(segment_path)
            
            # 音量調整
            current_db = audio.dBFS
            gain = target_volume - current_db
            audio = audio.apply_gain(gain)
            
            if i == 0:
                audio = audio.fade_in(fade_in * 1000)
                combined = audio
            else:
                combined = combined.append(audio, crossfade=crossfade * 1000)
        
        # 目標時間が指定されている場合、ループ処理
        if target_duration_minutes:
            target_duration_ms = target_duration_minutes * 60 * 1000  # 分→ミリ秒
            current_duration_ms = len(combined)
            
            logger.info(f"📏 現在の長さ: {current_duration_ms / 1000 / 60:.1f}分")
            logger.info(f"🎯 目標の長さ: {target_duration_minutes}分")
            
            if current_duration_ms < target_duration_ms:
                # 短い場合：ループして延長
                logger.info(f"🔄 目標時間まで自動ループ中...")
                base_audio = combined  # ループ用の基本音源を保存
                
                while len(combined) < target_duration_ms:
                    remaining_ms = target_duration_ms - len(combined)
                    
                    if remaining_ms >= len(base_audio):
                        # まだ1ループ分以上必要
                        combined = combined.append(base_audio, crossfade=crossfade * 1000)
                        logger.info(f"  → {len(combined) / 1000 / 60:.1f}分 / {target_duration_minutes}分")
                    else:
                        # 端数分だけ追加
                        partial_audio = base_audio[:remaining_ms]
                        combined = combined.append(partial_audio, crossfade=crossfade * 1000)
                        logger.info(f"  → {len(combined) / 1000 / 60:.1f}分（完了）")
                        break
                
                logger.info(f"✓ ループ完了: {len(combined) / 1000 / 60:.1f}分")
            
            elif current_duration_ms > target_duration_ms:
                # 長い場合：目標時間で切り取り
                logger.info(f"✂️ 目標時間で切り取り中...")
                combined = combined[:target_duration_ms]
                logger.info(f"✓ 切り取り完了: {len(combined) / 1000 / 60:.1f}分")
        
        # フェードアウト
        combined = combined.fade_out(fade_out * 1000)
        
        output_path = os.path.join(self.output_dir, output_name)
        combined.export(output_path, format="mp3", bitrate="320k")
        
        final_duration = len(combined) / 1000 / 60  # 分に変換
        logger.info(f"✓ 音声処理完了: {output_path} ({final_duration:.1f}分)")
        return output_path

