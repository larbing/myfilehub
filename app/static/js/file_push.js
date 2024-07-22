
class FilePusher {

    constructor(websocket) {
        
        this.$ = function (id) {
            return document.getElementById(id);
        }

        this.httpClient = new HttpClient();
        this.websocket = websocket;
        this.websocket.subscribe(this);

        this.popupWindow = this.$('popupPushWindow');
        this.progress = this.$('pushProgress');
        this.pushMessage = this.$('pushMessage');
        this.pushFileButton = this.$('pushFileButton');
        this.closePushWindow = this.$('closePushWindow');
        this.fileId = this.$('fileId');
        this.deviceList = this.$('deviceList');
        
        this.init();
    }

    init() 
    {
        this.closePushWindow.addEventListener('click', this.closeWindowHandle.bind(this));
        this.pushFileButton.addEventListener('click', this.pushFileHandle.bind(this));
    }

    openPushFileWindow(fileid, fileName, fileSize) {
        this.$('fileId').value = fileid;
        this.$('fileName').innerText = fileName;
        this.popupWindow.style.display = 'flex';
        this.progress.style.display = 'none';
        this.progress.value = 0;
        this.progress.max = fileSize;
        this.printMessage("等待设备推送...");
        this.loadDeviceList();
    }

    loadDeviceList() {
        fetch('/device-list')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(text => {
            this.deviceList.innerHTML = text;
        })
    }

    closeWindowHandle(e) {
        this.popupWindow.style.display = 'none';
    }

    pushFileHandle() { 
        var deviceId = this.getDeviceId();
        var fileId = this.getFileId();

        if (deviceId == "") {
            alert("请选择设备");
            return;
        }

        if (fileId == "") {
            alert("请选择文件");
            return;
        }

        this.progress.style.display = 'flex';
        this.progress.value = 0;
        this.printMessage("正在推送...");
        this.pushFile(fileId, deviceId)
            .then(() => {
                this.printMessage("推送成功");
            })
            .catch(() => {
                this.printMessage("推送失败");
        });
    }

    onMessage(message) {
        self = this;
        try 
        {
          if (message.name == 'PUSH_FILE_PROGRESS') {
              self.updateProgress(message.values.total_bytes);
          }
        } catch (error) {
          console.error(error);
        }
    }

    async pushFile(fileId, deviceId) {
        const url = '/api/localsend/v2/push';
        const data = {
          fileId: fileId,
          deviceId: deviceId,
          socketId: this.websocket.socketId,
        };    
        const response = this.httpClient.sendPostRequest(url, data);
        response.catch((error) => {console.error(error);});
        return response;
    }

    printMessage(msg) {
        this.pushMessage.innerText = msg;
    }

    updateProgress(total_bytes) {
        this.progress.value = total_bytes;
    }

    getFileId() {
        return this.fileId.value;
    }

    getDeviceId() {
        return this.deviceList.value;
    }
}