# hello-function-python

pythonでAzure Functions。
EAST Japanでもpythonが使えるようになっていたので(2019-10)
手順のまとめ。

コードの中身は
[Azure で HTTP によってトリガーされる関数を作成する | Microsoft Docs](https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-create-first-function-python)
と同じ。URLに`name=`つきで呼ぶと、`hello, name`が帰ってくる、テンプレートそのままのもの。

- [hello-function-python](#hello-function-python)
- [最低限用意するもの](#%e6%9c%80%e4%bd%8e%e9%99%90%e7%94%a8%e6%84%8f%e3%81%99%e3%82%8b%e3%82%82%e3%81%ae)
- [git cloneからdeployまで](#git-clone%e3%81%8b%e3%82%89deploy%e3%81%be%e3%81%a7)
  - [準備](#%e6%ba%96%e5%82%99)
  - [変更を加える](#%e5%a4%89%e6%9b%b4%e3%82%92%e5%8a%a0%e3%81%88%e3%82%8b)
  - [デプロイ](#%e3%83%87%e3%83%97%e3%83%ad%e3%82%a4)
- [1から作る場合](#1%e3%81%8b%e3%82%89%e4%bd%9c%e3%82%8b%e5%a0%b4%e5%90%88)
- [メモ](#%e3%83%a1%e3%83%a2)


# 最低限用意するもの

- Azureのサブスクリプション
- [Azure CLI](https://docs.microsoft.com/ja-jp/cli/azure/install-azure-cli)
  - pipで入れないこと。WindowsはMSI, Debian/Ubuntuはaptでレポジトリから入れること
- Node.js 10.x LTS(12.xはLTSでもAzure Functions Core Toolsが死ぬ)
- [Azure Functions Core Tools](https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-run-local#v2) 2.x
  - Windowsではnpmで入れないこと。chocolatey使うこと
- Python 3.6 (3.7以上だとAzure Functions Core Toolsが警告吐いて死ぬ)

↑バージョン云々は
```
$ func -v
2.7.1724
```
での話。2019-10-29に
[Release 2.7.1812 · Azure/azure-functions-core-tools](https://github.com/Azure/azure-functions-core-tools/releases/tag/2.7.1812)
が出てるので、Python 3.7については使えるようになってるかも(未確認)。


# git cloneからdeployまで

## 準備

最初の1回だけ行う

``` bash
git clone https://github.com/heiwa4126/hello-function-python.git
cd hello-function-python
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

[Azureポータル](https://portal.azure.com/)でfunction作る。
Insightはあってもなくてもいいようだが、あったほうがいいと思う。

local.settings.jsonに設定をダウンロード
```
func azure functionapp fetch-app-settings <APP_NAME>
```

## 変更を加える

``` bash
cd hello-function-python
source .env/bin/activate
```

変更作業

ローカルにホスト起動してデバッグ
``` bash
func host start
```

curlやブラウザでデバックなどなど。



## デプロイ

AWS Lamdaのように「ポータルからZIPでデプロイ」というのがない。

Azure Functions Core Tools(と Azure CLI)がインストールされている場合は:

``` bash
func azure functionapp publish <APP_NAME> --build remote
```
デプロイ(zip プッシュ デプロイ)。

`--build remote`オプションをつけるとリモートビルドする。
`pip install -r requirements.txt`をリモートでやってくれるらしい。

`./.python_packages`があればこれも送信するらしい。


Azure CLIなら
``` 
az functionapp deployment source config-zip -g <functionのリソースグループ> -n <function名> --src <zipfile名>
```
で。


デプロイに関しては
- [Azure Functions のデプロイ テクノロジ | Microsoft Docs](https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-deployment-technologies)
- [Azure Functions の継続的なデプロイ | Microsoft Docs](https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-continuous-deployment)
- [Azure Functions の zip プッシュ デプロイ | Microsoft Docs](https://docs.microsoft.com/ja-jp/azure/azure-functions/deployment-zip-push)

を参照。

# 1から作る場合

作業ディレクトリに移動してから

``` bash
func init hello-function-python
cd hello-function-python
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
func new --template "Http Trigger" --name HttpTrigger1
git init
git add --all
git commit -am 'Initial commit'
```

これでだいたい同じものができる。

# メモ

``` bash
python --verson
```
が3ならvenvはいらないのでは? - そうでもなかった。今は3.6のみ。3.7ダメ

Azure Functions Core Toolsのバージョンチェックが厳しすぎ。

Pythonだと(たぶんLinuxベースだと)デプロイセンターが使えない。githubでデプロイができない。
これはたぶんLinuxベースのやつ(PythonとGolang)はdockerで動いてるからなのでは? docker hub経由にするか、Windowsで動くNode.jsか.NET Coreにするか。

Pythonだと
[Premium](https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-scale#premium-plan)プラン
か
[専用 (App Service)](https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-scale#app-service-plan)プラン
でしか動かない。意図的に停止しない限りウォーム状態で課金される。

[Azure Functions のスケールとホスティング | Microsoft Docs](https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-scale#premium-plan)
> 少なくとも 1 つのインスタンスが常にウォーム状態である必要があります。 つまり、実行数に関係なく、アクティブなプランごとに固定の月額コストがかかります
