# TAIRYOKU (体力) — Website

Fukuoka-based creative team **TAIRYOKU (体力)** official archive & portfolio website.

## 構成ファイル
- `index.html` — トップページ（全83フレームの一面敷き詰めウォール / ドリフト / スキャッター / HTMLテーブル）
- `works.html` / `exhibitions.html` / `about.html` / `creators.html` / `contact.html` — 各セクションページ
- `works/*.html` / `exhibitions/*.html` / `commissions/*.html` — 各作品・展示の個別ページ（全18ページ）
- `styles.css` — スタイルシート（紫〜青の単色インク・素のHTML風UI）
- `app.js` — インタラクション＆キネティック制御
- `assets/` — 画像・ロゴアセット一式
- `site_data.json` & `build_site.py` — 作品データ管理＆HTML一括生成スクリプト
- `vercel.json` — Vercel ホスティング設定（Clean URLs・画像キャッシュ最適化）

## ローカルでの確認方法
1. `index.html` をそのままブラウザで開く
2. またはローカルサーバーを起動して確認：
   ```bash
   python3 -m http.server 8000
   ```
   ブラウザで `http://localhost:8000` を開きます。

## 作品・展示データの追加・更新方法
1. `assets/` 内に新しい画像を追加
2. `site_data.json` に作品データまたは展示データを追記
3. 以下のコマンドで全HTMLページを再生成：
   ```bash
   python3 build_site.py
   ```

## Vercel への公開 & 独自ドメイン (`tairyoku.jp`) 設定手順
1. このフォルダを GitHub リポジトリに Push する
2. [Vercel](https://vercel.com/) で **Add New... → Project** から該当リポジトリを選択
3. Framework Preset は **Other**（ビルドコマンド不要・そのまま静的配信）のまま **Deploy** をクリックします。
4. デプロイ後、Vercel の **Project → Settings → Domains** から `tairyoku.jp` と `www.tairyoku.jp` を追加し、表示される DNS レコード（A / CNAME または Vercel Nameservers）をドメイン管理画面に設定します。
5. 本リポジトリ内の `canonical` / OGP / `sitemap.xml` / `robots.txt` は `https://tairyoku.jp` 前提で `build_site.py` から生成されています。
