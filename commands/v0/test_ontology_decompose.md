以下のドメインナレッジに基づいて、タスクをPrimitiveなアクションのmarkdown todo list を出力してください。分解の途中過程もわかるように出力を

---

### 1. Primitiveなアクションのリスト

エージェントが直接実行できる、最も基本的なアクションです。

* **移動系:**
    * `move_to(場所)`: 指定された場所に移動する
* **掃除系:**
    * `wipe_surface(表面の種類, 場所)`: 指定された場所の表面を拭く（例: `wipe_surface(テーブル, リビング)`）
    * `vacuum_floor(場所)`: 指定された場所の床を掃除機でかける
    * `dust_item(アイテム, 場所)`: 指定された場所にあるアイテムのホコリを払う
* **整理整頓系:**
    * `put_item_away(アイテム, 元の場所, 収納場所)`: アイテムを元の場所から指定された収納場所に片付ける
    * `sort_laundry(種類)`: 洗濯物を種類別に仕分ける（例: `sort_laundry(色物)`）
* **設備操作系:**
    * `start_dishwasher()`: 食洗機を起動する
    * `load_laundry_machine(種類)`: 洗濯機に洗濯物を入れる
    * `start_laundry_machine(コース)`: 洗濯機を起動する（例: `start_laundry_machine(標準)`）
    * `empty_trash_can(場所)`: 指定された場所のごみ箱を空にする
* **情報取得系（センサーデータなど）:**
    * `check_item_state(アイテム)`: アイテムの状態を確認する（例: `check_item_state(食器棚の食器)`）
    * `check_room_state(部屋)`: 部屋の状態を確認する（例: `check_room_state(リビングの床)`）

---

### 2. タスクを分解するためのルール（ドメインルール）

これらのルールは、上位の抽象的なタスクを下位の具体的なアクションやサブタスクに分解する方法を定義します。オントロジーのような構造を意識し、条件に応じた分解を可能にします。

#### 2.1. 高レベルタスクの分解ルール

* **`clean_house` (家をきれいにする)**
    * **IF** 全ての部屋が汚れている
    * **THEN** `clean_room(リビング)`, `clean_room(キッチン)`, `clean_room(寝室)`, `clean_room(浴室)` を実行する
    * **IF** 食器が汚れている
    * **THEN** `do_dishes` を実行する
    * **IF** 洗濯物がある
    * **THEN** `do_laundry` を実行する

* **`clean_room(部屋)` (部屋をきれいにする)**
    * **IF** `部屋` の床が汚れている
    * **THEN** `vacuum_floor(部屋)` を実行する
    * **IF** `部屋` の表面が汚れている
    * **THEN** `wipe_surface(全ての表面, 部屋)` を実行する
    * **IF** `部屋` にホコリがたまっている
    * **THEN** `dust_room(部屋)` を実行する
    * **IF** `部屋` に散らかったものがある
    * **THEN** `tidy_room(部屋)` を実行する
    * **IF** `部屋` のごみ箱が満杯である
    * **THEN** `empty_trash_can(部屋)` を実行する

#### 2.2. 中レベルタスクの分解ルール

* **`do_dishes` (食器洗いをする)**
    * **IF** 食器がシンクに散らばっている
    * **THEN** `collect_dishes_to_sink` を実行する
    * **IF** 食洗機がある and 食器が食洗機対応
    * **THEN** `load_dishwasher`, `start_dishwasher` を実行する
    * **ELSE** `wash_dishes_manually` を実行する

* **`do_laundry` (洗濯をする)**
    * **IF** 洗濯物が汚れている
    * **THEN** `sort_laundry(全て)`, `load_laundry_machine(仕分け済み洗濯物)`, `start_laundry_machine(適切なコース)`, `dry_laundry`, `fold_laundry`, `put_away_laundry` を実行する

* **`dust_room(部屋)` (部屋のホコリを払う)**
    * **FOR EACH** `アイテム` in `部屋` が `ほこりが付着しやすい`
    * **THEN** `dust_item(アイテム, 部屋)` を実行する

* **`tidy_room(部屋)` (部屋を整理整頓する)**
    * **FOR EACH** `アイテム` in `部屋` が `あるべき場所からずれている`
    * **THEN** `put_item_away(アイテム, 部屋, アイテムの収納場所)` を実行する

