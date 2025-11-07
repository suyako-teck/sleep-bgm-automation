#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自動テストツール - システム全体の動作確認
"""

import os
import sys
import time
import logging
import tempfile
from datetime import datetime

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


class AutoTester:
    """自動テストクラス"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.start_time = time.time()
    
    def print_header(self, title):
        """セクションヘッダー"""
        print()
        print("=" * 70)
        print(f"  {title}")
        print("=" * 70)
        print()
    
    def test_result(self, name, passed, error_msg=""):
        """テスト結果を記録"""
        if passed:
            print(f"  ✅ {name}")
            self.passed += 1
        else:
            print(f"  ❌ {name}")
            if error_msg:
                print(f"     エラー: {error_msg}")
            self.failed += 1
    
    def test_warning(self, name, msg=""):
        """警告を記録"""
        print(f"  ⚠️  {name}")
        if msg:
            print(f"     {msg}")
        self.warnings += 1
    
    def test_modules(self):
        """モジュールインポートテスト"""
        self.print_header("📦 1. Pythonモジュールテスト")
        
        modules = [
            ('pydub', 'pydub'),
            ('moviepy', 'moviepy.editor'),
            ('PIL', 'PIL'),
            ('yaml', 'yaml'),
            ('google.oauth2', 'google.oauth2.credentials'),
            ('googleapiclient', 'googleapiclient.discovery'),
            ('numpy', 'numpy'),
            ('requests', 'requests'),
        ]
        
        for display_name, import_name in modules:
            try:
                __import__(import_name.split('.')[0])
                self.test_result(f"{display_name}", True)
            except ImportError as e:
                self.test_result(f"{display_name}", False, str(e))
    
    def test_project_modules(self):
        """プロジェクトモジュールテスト"""
        self.print_header("🔧 2. プロジェクトモジュールテスト")
        
        try:
            from modules.audio_processor import AudioProcessor
            self.test_result("audio_processor", True)
        except Exception as e:
            self.test_result("audio_processor", False, str(e))
        
        try:
            from modules.video_creator import VideoCreator
            self.test_result("video_creator", True)
        except Exception as e:
            self.test_result("video_creator", False, str(e))
        
        try:
            from modules.youtube_uploader import YouTubeUploader
            self.test_result("youtube_uploader", True)
        except Exception as e:
            self.test_result("youtube_uploader", False, str(e))
        
        try:
            from modules.metadata_generator import MetadataGenerator
            self.test_result("metadata_generator", True)
        except Exception as e:
            self.test_result("metadata_generator", False, str(e))
        
        try:
            from template_manager import TemplateManager
            self.test_result("template_manager", True)
        except Exception as e:
            self.test_result("template_manager", False, str(e))
    
    def test_templates(self):
        """テンプレートファイルテスト"""
        self.print_header("📁 3. テンプレートファイルテスト")
        
        try:
            from template_manager import TemplateManager
            tm = TemplateManager()
            
            categories = tm.get_all_categories()
            total_templates = sum(len(cat['templates']) for cat in categories.values())
            
            print(f"  📊 検出されたテンプレート: {total_templates}個")
            print()
            
            # 各カテゴリをテスト
            for category_name, category_info in categories.items():
                print(f"  {category_info['icon']} {category_name}: {len(category_info['templates'])}個")
                
                for template_name in category_info['templates']:
                    info = tm.get_template_info(template_name)
                    
                    if info['prompt'] and "見つかりません" not in info['prompt']:
                        self.test_result(f"  └─ {template_name}", True)
                    else:
                        self.test_result(f"  └─ {template_name}", False, "プロンプトが読み込めません")
            
        except Exception as e:
            self.test_result("テンプレート読み込み", False, str(e))
    
    def test_audio_processing(self):
        """音声処理テスト"""
        self.print_header("🔊 4. 音声処理テスト（サンプル生成）")
        
        try:
            from pydub import AudioSegment
            from pydub.generators import Sine
            
            # 5秒のテスト音源を3個生成
            print("  📝 テスト音源生成中...")
            test_files = []
            
            for i in range(3):
                tone = Sine(440 + i * 100).to_audio_segment(duration=5000)
                test_file = os.path.join(tempfile.gettempdir(), f"test_audio_{i}.mp3")
                tone.export(test_file, format="mp3")
                test_files.append(test_file)
            
            self.test_result("テスト音源生成（3個）", True)
            
            # 音声処理テスト
            from modules.audio_processor import AudioProcessor
            processor = AudioProcessor()
            
            print("  🔧 音声結合テスト...")
            output = processor.process_audio(
                test_files,
                fade_in=1,
                fade_out=1,
                crossfade=0.5,
                target_volume=-6,
                output_name="test_combined.mp3",
                target_duration_minutes=None
            )
            
            if os.path.exists(output):
                file_size = os.path.getsize(output) / 1024
                self.test_result(f"音声結合（{file_size:.1f}KB生成）", True)
                os.remove(output)
            else:
                self.test_result("音声結合", False, "出力ファイルが生成されませんでした")
            
            # テストファイル削除
            for f in test_files:
                try:
                    os.remove(f)
                except:
                    pass
            
        except Exception as e:
            self.test_result("音声処理", False, str(e))
    
    def test_video_creation(self):
        """動画生成テスト"""
        self.print_header("🎬 5. 動画生成テスト（5秒動画）")
        
        try:
            from pydub import AudioSegment
            from pydub.generators import Sine
            from modules.video_creator import VideoCreator
            
            # 5秒のテスト音源
            print("  📝 テスト音源生成中...")
            tone = Sine(440).to_audio_segment(duration=5000)
            test_audio = os.path.join(tempfile.gettempdir(), "test_video_audio.mp3")
            tone.export(test_audio, format="mp3")
            
            self.test_result("テスト音源生成", True)
            
            # 動画生成テスト
            print("  🎥 テスト動画生成中（5秒）...")
            creator = VideoCreator()
            
            start = time.time()
            output = creator.create_video(
                test_audio,
                None,
                (640, 480),
                30,
                "テスト動画",
                "",
                "test_video.mp4"
            )
            elapsed = time.time() - start
            
            if os.path.exists(output):
                file_size = os.path.getsize(output) / (1024 * 1024)
                self.test_result(f"動画生成（{file_size:.2f}MB、{elapsed:.1f}秒）", True)
                
                # 生成時間から8時間動画の推定時間を計算
                estimated_8h = (elapsed / 5) * (8 * 60 * 60)
                estimated_minutes = estimated_8h / 60
                print()
                print(f"  📊 推定処理時間（8時間動画）: 約{estimated_minutes:.1f}分")
                
                # クリーンアップ
                try:
                    os.remove(output)
                except:
                    pass
            else:
                self.test_result("動画生成", False, "出力ファイルが生成されませんでした")
            
            # テスト音源削除
            try:
                os.remove(test_audio)
            except:
                pass
            
        except Exception as e:
            self.test_result("動画生成", False, str(e))
    
    def test_youtube_auth(self):
        """YouTube認証テスト"""
        self.print_header("🔐 6. YouTube認証テスト")
        
        credentials_path = "credentials.json"
        token_path = "token.json"
        
        if os.path.exists(credentials_path):
            self.test_result("credentials.json", True)
        else:
            self.test_warning("credentials.json なし", "YouTube機能をテストできません")
        
        if os.path.exists(token_path):
            self.test_result("token.json（認証済み）", True)
            
            # 認証の有効性をテスト
            try:
                from modules.youtube_uploader import YouTubeUploader
                uploader = YouTubeUploader()
                # 認証サービスの取得のみ（アップロードはしない）
                youtube = uploader._get_authenticated_service()
                self.test_result("YouTube API接続", True)
            except Exception as e:
                self.test_result("YouTube API接続", False, "認証が無効です")
        else:
            self.test_warning("token.json なし", "auth.bat を実行してください")
    
    def test_gpu(self):
        """GPU検出テスト"""
        self.print_header("🎮 7. GPU高速化テスト")
        
        import subprocess
        
        try:
            result = subprocess.run(['ffmpeg', '-encoders'], capture_output=True, text=True, timeout=5)
            encoders = result.stdout.lower()
            
            gpu_found = False
            
            # NVIDIA
            if 'h264_nvenc' in encoders:
                print("  🔍 NVIDIA NVENC検出")
                if self._test_encoder_quick('h264_nvenc'):
                    self.test_result("NVIDIA NVENC動作確認", True)
                    gpu_found = True
                else:
                    self.test_warning("NVIDIA NVENC", "検出されたが動作しません")
            
            # AMD
            if 'h264_amf' in encoders:
                print("  🔍 AMD AMF検出")
                if self._test_encoder_quick('h264_amf'):
                    self.test_result("AMD AMF動作確認", True)
                    gpu_found = True
                else:
                    self.test_warning("AMD AMF", "検出されたが動作しません")
            
            # Intel
            if 'h264_qsv' in encoders:
                print("  🔍 Intel QuickSync検出")
                if self._test_encoder_quick('h264_qsv'):
                    self.test_result("Intel QuickSync動作確認", True)
                    gpu_found = True
                else:
                    self.test_warning("Intel QuickSync", "検出されたが動作しません")
            
            if not gpu_found:
                print("  💻 CPUエンコード使用")
                print("     → GPU高速化は利用できません（CPUで動作）")
            
        except Exception as e:
            self.test_warning("GPU検出", f"テスト失敗: {str(e)}")
    
    def _test_encoder_quick(self, encoder_name):
        """エンコーダーのクイックテスト"""
        import subprocess
        
        try:
            test_output = os.path.join(tempfile.gettempdir(), "quick_test.mp4")
            cmd = [
                'ffmpeg', '-y', '-loglevel', 'error',
                '-f', 'lavfi', '-i', 'color=c=black:s=320x240:d=1',
                '-c:v', encoder_name, '-t', '1',
                test_output
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=10)
            success = result.returncode == 0 and os.path.exists(test_output)
            
            try:
                os.remove(test_output)
            except:
                pass
            
            return success
        except:
            return False
    
    def test_ffmpeg(self):
        """ffmpegテスト"""
        self.print_header("🎬 8. ffmpegテスト")
        
        import subprocess
        
        try:
            result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                self.test_result(f"ffmpeg ({version_line[:50]}...)", True)
            else:
                self.test_result("ffmpeg", False, "実行エラー")
        except FileNotFoundError:
            self.test_result("ffmpeg", False, "インストールされていません")
        except Exception as e:
            self.test_result("ffmpeg", False, str(e))
    
    def test_performance(self):
        """パフォーマンステスト"""
        self.print_header("⚡ 9. パフォーマンステスト")
        
        import multiprocessing
        
        cpu_count = multiprocessing.cpu_count()
        print(f"  💻 CPU: {cpu_count}コア")
        
        # 簡易ベンチマーク
        print(f"  ⏱️ 演算速度テスト...")
        start = time.time()
        _ = sum(i * i for i in range(5000000))
        elapsed = time.time() - start
        
        if elapsed < 0.5:
            rating = "⭐⭐⭐⭐⭐ 非常に高速"
            self.test_result(f"CPU性能 ({elapsed:.2f}秒)", True)
        elif elapsed < 1.0:
            rating = "⭐⭐⭐⭐ 高速"
            self.test_result(f"CPU性能 ({elapsed:.2f}秒)", True)
        elif elapsed < 2.0:
            rating = "⭐⭐⭐ 標準"
            self.test_result(f"CPU性能 ({elapsed:.2f}秒)", True)
        else:
            rating = "⭐⭐ 低速"
            self.test_warning(f"CPU性能 ({elapsed:.2f}秒)", "CPUが遅い可能性")
        
        print(f"     評価: {rating}")
    
    def test_file_structure(self):
        """ファイル構造テスト"""
        self.print_header("📂 10. ファイル構造テスト")
        
        required_files = [
            "manual_mode_v2.py",
            "template_manager.py",
            "requirements.txt",
            "manual.bat",
            "setup.bat",
            "modules/__init__.py",
            "modules/audio_processor.py",
            "modules/video_creator.py",
            "modules/youtube_uploader.py",
            "modules/metadata_generator.py"
        ]
        
        for file in required_files:
            if os.path.exists(file):
                self.test_result(file, True)
            else:
                self.test_result(file, False, "ファイルが見つかりません")
        
        # templatesフォルダ
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        template_dir = os.path.join(parent_dir, "templates")
        
        if os.path.exists(template_dir):
            self.test_result("../templates/ フォルダ", True)
        else:
            self.test_result("../templates/ フォルダ", False, "テンプレートフォルダがありません")
    
    def run_all_tests(self):
        """全テスト実行"""
        print()
        print("╔" + "=" * 68 + "╗")
        print("║" + " " * 20 + "🧪 自動テスト実行 🧪" + " " * 20 + "║")
        print("╚" + "=" * 68 + "╝")
        
        # 仮想環境チェック
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            print()
            print(f"✅ 仮想環境で実行中: {sys.prefix}")
        else:
            print()
            print(f"⚠️  グローバルPythonで実行中")
            print(f"   manual.batから起動することを推奨")
        
        # 各テスト実行
        self.test_modules()
        self.test_project_modules()
        self.test_templates()
        self.test_audio_processing()
        self.test_video_creation()
        self.test_youtube_auth()
        self.test_gpu()
        self.test_ffmpeg()
        self.test_performance()
        self.test_file_structure()
        
        # 結果サマリー
        elapsed = time.time() - self.start_time
        
        print()
        print("=" * 70)
        print("📊 テスト結果サマリー")
        print("=" * 70)
        print()
        print(f"  ✅ 成功: {self.passed}個")
        print(f"  ❌ 失敗: {self.failed}個")
        print(f"  ⚠️  警告: {self.warnings}個")
        print(f"  ⏱️ 所要時間: {elapsed:.1f}秒")
        print()
        
        if self.failed == 0:
            print("=" * 70)
            print("🎉 すべてのテストに合格しました！")
            print("=" * 70)
            print()
            print("✅ このシステムは正常に動作します")
            print("✅ manual.bat を実行して動画を生成できます")
            print()
            return True
        else:
            print("=" * 70)
            print("⚠️  一部のテストが失敗しました")
            print("=" * 70)
            print()
            print("推奨対応:")
            print("  1. setup.bat を実行")
            print("  2. reinstall.bat を実行")
            print("  3. TROUBLESHOOTING.md を参照")
            print()
            return False


def main():
    tester = AutoTester()
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

