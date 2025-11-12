'use client';

import { useState, useRef, useCallback } from 'react';
import type { AudioRecorderState } from '@/types';

export function useAudioRecorder() {
  const [state, setState] = useState<AudioRecorderState>({
    isRecording: false,
    audioBlob: null,
    duration: 0,
    error: null,
  });

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  const startRecording = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          sampleRate: 44100,
        },
      });

      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm',
      });

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
        setState((prev) => ({ ...prev, audioBlob: blob, isRecording: false }));
        chunksRef.current = [];
        
        // Stop all tracks
        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorderRef.current = mediaRecorder;
      mediaRecorder.start(1000); // Collect data every second

      // Start duration timer
      let seconds = 0;
      timerRef.current = setInterval(() => {
        seconds++;
        setState((prev) => ({ ...prev, duration: seconds }));
      }, 1000);

      setState((prev) => ({
        ...prev,
        isRecording: true,
        audioBlob: null,
        duration: 0,
        error: null,
      }));
    } catch (error) {
      setState((prev) => ({
        ...prev,
        error: error instanceof Error ? error.message : 'Failed to start recording',
      }));
    }
  }, []);

  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current && state.isRecording) {
      mediaRecorderRef.current.stop();
      
      if (timerRef.current) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }
    }
  }, [state.isRecording]);

  const reset = useCallback(() => {
    setState({
      isRecording: false,
      audioBlob: null,
      duration: 0,
      error: null,
    });
    chunksRef.current = [];
  }, []);

  return {
    ...state,
    startRecording,
    stopRecording,
    reset,
  };
}
