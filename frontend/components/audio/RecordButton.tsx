'use client';

import { Mic, Square } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { formatDuration } from '@/lib/utils';

interface RecordButtonProps {
  isRecording: boolean;
  duration: number;
  onStart: () => void;
  onStop: () => void;
  disabled?: boolean;
}

export function RecordButton({
  isRecording,
  duration,
  onStart,
  onStop,
  disabled = false,
}: RecordButtonProps) {
  const handleClick = () => {
    if (isRecording) {
      onStop();
    } else {
      onStart();
    }
  };

  return (
    <div className="flex flex-col items-center gap-4">
      <Button
        onClick={handleClick}
        disabled={disabled}
        className={`
          h-20 w-20 rounded-full transition-all duration-300 shadow-lg
          ${
            isRecording
              ? 'bg-red-600 hover:bg-red-700 animate-pulse'
              : 'bg-blue-600 hover:bg-blue-700'
          }
        `}
        size="icon"
        aria-label={isRecording ? 'Stop recording' : 'Start recording'}
      >
        {isRecording ? (
          <Square className="h-8 w-8 text-white fill-white" />
        ) : (
          <Mic className="h-8 w-8 text-white" />
        )}
      </Button>
      
      {isRecording && (
        <div className="flex items-center gap-2 text-sm font-medium text-gray-700">
          <div className="h-2 w-2 bg-red-600 rounded-full animate-pulse" />
          <span>{formatDuration(duration)}</span>
        </div>
      )}
      
      <p className="text-sm text-gray-600 text-center max-w-xs">
        {isRecording
          ? 'Recording... Click to stop'
          : 'Click to start recording your answer'}
      </p>
    </div>
  );
}
