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
        
    def process_audio(self, segments, fade_in, fade_out, crossfade, target_volume, output_name="final_audio.mp3"):
        """複数音源を結合"""
        logger.info(f"🔧 {len(segments)}個の音源を結合...")
        
        combined = AudioSegment.empty()
        
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
        
        combined = combined.fade_out(fade_out * 1000)
        
        output_path = os.path.join(self.output_dir, output_name)
        combined.export(output_path, format="mp3", bitrate="320k")
        
        logger.info(f"✓ 音声処理完了: {output_path}")
        return output_path

