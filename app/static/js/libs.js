class LocalSendClient {
  constructor() {
    this.socket = new MyWebSocket('ws://' + document.location.host + '/ws');
  }

  async push(fileId, deviceId,updateProgress) {
    const url = '/api/localsend/v2/push';
    const data = {
      fileId: fileId,
      deviceId: deviceId,
      socketId: this.socket.socketId,
    };

    this.socket.onMessage = (message) => {
      try 
      {
        if (message.name == 'PUSH_FILE_PROGRESS') {
            updateProgress(message.values.total_bytes);
        }
      } catch (error) {
        console.error(error);
      }
    }

    const response = this.sendPostRequest(url, data);
    response.then((text) => {
    })
      .catch((error) => {
        console.error(error);
      });

    return response;
  }

  // 标记为异步的sendPostRequest方法
  async sendPostRequest(url, data) {

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.text();
  }
}

class MyWebSocket {
  constructor(url) {
    this.url = url;
    this.ws = null;
    this.socketId = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5; // 最大重试次数
    this.connect();
  }

  connect() {
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      console.log('WebSocket connected');
      this.onOpen();
      this.reconnectAttempts = 0; // 重置重试次数
    };

    this.ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        if (message.name == 'CONNECT_SUCCESS') {
          this.socketId = message.values.socket_id;
        }
        this.onMessage(message);
      } catch (e) {
        console.error(e);
      }
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error: ', error);
      this.onError(error);
      this.reconnect(); // 尝试重连
    };

    this.ws.onclose = () => {
      console.log('WebSocket connection closed');
      this.onClose();
      this.reconnect(); // 尝试重连
    };
  }

  reconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      const timeout = Math.pow(2, this.reconnectAttempts) * 1000; // 指数退避算法
      setTimeout(() => {
        console.log(`Attempting to reconnect... Attempt ${this.reconnectAttempts + 1}`);
        this.connect();
        this.reconnectAttempts++;
      }, timeout);
    } else {
      console.error('Max reconnect attempts reached');
    }
  }

  onOpen() { }
  onMessage(message) {
    // console.log('Received data from server1: ', message);
  }
  onError(error) { }
  onClose() { }
}