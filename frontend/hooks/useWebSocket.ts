'use client';

import { useState, useEffect, useCallback, useRef } from 'react';

interface WebSocketMessage {
  type: string;
  data: unknown;
  timestamp?: number;
}

interface UseWebSocketOptions {
  url: string;
  onMessage?: (message: WebSocketMessage) => void;
  onOpen?: () => void;
  onClose?: () => void;
  onError?: (error: Event) => void;
  reconnect?: boolean;
  reconnectInterval?: number;
}

export function useWebSocket({
  url,
  onMessage,
  onOpen,
  onClose,
  onError,
  reconnect = true,
  reconnectInterval = 3000,
}: UseWebSocketOptions) {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const shouldReconnectRef = useRef(reconnect);

  useEffect(() => {
    shouldReconnectRef.current = reconnect;
  }, [reconnect]);

  const connect = useCallback(() => {
    try {
      const ws = new WebSocket(url);
      ws.binaryType = 'arraybuffer'; // Support binary data

      ws.onopen = () => {
        setIsConnected(true);
        onOpen?.();
      };

      ws.onmessage = (event) => {
        try {
          // Handle binary data (if backend sends audio back - not used currently)
          if (event.data instanceof ArrayBuffer) {
            console.log('Received binary data:', event.data.byteLength, 'bytes');
            return;
          }

          // Handle JSON messages
          const message = JSON.parse(event.data);
          setLastMessage(message);
          onMessage?.(message);
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error);
        }
      };

      ws.onclose = () => {
        setIsConnected(false);
        onClose?.();
        
        // Schedule reconnect using ref to avoid circular dependency
        if (shouldReconnectRef.current && reconnectTimeoutRef.current === null) {
          reconnectTimeoutRef.current = setTimeout(() => {
            reconnectTimeoutRef.current = null;
            // Reconnect by creating new WebSocket directly
            const newWs = new WebSocket(url);
            newWs.binaryType = 'arraybuffer';
            newWs.onopen = ws.onopen;
            newWs.onmessage = ws.onmessage;
            newWs.onclose = ws.onclose;
            newWs.onerror = ws.onerror;
            wsRef.current = newWs;
          }, reconnectInterval);
        }
      };

      ws.onerror = (error) => {
        onError?.(error);
      };

      wsRef.current = ws;
    } catch (error) {
      console.error('Failed to create WebSocket connection:', error);
    }
  }, [url, onMessage, onOpen, onClose, onError, reconnectInterval]);

  const disconnect = useCallback(() => {
    shouldReconnectRef.current = false;
    
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }
    
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
  }, []);

  const sendMessage = useCallback((message: unknown | ArrayBuffer) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      if (message instanceof ArrayBuffer) {
        // Send binary audio data
        wsRef.current.send(message);
      } else {
        // Send JSON message
        wsRef.current.send(JSON.stringify(message));
      }
      return true;
    }
    return false;
  }, []);

  useEffect(() => {
    connect();
    return () => {
      shouldReconnectRef.current = false;
      disconnect();
    };
  }, [connect, disconnect]);

  return {
    isConnected,
    lastMessage,
    sendMessage,
    disconnect,
  };
}
