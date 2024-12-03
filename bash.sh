wget -O vscode-server.tar.gz https://update.code.visualstudio.com/latest/server-linux-x64/stable
tar -xzf vscode-server.tar.gz
./server/bin/code-server --host 0.0.0.0 --port 8080
