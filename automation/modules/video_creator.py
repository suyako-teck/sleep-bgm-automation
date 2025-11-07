#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""動画生成モジュール"""

import os
import logging
from moviepy.editor import AudioFileClip, ImageClip, TextClip, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFilter

logger = logging.getLogger(__name__)


class VideoCreator:
    """動画生成クラス"""
    
    def __init__(self):
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def create_video(self, audio_path, background, resolution, fps, title, channel_name="", output_name="final_video.mp4"):
        """動画を生成"""
        logger.info("🎬 動画生成中...")
        
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        
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
        video.write_videofile(output_path, fps=fps, codec='libx264', audio_codec='aac', preset='medium', logger=None)
        
        logger.info(f"✓ 動画生成完了: {output_path}")
        return output_path
    
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

