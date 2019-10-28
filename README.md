# hello-function-python

pythonでAzure Functions。
EAST Japanでもpythonが使えるようになっていたので(2019-10)
手順のまとめ。

コードの中身は
[Azure で HTTP によってトリガーされる関数を作成する | Microsoft Docs](https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-create-first-function-python)
と同じ。


# git cloneからdeployまで

## 最低限用意するもの

- Azureのサブスクリプション
- [Azure CLI](https://docs.microsoft.com/ja-jp/cli/azure/install-azure-cli)
  - pipで入れないこと。WindowsはMSI, Debian/Ubuntuはaptでレポジトリから入れること
- Node.js 10.x (12.xはLTSでも今はダメ)
- [Azure Functions Core Tools](https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-run-local#v2) 2.x
  - Windowsではnpmで入れないこと。chocolatey使うこと
- Python 3.6以上

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

```
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
