#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
半自動モード v2 - テンプレート選択＋ショート対応
⚠️ Mubert APIは使用しません（費用節約）
"""

import os
import sys
import logging
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import webbrowser

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# モジュールインポート
try:
    from modules.audio_processor import AudioProcessor
    from modules.video_creator import VideoCreator
    from modules.youtube_uploader import YouTubeUploader
    from modules.metadata_generator import MetadataGenerator
    from template_manager import TemplateManager
except ImportError as e:
    print(f"❌ モジュールのインポートエラー: {e}")
    print("setup.bat を実行してください")
    sys.exit(1)


class ManualModeGUI:
    """半自動モードGUI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("AI音楽BGM 半自動生成ツール v2 - API不使用")
        self.root.geometry("1400x850")
        
        self.checklist_vars = {}
        self.audio_files = []
        self.config = {}
        self.template_manager = TemplateManager()
        self.video_type = tk.StringVar(value="long")
        self.generated_long_video = None
        self.selected_template = None
        
        self.create_widgets()
    
    def create_widgets(self):
        """ウィジェット作成"""
        
        # 左：チェックリスト
        left_frame = ttk.Frame(self.root, padding="10", width=300)
        left_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.W))
        left_frame.grid_propagate(False)
        
        ttk.Label(left_frame, text="📋 制作チェックリスト", font=('Arial', 12, 'bold')).pack(pady=10)
        
        checklist_items = [
            ("step1", "1. テンプレート選択"),
            ("step2", "2. プロンプト確認"),
            ("step3", "3. Mubert音源生成"),
            ("step4", "4. 音源ファイル選択"),
            ("step5", "5. 形式選択"),
            ("step6", "6. 設定入力"),
            ("step7", "7. 動画生成"),
            ("step8", "8. アップロード")
        ]
        
        for key, text in checklist_items:
            var = tk.BooleanVar()
            self.checklist_vars[key] = var
            ttk.Checkbutton(left_frame, text=text, variable=var, command=self.update_progress).pack(anchor=tk.W, pady=3)
        
        self.progress_label = ttk.Label(left_frame, text="進捗: 0/8", font=('Arial', 11, 'bold'), foreground='blue')
        self.progress_label.pack(pady=15)
        
        next_frame = ttk.LabelFrame(left_frame, text="次のステップ", padding="10")
        next_frame.pack(fill=tk.X, pady=10)
        self.next_step_label = tk.Label(next_frame, text="テンプレート選択", wraplength=260, justify=tk.LEFT, fg='green')
        self.next_step_label.pack()
        
        # 中央：テンプレート選択
        center_frame = ttk.Frame(self.root, padding="10")
        center_frame.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.W, tk.E))
        
        ttk.Label(center_frame, text="🎵 テンプレート選択", font=('Arial', 12, 'bold')).pack(pady=10)
        
        self.category_notebook = ttk.Notebook(center_frame)
        self.category_notebook.pack(fill=tk.BOTH, expand=True)
        self.create_category_tabs()
        
        # プロンプト表示
        prompt_frame = ttk.LabelFrame(center_frame, text="📝 Mubertプロンプト（手動生成用）", padding="10")
        prompt_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        ttk.Label(prompt_frame, text="⚠️ API不使用 - Mubertサイトで手動生成", foreground='red', font=('Arial', 9, 'bold')).pack(pady=5)
        
        self.prompt_text = scrolledtext.ScrolledText(prompt_frame, height=5, wrap=tk.WORD)
        self.prompt_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        btn_frame = ttk.Frame(prompt_frame)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="📋 コピー", command=self.copy_prompt, width=15).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_frame, text="🌐 Mubert開く", command=self.open_mubert, width=15).pack(side=tk.LEFT, padx=3)
        
        # 右：設定・実行
        right_frame = ttk.Frame(self.root, padding="10")
        right_frame.grid(row=0, column=2, sticky=(tk.N, tk.S, tk.W, tk.E))
        
        # 形式選択
        format_frame = ttk.LabelFrame(right_frame, text="📹 動画形式", padding="10")
        format_frame.pack(fill=tk.X, pady=10)
        ttk.Radiobutton(format_frame, text="🎬 ロング（25分〜8時間）", variable=self.video_type, value="long").pack(anchor=tk.W)
        ttk.Radiobutton(format_frame, text="📱 ショート（60秒）", variable=self.video_type, value="short").pack(anchor=tk.W)
        
        # 音源選択
        audio_frame = ttk.LabelFrame(right_frame, text="🎵 音源（手動ダウンロード）", padding="10")
        audio_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(audio_frame, text="音源追加", command=self.add_audio).pack(pady=3, fill=tk.X)
        self.audio_listbox = tk.Listbox(audio_frame, height=4)
        self.audio_listbox.pack(fill=tk.X, pady=3)
        
        # 設定
        settings_frame = ttk.LabelFrame(right_frame, text="⚙️ 設定", padding="10")
        settings_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(settings_frame, text="タイトル:").grid(row=0, column=0, sticky=tk.W)
        self.title_entry = ttk.Entry(settings_frame, width=40)
        self.title_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=3)
        
        ttk.Label(settings_frame, text="長さ:").grid(row=1, column=0, sticky=tk.W)
        duration_frame = ttk.Frame(settings_frame)
        duration_frame.grid(row=1, column=1, sticky=tk.W, pady=3)
        
        self.duration_var = tk.StringVar(value="480")
        duration_options = [
            ("25分（ポモドーロ）", "25"),
            ("1時間（短時間作業）", "60"),
            ("3時間（作業セッション）", "180"),
            ("5時間（長時間作業）", "300"),
            ("8時間（睡眠）", "480"),
            ("10時間（深い睡眠）", "600"),
            ("12時間（超長時間）", "720")
        ]
        
        duration_combo = ttk.Combobox(duration_frame, textvariable=self.duration_var, width=25, state='readonly')
        duration_combo['values'] = [f"{label} - {mins}分" for label, mins in duration_options]
        duration_combo.set("8時間（睡眠） - 480分")
        duration_combo.bind('<<ComboboxSelected>>', lambda e: self._on_duration_change())
        duration_combo.pack(side=tk.LEFT)
        
        ttk.Label(duration_frame, text="※音源を自動ループ", foreground='gray', font=('Arial', 8)).pack(side=tk.LEFT, padx=5)
        
        settings_frame.columnconfigure(1, weight=1)
        
        # 実行ボタン
        button_frame = ttk.LabelFrame(right_frame, text="🚀 実行（API費用0円）", padding="10")
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(button_frame, text="✅ YouTube APIのみ使用（無料）", foreground='green', font=('Arial', 8)).pack(pady=5)
        
        ttk.Button(button_frame, text="🎬 動画生成", command=self.generate_video, width=25).pack(pady=3, fill=tk.X)
        ttk.Button(button_frame, text="📤 アップロード", command=self.upload_video, width=25).pack(pady=3, fill=tk.X)
        ttk.Button(button_frame, text="🚀 生成＋アップロード", command=self.generate_and_upload, width=25).pack(pady=3, fill=tk.X)
        
        # ログ
        log_frame = ttk.LabelFrame(self.root, text="📊 ログ", padding="5")
        log_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # ステータスバー
        self.status_var = tk.StringVar(value="準備完了")
        ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        self.root.columnconfigure(1, weight=2)
        self.root.columnconfigure(2, weight=2)
        self.root.rowconfigure(0, weight=1)
    
    def create_category_tabs(self):
        """カテゴリタブ作成"""
        for category, info in self.template_manager.get_all_categories().items():
            tab = ttk.Frame(self.category_notebook)
            self.category_notebook.add(tab, text=f"{info['icon']} {category}")
            
            ttk.Label(tab, text=info['description'], foreground='gray').pack(pady=10)
            
            btn_container = ttk.Frame(tab)
            btn_container.pack(fill=tk.BOTH, expand=True, padx=10)
            
            for i, template_name in enumerate(info['templates']):
                ttk.Button(btn_container, text=template_name, command=lambda t=template_name: self.select_template(t), width=20).grid(row=i//2, column=i%2, padx=5, pady=5)
    
    def select_template(self, template_name):
        """テンプレート選択"""
        self.selected_template = template_name
        self.log(f"✓ 選択: {template_name}")
        
        info = self.template_manager.get_template_info(template_name)
        
        self.prompt_text.delete(1.0, tk.END)
        self.prompt_text.insert(1.0, info['prompt'])
        
        # タイトルを自動生成
        self._update_title()
        
        self.config['tags'] = info['tags']
        
        self.checklist_vars['step1'].set(True)
        self.update_progress()
        self.status_var.set(f"{template_name} - Mubertで音源生成してください")
    
    def _update_title(self):
        """選択されたテンプレートと時間からタイトルを自動生成"""
        if not self.selected_template:
            return
        
        # 時間を取得
        duration_text = self.duration_var.get()
        # "8時間（睡眠） - 480分" から "8時間" を抽出
        if " - " in duration_text:
            duration_label = duration_text.split(" - ")[0]
        else:
            duration_label = duration_text
        
        # タイトルパターン
        template_titles = {
            "ピンクノイズ": f"【{duration_label}】ピンクノイズで深い眠り | 睡眠導入・集中力アップ",
            "ホワイトノイズ": f"【{duration_label}】ホワイトノイズで快適な睡眠 | 赤ちゃんの寝かしつけにも",
            "ブラウンノイズ": f"【{duration_label}】ブラウンノイズで深い集中 | 勉強・作業用BGM",
            "雨音": f"【{duration_label}】雨の音でリラックス | 睡眠・作業用BGM",
            "水音": f"【{duration_label}】小川のせせらぎ | 自然音で癒しの時間",
            "森": f"【{duration_label}】森の音 | 鳥のさえずりで目覚める朝",
            "海辺": f"【{duration_label}】波の音でリラックス | 睡眠・瞑想用BGM",
            "森の夜": f"【{duration_label}】森の夜 | 虫の音で深い眠り",
            "自然": f"【{duration_label}】自然の音 | リラックス・睡眠用BGM",
            "炎": f"【{duration_label}】暖炉の音 | 焚き火のパチパチ音で癒し",
            "雨焚火": f"【{duration_label}】雨音と焚き火 | 究極の癒しBGM",
            "ピアノ": f"【{duration_label}】静かなピアノ曲 | 睡眠・作業用BGM",
            "自然ピアノ": f"【{duration_label}】ピアノと自然音 | 癒しの音楽",
            "子守歌": f"【{duration_label}】優しい子守歌 | 赤ちゃんの寝かしつけ",
            "雨窓ローファイ": f"【{duration_label}】Lo-fi × 雨音 | 作業・勉強用BGM",
            "アンビエント": f"【{duration_label}】アンビエント音楽 | 瞑想・睡眠用",
            "星空ドローン": f"【{duration_label}】星空ドローン | 宇宙的な癒しの音",
            "シータ波": f"【{duration_label}】シータ波バイノーラル | 深い瞑想・睡眠",
            "風鈴せせらぎ": f"【{duration_label}】風鈴とせせらぎ | 和の癒しBGM",
            "ASMRソフトタッチ": f"【{duration_label}】ASMRソフトタッチ | タッピング音で睡眠",
            "ささやきガイド": f"【{duration_label}】ささやき睡眠誘導 | 眠りのガイド付き",
            "ポモドーロ作業": f"【{duration_label}】ポモドーロ作業BGM | ブラウンノイズで深い集中",
            "ポモドーロ休憩": f"【{duration_label}】ポモドーロ休憩BGM | 集中力リセット・リフレッシュ音楽",
            "ポモドーロ長休憩": f"【{duration_label}】ポモドーロ長休憩BGM | 自然音で深いリフレッシュ"
        }
        
        # タイトルを設定
        title = template_titles.get(self.selected_template, f"【{duration_label}】{self.selected_template} | 睡眠・リラックス用BGM")
        
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, title)
        
        self.log(f"📝 タイトル自動生成: {title}")
    
    def _on_duration_change(self):
        """長さ変更時にタイトルを更新"""
        if self.selected_template:
            self._update_title()
            self.log(f"⏱️ 長さ変更: {self.duration_var.get()}")
    
    def open_mubert(self):
        """Mubertサイトを開く"""
        webbrowser.open("https://mubert.com/render")
        self.log("🌐 Mubert開きました")
        messagebox.showinfo("手順", "1. プロンプトを貼り付け\n2. Duration: 600秒\n3. Generate\n4. Download\n5. 音源追加")
    
    def copy_prompt(self):
        """プロンプトコピー"""
        prompt = self.prompt_text.get(1.0, tk.END).strip()
        if not prompt or "見つかりません" in prompt:
            messagebox.showwarning("警告", "先にテンプレート選択")
            return
        
        self.root.clipboard_clear()
        self.root.clipboard_append(prompt)
        self.log("✓ コピー完了")
        
        if messagebox.askyesno("コピー完了", "Mubertサイトを開きますか？"):
            self.open_mubert()
        
        self.checklist_vars['step2'].set(True)
        self.update_progress()
    
    def add_audio(self):
        """音源追加"""
        files = filedialog.askopenfilenames(title="音源選択", filetypes=[("Audio", "*.mp3 *.wav"), ("All", "*.*")])
        for file in files:
            if file not in self.audio_files:
                self.audio_files.append(file)
                self.audio_listbox.insert(tk.END, os.path.basename(file))
        
        if files:
            self.checklist_vars['step3'].set(True)
            self.checklist_vars['step4'].set(True)
            self.update_progress()
            self.log(f"✓ {len(files)}個追加")
    
    def update_progress(self):
        """進捗更新"""
        completed = sum(1 for v in self.checklist_vars.values() if v.get())
        self.progress_label.config(text=f"進捗: {completed}/8")
    
    def log(self, msg):
        """ログ表示"""
        self.log_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def generate_video(self):
        """動画生成"""
        if not self.audio_files:
            messagebox.showerror("エラー", "音源を選択してください")
            return
        
        self.status_var.set("🎬 動画生成中...")
        self.log("=" * 70)
        self.log("🎬 動画生成開始")
        self.log("=" * 70)
        
        try:
            # 設定情報をログ出力
            self.log(f"📋 設定情報:")
            self.log(f"  ├─ テンプレート: {self.selected_template}")
            self.log(f"  ├─ タイトル: {self.title_entry.get()}")
            self.log(f"  ├─ 形式: {'ショート動画' if self.video_type.get() == 'short' else 'ロング動画'}")
            self.log(f"  └─ 音源数: {len(self.audio_files)}個")
            self.log("")
            
            # 目標時間を取得（コンボボックスから分数を抽出）
            duration_text = self.duration_var.get()
            # "8時間（睡眠） - 480分" から "480" を抽出
            target_minutes = int(duration_text.split(" - ")[1].replace("分", ""))
            self.log(f"⏱️ 目標時間: {target_minutes}分 ({target_minutes/60:.1f}時間)")
            self.log("")
            
            self.log("🔊 音声処理を開始...")
            
            processor = AudioProcessor()
            
            # 音源を結合＋ループ処理
            final_audio = processor.process_audio(
                self.audio_files, 
                fade_in=3, 
                fade_out=5, 
                crossfade=1, 
                target_volume=-6, 
                output_name=f"{self.selected_template}_audio.mp3",
                target_duration_minutes=target_minutes
            )
            
            self.log("")
            self.log("✅ 音声処理完了")
            self.log("")
            
            self.log("🎥 動画生成を開始...")
            creator = VideoCreator()
            
            is_short = self.video_type.get() == "short"
            resolution = (1080, 1920) if is_short else (1920, 1080)
            output_name = f"{'short' if is_short else 'long'}_{self.selected_template}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
            
            self.log(f"  ├─ 解像度: {resolution[0]}x{resolution[1]}")
            self.log(f"  ├─ FPS: 30")
            self.log(f"  └─ 出力ファイル: {output_name}")
            self.log("")
            
            video_path = creator.create_video(final_audio, None, resolution, 30, self.title_entry.get(), "", output_name)
            
            self.config['video_path'] = video_path
            self.generated_long_video = video_path
            
            self.log("")
            self.log("✅ 動画生成完了")
            self.log(f"📁 保存先: {os.path.abspath(video_path)}")
            self.log(f"📊 ファイルサイズ: {os.path.getsize(video_path) / (1024**3):.2f} GB")
            self.log("")
            self.log("=" * 70)
            
            self.status_var.set("✅ 動画生成完了")
            
            self.checklist_vars['step7'].set(True)
            self.update_progress()
            
            if messagebox.askyesno("完了", f"動画生成完了\n\n{os.path.basename(video_path)}\n\nフォルダを開きますか？"):
                os.startfile(os.path.dirname(os.path.abspath(video_path)))
            
        except Exception as e:
            self.log(f"❌ エラー: {e}")
            self.status_var.set("❌ エラー")
            messagebox.showerror("エラー", str(e))
    
    def upload_video(self):
        """アップロード"""
        if 'video_path' not in self.config:
            file = filedialog.askopenfilename(title="動画選択", filetypes=[("Video", "*.mp4"), ("All", "*.*")])
            if not file:
                return
            self.config['video_path'] = file
        
        self.status_var.set("📤 アップロード中...")
        self.log("")
        self.log("=" * 70)
        self.log("📤 YouTubeアップロード開始")
        self.log("=" * 70)
        self.log("")
        self.log(f"📹 動画: {os.path.basename(self.config['video_path'])}")
        self.log(f"📝 タイトル: {self.title_entry.get()}")
        self.log("")
        self.log("🔐 YouTube認証中...")
        
        try:
            uploader = YouTubeUploader()
            metadata_gen = MetadataGenerator()
            
            tags = self.config.get('tags', metadata_gen.generate_tags_from_template(self.selected_template or ""))
            
            description = f"""ご視聴ありがとうございます。
{self.duration_entry.get()}分間の{self.selected_template or 'BGM'}です。

▷ 特徴
- 60 BPMの落ち着いたサウンド
- 長時間再生対応

▷ 制作
- 音源：Mubert (Creator/Proプラン)
- 制作日：{datetime.now().strftime("%Y-%m-%d")}

#sleep #relaxing #bgm #作業用BGM #睡眠導入
"""
            
            self.log("✅ 認証成功")
            self.log("")
            self.log("📤 アップロード実行中...")
            self.log("  （進捗は別ウィンドウで確認してください）")
            self.log("")
            
            video_id = uploader.upload_video(self.config['video_path'], self.title_entry.get(), description, tags[:15], 10, 'public')
            
            url = f"https://www.youtube.com/watch?v={video_id}"
            
            self.log("")
            self.log("=" * 70)
            self.log("✅ YouTubeアップロード完了")
            self.log("=" * 70)
            self.log("")
            self.log(f"🎬 動画ID: {video_id}")
            self.log(f"🔗 URL: {url}")
            self.log(f"📊 タグ数: {len(tags[:15])}個")
            self.log("")
            self.log("✅ URLをクリップボードにコピーしました")
            self.log("")
            
            self.root.clipboard_clear()
            self.root.clipboard_append(url)
            
            self.status_var.set("✅ 完了")
            self.checklist_vars['step8'].set(True)
            self.update_progress()
            
            messagebox.showinfo("完了", f"アップロード完了！\n\n動画ID: {video_id}\n\n{url}\n\nURLをクリップボードにコピーしました")
            
        except Exception as e:
            self.log(f"❌ エラー: {e}")
            self.status_var.set("❌ エラー")
            messagebox.showerror("エラー", str(e))
    
    def generate_and_upload(self):
        """生成＋アップロード"""
        self.checklist_vars['step6'].set(True)
        self.update_progress()
        
        self.generate_video()
        
        if 'video_path' in self.config and os.path.exists(self.config['video_path']):
            if messagebox.askyesno("確認", "YouTubeにアップロードしますか？"):
                self.upload_video()


