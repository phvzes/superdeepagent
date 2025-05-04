
import { useEffect, useState } from 'react';
import { io } from 'socket.io-client';

let socket;

export const initializeSocket = () => {
  if (!socket) {
    socket = io(process.env.NEXT_PUBLIC_WEBSOCKET_URL || 'http://localhost:3000');

    socket.on('connect', () => {
      console.log('WebSocket connected');
    });

    socket.on('disconnect', () => {
      console.log('WebSocket disconnected');
    });

    socket.on('error', (error) => {
      console.error('WebSocket error:', error);
    });
  }

  return socket;
};

export const useSocket = () => {
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const socketInstance = initializeSocket();

    const onConnect = () => {
      setIsConnected(true);
    };

    const onDisconnect = () => {
      setIsConnected(false);
    };

    socketInstance.on('connect', onConnect);
    socketInstance.on('disconnect', onDisconnect);

    if (socketInstance.connected) {
      setIsConnected(true);
    }

    return () => {
      socketInstance.off('connect', onConnect);
      socketInstance.off('disconnect', onDisconnect);
    };
  }, []);

  return { socket: initializeSocket(), isConnected };
};

export const useSocketEvent = (event, callback) => {
  useEffect(() => {
    const socketInstance = initializeSocket();

    socketInstance.on(event, callback);

    return () => {
      socketInstance.off(event, callback);
    };
  }, [event, callback]);
};

export const emitSocketEvent = (event, data) => {
  const socketInstance = initializeSocket();
  socketInstance.emit(event, data);
};
