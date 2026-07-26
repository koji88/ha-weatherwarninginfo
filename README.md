# JMA Weather Warning Information

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)

Home Assistantと連携し、気象庁（JMA）が発表する気象警報・注意報を取得するためのカスタムコンポーネントです。

## 主な機能

-   **UIによる簡単設定**: Home AssistantのUIから、監視したい地域（市町村区）をコードで指定するだけで設定が完了します。
-   **センサーエンティティ**: 設定した地域の警報・注意報を監視するセンサーを作成します。
    -   **状態**: 発表されている警報・注意報の数
    -   **属性**:
        -   `area_name`: 地域の名称
        -   `warnings`: 発表されている警報・注意報のリスト
        -   `link`: 気象庁の該当地域の警報ページへのURL
        -   `last_updated`: 最終更新時刻

## 前提条件

-   Home Assistantがインストール済みであること。
-   HACS (Home Assistant Community Store) がインストール済みであること。

## インストール

### 1. HACSでのインストール (推奨)

1.  HACS > Integrations に移動します。
2.  右上の3つのドットメニューから「カスタムリポジトリ」を選択します。
3.  `リポジトリ`にこのGitHubリポジトリのURLを入力します。
4.  `カテゴリ`で「統合」を選択し、「追加」をクリックします。
5.  HACSの画面に戻り、「JMA Weather Warning Information」を検索してインストールします。
6.  Home Assistantを再起動します。

### 2. 手動でのインストール

1.  `custom_components/weatherwarninginfo` ディレクトリを、お使いのHome Assistantの `<config>/custom_components` ディレクトリにコピーします。
2.  Home Assistantを再起動します。

## 設定方法

1.  **[設定]** > **[デバイスとサービス]** に移動します。
2.  右下の **[統合を追加]** をクリックし、「**JMA Weather Warning Info**」を検索して選択します。
3.  設定ウィンドウが表示されたら、情報を取得したい地域の**エリアコード（市町村区コード）**を入力します。
    -   **エリアコードの確認方法**:
        気象庁のウェブサイトにアクセスし、目的の市町村区を選択してください。ブラウザのURLに表示される `area_code=` の後の数字がエリアコードです。
        (例: 東京都千代田区の場合、URLは `...&area_code=1310100&...` となり、エリアコードは `1310100` です)
4.  **[送信]** をクリックして設定を完了します。

## センサーの利用例

この統合は `sensor.市区町村名_の気象警報_注意報` という名前のセンサーエンティティを作成します。

### Lovelace UIでの表示例

#### Entitiesカード

```yaml
type: entities
entities:
  - entity: sensor.osaka_shi_no_kisho_keiho_chuiho
    name: 大阪市の気象警報
title: 気象情報
```

#### Markdownカード (詳細表示)

```yaml
type: markdown
content: >
  ### {{ state_attr('sensor.osaka_shi_no_kisho_keiho_chuiho', 'area_name') }}の気象情報

  **発表中の警報・注意報: {{ states('sensor.osaka_shi_no_kisho_keiho_chuiho') }}件**

  {% for warning in state_attr('sensor.osaka_shi_no_kisho_keiho_chuiho', 'warnings') %}
  - {{ warning }}
  {% else %}
  現在、発表されている警報・注意報はありません。
  {% endfor %}

  [詳細情報（気象庁）]({{ state_attr('sensor.osaka_shi_no_kisho_keiho_chuiho', 'link') }})

  最終更新: {{ state_attr('sensor.osaka_shi_no_kisho_keiho_chuiho', 'last_updated') }}
```

## 開発者向け情報

リポジトリのルートにある `test_script.py` を使用すると、Home Assistant環境外でデータ取得のテストを実行できます。

```bash
# 依存ライブラリのインストール
pip install aiohttp

# スクリプトの実行 (例: 東京都千代田区)
python test_script.py 1310100
```