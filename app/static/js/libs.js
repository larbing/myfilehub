class HttpClient {
  constructor() {
  }


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
    this.subscribers = {};
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
        // this.onMessage(message);

        if (this.subscribers["message"]) {
          this.subscribers["message"].forEach((subscriber) => {
            subscriber.onMessage(message);
          });
        }

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

  subscribe(subscriber) {
    if (!this.subscribers["message"]) {
      this.subscribers["message"] = [];
    }

    this.subscribers["message"].push(subscriber);
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