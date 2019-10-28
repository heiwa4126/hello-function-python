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
  - [最初の1回](#%e6%9c%80%e5%88%9d%e3%81%ae1%e5%9b%9e)
  - [変更を加える](#%e5%a4%89%e6%9b%b4%e3%82%92%e5%8a%a0%e3%81%88%e3%82%8b)
  - [デプロイ](#%e3%83%87%e3%83%97%e3%83%ad%e3%82%a4)
- [1から作る場合](#1%e3%81%8b%e3%82%89%e4%bd%9c%e3%82%8b%e5%a0%b4%e5%90%88)
- [その他メモ](#%e3%81%9d%e3%81%ae%e4%bb%96%e3%83%a1%e3%83%a2)


# 最低限用意するもの

- Azureのサブスクリプション
- [Azure CLI](https://docs.microsoft.com/ja-jp/cli/azure/install-azure-cli)
  - pipで入れないこと。WindowsはMSI, Debian/Ubuntuはaptでレポジトリから入れること
- Node.js 10.x LTS(12.xはLTSでもAzure Functions Core Toolsが死ぬ)
- [Azure Functions Core Tools](https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-run-local#v2) 2.x
  - Windowsではnpmで入れないこと。chocolatey使うこと
- Python 3.6 (3.7以上だとAzure Functions Core Toolsが死ぬ)

# git cloneからdeployまで


## 最初の1回

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


``` bash
func azure functionapp publish <APP_NAME> --build remote
```

`--build remote`オプションをつけるとリモートビルドする。
`pip install -r requirements.txt`をリモートでやってくれるらしい。

`./.python_packages`があればこれも送信するらしい。



# 1から作る場合

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

# その他メモ

``` bash
python --verson
```
が3ならvenvはいらないのでは?

Azure Functions Core Toolsのバージョンチェックが厳しすぎ。

Pythonだと(たぶんLinuxベースだと)デプロイセンターが使えない。githubでデプロイができない。これはたぶんLinuxベースのやつ(PythonとGolang)はdockerで動いてるからなのでは。docker hub経由にするか、Windowsで動くNode.jsか.NET Coreにするか。