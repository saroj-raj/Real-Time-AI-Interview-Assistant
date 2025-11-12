'use client';

import { useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface TranscriptDisplayProps {
  transcript: string;
  isInterim?: boolean;
  title?: string;
}

export function TranscriptDisplay({
  transcript,
  isInterim = false,
  title = 'Transcript',
}: TranscriptDisplayProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [transcript]);

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="text-lg">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div
          ref={scrollRef}
          className="h-64 overflow-y-auto rounded-md border border-gray-200 bg-gray-50 p-4"
        >
          {transcript ? (
            <p
              className={`text-sm leading-relaxed whitespace-pre-wrap ${
                isInterim ? 'text-gray-500 italic' : 'text-gray-900'
              }`}
            >
              {transcript}
            </p>
          ) : (
            <p className="text-sm text-gray-400 italic">
              Transcript will appear here...
            </p>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