def check_requirements():
    """起動前の必須ファイル・環境チェック"""
    print("=" * 70)
    print("🔍 起動前チェック")
    print("=" * 70)
    print()
    
    # 仮想環境チェック
    import sys
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print(f"✅ 仮想環境で実行中: {sys.prefix}")
    else:
        print(f"⚠️  グローバルPythonで実行中: {sys.prefix}")
        print(f"   manual.bat から起動してください")
    print()
    
    issues = []
    warnings = []
    
    # 1. Pythonモジュールチェック
    print("📦 Pythonモジュールチェック:")
    required_modules = [
        ('pydub', 'pydub'),
        ('moviepy', 'moviepy'),
        ('PIL (Pillow)', 'PIL'),
        ('google.oauth2', 'google.oauth2'),
        ('googleapiclient', 'googleapiclient'),
        ('yaml (PyYAML)', 'yaml')
    ]
    
    for display_name, import_name in required_modules:
        try:
            # モジュール名をそのままインポート
            if '.' in import_name:
                # サブモジュールの場合は親モジュールからインポート
                parts = import_name.split('.')
                module = __import__(import_name)
                for part in parts[1:]:
                    module = getattr(module, part)
            else:
                __import__(import_name)
            print(f"  ✅ {display_name}")
        except (ImportError, AttributeError) as e:
            print(f"  ❌ {display_name} - インストールが必要")
            issues.append(f"{display_name}がインストールされていません")
    print()
    
    # 2. テンプレートフォルダチェック
    print("📁 テンプレートフォルダチェック:")
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(parent_dir, "templates")
    
    if os.path.exists(template_dir):
        print(f"  ✅ templates/ フォルダ検出")
        
        # カテゴリフォルダチェック
        categories = ["noise", "nature", "fire", "piano", "ambient", "special"]
        template_count = 0
        
        for category in categories:
            category_path = os.path.join(template_dir, category)
            if os.path.exists(category_path):
                md_files = [f for f in os.listdir(category_path) if f.endswith('.md') and f != 'README.md']
                template_count += len(md_files)
                print(f"    ├─ {category}/ ({len(md_files)}個)")
            else:
                warnings.append(f"カテゴリフォルダ {category}/ が見つかりません")
        
        print(f"  📊 合計: {template_count}個のテンプレート")
    else:
        print(f"  ❌ templates/ フォルダが見つかりません")
        issues.append("templatesフォルダが存在しません")
    print()
    
    # 3. 出力フォルダチェック
    print("📂 作業フォルダチェック:")
    automation_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(automation_dir, "output")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"  ✅ output/ フォルダ作成")
    else:
        print(f"  ✅ output/ フォルダ存在")
    print()
    
    # 4. YouTube認証ファイルチェック
    print("🔐 YouTube API認証チェック:")
    credentials_path = os.path.join(automation_dir, "credentials.json")
    token_path = os.path.join(automation_dir, "token.json")
    
    if os.path.exists(credentials_path):
        print(f"  ✅ credentials.json 存在")
    else:
        print(f"  ⚠️  credentials.json なし")
        warnings.append("credentials.json が見つかりません（YouTube機能が使えません）")
    
    if os.path.exists(token_path):
        print(f"  ✅ token.json 存在（認証済み）")
    else:
        print(f"  ⚠️  token.json なし（初回認証が必要）")
        if os.path.exists(credentials_path):
            warnings.append("auth.bat を実行してYouTube認証を完了してください")
    print()
    
    # 5. ffmpegチェック（分割エクスポート用）
    print("🎬 ffmpegチェック:")
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"  ✅ ffmpeg インストール済み")
            print(f"     {version_line}")
        else:
            print(f"  ❌ ffmpeg が正常に動作しません")
            warnings.append("ffmpeg が正常に動作しません（4時間以上の動画生成に影響）")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print(f"  ⚠️  ffmpeg が見つかりません")
        warnings.append("ffmpeg未インストール（4時間以上の動画生成時に必要）")
    print()
    
    # 結果サマリー
    print("=" * 70)
    if issues:
        print("❌ 致命的な問題が見つかりました:")
        for issue in issues:
            print(f"  • {issue}")
        print()
        print("解決方法:")
        print("  1. setup.bat を実行してください")
        print("  2. 問題が解決しない場合は README.md を確認してください")
        print("=" * 70)
        return False
    
    elif warnings:
        print("⚠️  警告がありますが、起動は可能です:")
        for warning in warnings:
            print(f"  • {warning}")
        print()
        print("推奨対応:")
        if "credentials.json" in str(warnings):
            print("  • YouTube機能を使う場合は credentials.json を配置してください")
            print("    詳細: README.md の「YouTube API設定」を参照")
        if "auth.bat" in str(warnings):
            print("  • auth.bat を実行してYouTube認証を完了してください")
        if "ffmpeg" in str(warnings):
            print("  • 4時間以上の動画を作る場合は ffmpeg をインストールしてください")
            print("    https://ffmpeg.org/download.html")
        print("=" * 70)
        
        # 警告のみの場合は続行確認
        response = input("\n続行しますか? (y/n): ")
        if response.lower() != 'y':
            return False
    
    else:
        print("✅ すべてのチェックに合格しました！")
        print("=" * 70)
    
    print()
    return True


def main():
    # 起動前チェック
    if not check_requirements():
        print("\n終了します。")
        input("Enterキーで閉じます...")
        return
    
    print("🚀 GUIを起動中...")
    print()
    
    root = tk.Tk()
    app = ManualModeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

