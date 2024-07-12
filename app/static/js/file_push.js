
class FilePusher {

    constructor(url) {
        this.$ = function (id) {
            return document.getElementById(id);
        }

        this.localSendClient = new LocalSendClient();
        this.socket = new MyWebSocket(url);

        this.popupWindow = this.$('popupPushWindow');
        this.progress = this.$('pushProgress');
        this.pushMessage = this.$('pushMessage');
        this.deviceSelect = this.$('deviceSelect');
        this.pushFileButton = this.$('pushFileButton');
        this.closePushWindow = this.$('closePushWindow');
        this.fileId = this.$('fileId');
        this.init();
    }

    init() 
    {
        this.closePushWindow.addEventListener('click', this.closeWindowHandle.bind(this));
        this.pushFileButton.addEventListener('click', this.pushFileHandle.bind(this));

        const self = this;
        this.socket.onMessage = (message) => {
            this.updateProgress(self,message);
        }
    }

    openPushFileWindow(fileid, fileName, fileSize) {
        this.$('fileId').value = fileid;
        this.$('fileName').innerText = fileName;
        this.popupWindow.style.display = 'flex';
        this.progress.style.display = 'none';
        this.progress.value = 0;
        this.progress.max = fileSize;

        this.printMessage("等待设备推送...");
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
        this.localSendClient.push(fileId, deviceId, this.socket.socketId)
            .then(() => {
                this.printMessage("推送成功");
            })
            .catch(() => {
                this.printMessage("推送失败");
        });
    }

    printMessage(msg) {
        this.pushMessage.innerText = msg;
    }

    updateProgress(self,message) {
        try {
            if (message.name == 'PUSH_FILE_PROGRESS') {
                self.progress.value = message.values.total_bytes;
            }
        } catch (error) {
            console.error(error);
        }
    }

    getFileId() {
        return this.fileId.value;
    }

    getDeviceId() {
        return this.deviceSelect.value;
    }
}