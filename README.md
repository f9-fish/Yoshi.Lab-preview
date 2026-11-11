# Yoshi.Lab-preview — AI教材スタジオ（公開無効）

`f9-fish/Yoshi.Lab` の `feature/ai-material-studio-foundation`、コミット `1eb335152213df3b47f254a406a2e86f83c3497f` の画面から作成した、独立したプレビューです。本番アプリ・main・教材JSONを変更しません。

## 公開予定URL

https://f9-fish.github.io/Yoshi.Lab-preview/teacher-studio.html

公開済みとは限りません。GitHub Pagesの成功したデプロイを確認してください。リポジトリは公開を想定します。noindexは検索エンジン向けの依頼であり、アクセス制限ではありません。

## 安全のための変更

- `/generate` だけを呼び出します。公開ボタン・公開処理・`/preview` 呼び出しは含みません。
- API接続先は `https://studioapi-bfaa4wjjga-an.a.run.app`。
- 本番の `account.js` を読み込みません。`preview-auth.js` は確認済みGoogleログインと、本人の `teacherUids/{uid}` の読み取りだけを行います。サーバーでも教員権限が検証されます。
- 生徒プロフィール・学習履歴・XP・ランキング・最終アクセスにはアクセスしません。
- 下書きは `yoshilab.preview.studio.draft.v1:{uid}` のキーでlocalStorageへ保存します。本番の下書きとは別キーです。自動バックアップ・端末間共有はありません。同じ端末のブラウザに残るため共有端末ではサイトデータを削除してください。
- Firebaseアプリ名は `yoshilab-studio-preview`、認証保持はブラウザセッション単位。本番と別の認証インスタンスを使用します。
- APIキーは既存のFirebase公開Web設定です。Geminiキー・GitHubトークンなどの秘密情報は含みません。
- 画面からの誤公開を防ぐ構成です。デプロイ済みAPI自体の `/publish` の権限を無効化するものではありません。
- 同じGitHub Pagesホストでは本番と同一Originです。リポジトリを分けてもOriginのセキュリティ境界にはなりません。

## GitHub設定（プレビュー用リポジトリのみ）

1. `f9-fish/Yoshi.Lab-preview` を作成する。既存なら内容を確認し、上書きせず専用ブランチで提案する。
2. このフォルダの内容を配置し、GitHubへ送信する。
3. 当該リポジトリの Settings → Pages → Build and deployment で `Deploy from a branch`、配信ブランチ、`/(root)` を選択する。
4. Pagesの配信成功を確認し、上記URLへアクセスする。

元リポジトリのPages設定・main・PR #66は変更しません。APIキーやサーバーSecretsをPagesの設定に登録する必要はありません。

## Firebase／APIの確認項目（勝手に変更しない）

- Authentication → Settings → Authorized domains に `f9-fish.github.io` があること。パス `/Yoshi.Lab-preview` は登録しません。
- `studioApi` の `STUDIO_ALLOWED_ORIGINS` に `https://f9-fish.github.io` が含まれること。本番PagesとOriginは同じなので通常追加不要ですが、稼働設定は未確認です。
- 利用者の教員権限が既存の `teacherUids/{uid}` に登録済みであること。未登録なら既存の管理手順で対応してください。
- 不足があれば管理者が内容を確認してから設定する。本構成のためにRulesやFunctionsを変更・再デプロイしない。

本APIへの実生成はGemini利用料金と、サーバー側 `studioQuota/{uid}/generate` の利用回数更新を伴います。確認したブランチでは上限は教員あたり1時間5回ですが、稼働設定・稼働コードの一致は未確認です。本文はAIへ送信されるため、テストには個人情報を含まないオリジナル英文を使ってください。

## ローカル確認

```sh
python -m http.server 8080
```

http://localhost:8080/teacher-studio.html を開きます。実認証にはFirebaseでそのホストが承認されている必要があり、APIのCORS設定にも依存します。外部設定がなくても以下のモックテストは実行できます。

```sh
node --test --test-isolation=none tests/preview.test.cjs
python tests/preview-browser.py
```

ブラウザーテストにはPython Playwrightと `/usr/bin/chromium` が必要です。テストは全リクエストを捕捉し、Firebase・API・Geminiへの通信を行いません。

## 公開後に管理者が確認する操作

1. Googleログイン前は編集フォームを操作できない。
2. 登録済み教員でログインするとフォームが表示される。生徒アカウントは拒否される。
3. テスト英文で5種類の問題を生成する。Networkには当該APIの `/generate` だけがある。
4. 問題文・正解・日本語訳・採用チェックを編集する。
5. 下書きを保存してページを再読み込みし、再ログイン後に復元する。
6. ログアウトで本文と問題が画面から消える。
7. 公開ボタンがなく、`/publish`・`/preview` への通信がない。

## 未確認事項

実Googleログイン、稼働中の教員権限・Rules、CORS、API・Geminiの実生成、GitHub Pages実配信はローカルテストとは別に確認が必要です。本番Firebaseへテスト接続していません。
