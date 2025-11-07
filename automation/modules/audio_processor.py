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
            target_duration_ms = int(target_duration_minutes * 60 * 1000)  # 分→ミリ秒（整数化）
            current_duration_ms = len(combined)
            
            logger.info(f"📏 現在の長さ: {current_duration_ms / 1000 / 60:.1f}分")
            logger.info(f"🎯 目標の長さ: {target_duration_minutes}分")
            
            if current_duration_ms < target_duration_ms:
                # 短い場合：ループして延長（チャンク方式で効率化）
                logger.info(f"🔄 目標時間まで自動ループ中...")
                base_audio = combined  # ループ用の基本音源を保存
                base_duration_ms = len(base_audio)
                
                # 必要なループ回数を計算
                loops_needed = (target_duration_ms - current_duration_ms) // base_duration_ms
                remaining_ms = target_duration_ms - current_duration_ms - (loops_needed * base_duration_ms)
                
                logger.info(f"  📊 ループ回数: {loops_needed}回 + 端数{remaining_ms/1000:.1f}秒")
                
                # ループを追加（大きなチャンクで処理）
                for loop_num in range(int(loops_needed)):
                    combined = combined.append(base_audio, crossfade=crossfade * 1000)
                    if (loop_num + 1) % 5 == 0:  # 5回ごとに進捗表示
                        logger.info(f"  → {len(combined) / 1000 / 60:.1f}分 / {target_duration_minutes}分")
                
                # 端数があれば追加
                if remaining_ms > 0:
                    partial_audio = base_audio[:int(remaining_ms)]
                    combined = combined.append(partial_audio, crossfade=crossfade * 1000)
                
                logger.info(f"✓ ループ完了: {len(combined) / 1000 / 60:.1f}分")
            
            elif current_duration_ms > target_duration_ms:
                # 長い場合：目標時間で切り取り
                logger.info(f"✂️ 目標時間で切り取り中...")
                combined = combined[:int(target_duration_ms)]
                logger.info(f"✓ 切り取り完了: {len(combined) / 1000 / 60:.1f}分")
        
        # フェードアウト
        combined = combined.fade_out(fade_out * 1000)
        
        output_path = os.path.join(self.output_dir, output_name)
        final_duration_minutes = len(combined) / 1000 / 60
        
        # 長尺音源の場合は低ビットレートで軽量化
        if final_duration_minutes > 180:  # 3時間以上
            logger.info(f"⚠️ 長尺音源のため192kbpsで出力します")
            bitrate = "192k"
        else:
            bitrate = "320k"
        
        logger.info(f"💾 MP3エクスポート中（{final_duration_minutes:.1f}分）...")
        
        # 超長尺の場合は分割エクスポート（WAVファイルサイズ制限回避）
        if final_duration_minutes > 240:  # 4時間以上
            logger.info(f"🔄 超長尺のため分割エクスポート方式を使用")
            self._export_long_audio(combined, output_path, bitrate, final_duration_minutes)
        else:
            # 通常エクスポート
            combined.export(output_path, format="mp3", bitrate=bitrate, parameters=["-q:a", "2"])
        
        logger.info(f"✓ 音声処理完了: {output_path} ({final_duration_minutes:.1f}分)")
        return output_path
    
    def _export_long_audio(self, audio_segment, output_path, bitrate, duration_minutes):
        """超長尺音源を分割してエクスポート"""
        import tempfile
        import subprocess
        
        # 60分ごとに分割
        chunk_duration_ms = 60 * 60 * 1000  # 60分
        total_duration_ms = len(audio_segment)
        num_chunks = (total_duration_ms + chunk_duration_ms - 1) // chunk_duration_ms
        
        logger.info(f"  📦 {num_chunks}個のチャンクに分割...")
        
        temp_files = []
        temp_dir = tempfile.gettempdir()
        
        try:
            # 各チャンクをエクスポート
            for i in range(num_chunks):
                start_ms = i * chunk_duration_ms
                end_ms = min((i + 1) * chunk_duration_ms, total_duration_ms)
                
                chunk = audio_segment[start_ms:end_ms]
                temp_file = os.path.join(temp_dir, f"chunk_{i:03d}.mp3")
                
                # MP3に直接エクスポート（WAV経由を回避）
                chunk.export(temp_file, format="mp3", bitrate=bitrate, parameters=["-q:a", "2"])
                temp_files.append(temp_file)
                
                logger.info(f"    → チャンク {i+1}/{num_chunks} 完了")
            
            # ffmpegで結合
            logger.info(f"  🔗 チャンクを結合中...")
            
            # concat用のファイルリスト作成
            concat_file = os.path.join(temp_dir, "concat_list.txt")
            with open(concat_file, 'w', encoding='utf-8') as f:
                for temp_file in temp_files:
                    # Windowsパスをエスケープ
                    escaped_path = temp_file.replace('\\', '/')
                    f.write(f"file '{escaped_path}'\n")
            
            # ffmpegで結合
            cmd = [
                'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
                '-i', concat_file,
                '-c', 'copy',  # 再エンコードなし（高速）
                output_path
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"  ✓ 結合完了")
            
        finally:
            # 一時ファイル削除
            for temp_file in temp_files:
                try:
                    os.remove(temp_file)
                except:
                    pass
            try:
                os.remove(concat_file)
            except:
                pass

