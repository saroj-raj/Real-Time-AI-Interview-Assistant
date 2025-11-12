'use client';

import { Clock } from 'lucide-react';
import { formatDuration } from '@/lib/utils';

interface TimerProps {
  seconds: number;
  warningAt?: number;
  dangerAt?: number;
}

export function Timer({
  seconds,
  warningAt = 120, // 2 minutes
  dangerAt = 180, // 3 minutes
}: TimerProps) {
  const getColorClass = () => {
    if (seconds >= dangerAt) return 'text-red-600';
    if (seconds >= warningAt) return 'text-yellow-600';
    return 'text-gray-700';
  };

  return (
    <div className={`flex items-center gap-2 font-mono text-lg ${getColorClass()}`}>
      <Clock className="h-5 w-5" />
      <span>{formatDuration(seconds)}</span>
    </div>
  );
}
