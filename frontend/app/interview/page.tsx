'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Mic, MicOff, Copy, RotateCw, CheckCircle, Square } from 'lucide-react';
import { useStore } from '@/lib/store';
import { withAuth } from '@/components/auth/AuthProvider';
import { formatDuration } from '@/lib/utils';
import { useWebSocket } from '@/hooks/useWebSocket';
import { useAudioStreaming } from '@/hooks/useAudioStreaming';
import type { TranscriptSegment, QuestionAnswer, WSMessage, WSTranscriptMessage, WSQuestionDetectedMessage, WSAnswerGeneratedMessage } from '@/types';

function InterviewPage() {
  const { currentSession, transcriptSegments, addTranscriptSegment, addQuestionAnswer, updateQuestionAnswer } = useStore();
  const [isListening, setIsListening] = useState(false);
  const [duration, setDuration] = useState(0);
  const [currentQuestion, setCurrentQuestion] = useState<string>('');
  const [currentAnswer, setCurrentAnswer] = useState<string>('');
  const [currentQuestionId, setCurrentQuestionId] = useState<string>('');
  const [isPaused, setIsPaused] = useState(false);
  const router = useRouter();
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const transcriptEndRef = useRef<HTMLDivElement>(null);
  
  const { startStreaming, stopStreaming } = useAudioStreaming();

  // WebSocket connection
  const { isConnected, sendMessage, disconnect } = useWebSocket({
    url: `${process.env.NEXT_PUBLIC_API_URL?.replace('http', 'ws')}/ws/interview/${currentSession?.id || 'test'}`,
    onMessage: (message) => {
      // Cast to WSMessage for type safety
      handleWebSocketMessage(message as WSMessage);
    },
    onError: (error) => {
      console.error('WebSocket error:', error);
    },
    reconnect: isListening,
  });

  function handleWebSocketMessage(message: WSMessage) {
    console.log('WebSocket message:', message);

    switch (message.type) {
      case 'transcript': {
        const transcriptMsg = message as WSTranscriptMessage;
        const segment: TranscriptSegment = {
          id: Date.now().toString(),
          sessionId: currentSession?.id || '',
          speaker: transcriptMsg.data.speaker,
          text: transcriptMsg.data.text,
          timestamp: message.timestamp || Date.now(),
          isFinal: transcriptMsg.data.isFinal,
        };
        addTranscriptSegment(segment);
        break;
      }

      case 'question_detected': {
        const questionMsg = message as WSQuestionDetectedMessage;
        setCurrentQuestion(questionMsg.data.question);
        setCurrentAnswer('Generating answer...');
        break;
      }

      case 'answer_generated': {
        const answerMsg = message as WSAnswerGeneratedMessage;
        setCurrentAnswer(answerMsg.data.answer);
        setCurrentQuestionId(answerMsg.data.questionId);

        const qa: QuestionAnswer = {
          id: answerMsg.data.questionId,
          sessionId: currentSession?.id || '',
          question: currentQuestion,
          questionTimestamp: Date.now(),
          suggestedAnswer: answerMsg.data.answer,
          wasUsed: false,
          confidence: answerMsg.data.confidence,
          contextUsed: answerMsg.data.contextUsed,
          createdAt: new Date(),
        };
        addQuestionAnswer(qa);
        break;
      }

      case 'error': {
        console.error('Backend error:', message.data);
        break;
      }
    }
  }

  useEffect(() => {
    if (!currentSession) {
      router.push('/dashboard');
      return;
    }

    // Auto-scroll transcript to bottom
    transcriptEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [transcriptSegments, currentSession, router]);

  useEffect(() => {
    if (isListening && !isPaused) {
      timerRef.current = setInterval(() => {
        setDuration((prev) => prev + 1);
      }, 1000);
    } else {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    }
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, [isListening, isPaused]);

  const handleStartListening = useCallback(async () => {
    setIsListening(true);
    setIsPaused(false);

    // Start audio streaming
    await startStreaming((audioChunk) => {
      // Send audio chunk to backend via WebSocket
      if (isConnected) {
        audioChunk.arrayBuffer().then((buffer) => {
          sendMessage(buffer);
        });
      }
    });
  }, [startStreaming, isConnected, sendMessage]);

  const handlePause = useCallback(() => {
    setIsPaused(!isPaused);
    if (!isPaused) {
      stopStreaming();
    } else {
      handleStartListening();
    }
  }, [isPaused, stopStreaming, handleStartListening]);

  const handleStop = useCallback(() => {
    setIsListening(false);
    setIsPaused(false);
    stopStreaming();
    disconnect();
  }, [stopStreaming, disconnect]);

  const handleCopyAnswer = useCallback(() => {
    navigator.clipboard.writeText(currentAnswer);
  }, [currentAnswer]);

  const handleRegenerateAnswer = useCallback(() => {
    // Send regeneration request to backend
    sendMessage({
      type: 'regenerate_answer',
      questionId: currentQuestionId,
    });
    setCurrentAnswer('Regenerating answer...');
  }, [currentQuestionId, sendMessage]);

  const handleMarkAsUsed = useCallback(() => {
    if (currentQuestionId) {
      updateQuestionAnswer(currentQuestionId, { wasUsed: true });
    }
  }, [currentQuestionId, updateQuestionAnswer]);

  const getTimerColor = () => {
    if (duration < 300) return 'text-gray-700';
    if (duration < 900) return 'text-yellow-600';
    return 'text-red-600';
  };

  if (!currentSession) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white p-4">
      <div className="max-w-7xl mx-auto space-y-4">
        {/* Header */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-3">
            <div>
              <CardTitle className="text-lg">
                {currentSession.roleName} at {currentSession.companyName}
              </CardTitle>
              <p className="text-sm text-gray-500 mt-1">
                {isListening && !isPaused ? '🔴 LISTENING' : isPaused ? '⏸️ PAUSED' : '⏹️ STOPPED'}
              </p>
            </div>
            <div className={`text-2xl font-mono font-bold ${getTimerColor()}`}>
              {formatDuration(duration)}
            </div>
          </CardHeader>
        </Card>

        {/* Main Content */}
        <div className="grid lg:grid-cols-2 gap-4">
          {/* Left Column: Question & Answer */}
          <div className="space-y-4">
            {/* Current Question */}
            <Card>
              <CardHeader>
                <CardTitle className="text-base flex items-center gap-2">
                  👔 Recruiter Question
                </CardTitle>
              </CardHeader>
              <CardContent>
                {currentQuestion ? (
                  <p className="text-gray-800 text-lg">{currentQuestion}</p>
                ) : (
                  <p className="text-gray-400 italic">Waiting for question...</p>
                )}
              </CardContent>
            </Card>

            {/* Suggested Answer */}
            <Card className="bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-200">
              <CardHeader>
                <CardTitle className="text-base flex items-center gap-2">
                  💡 Suggested Answer
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {currentAnswer ? (
                  <>
                    <p className="text-gray-800 leading-relaxed">{currentAnswer}</p>
                    <div className="flex gap-2 flex-wrap">
                      <Button size="sm" variant="outline" onClick={handleCopyAnswer}>
                        <Copy className="h-4 w-4 mr-2" />
                        Copy
                      </Button>
                      <Button size="sm" variant="outline" onClick={handleRegenerateAnswer}>
                        <RotateCw className="h-4 w-4 mr-2" />
                        Regenerate
                      </Button>
                      <Button size="sm" variant="outline" onClick={handleMarkAsUsed}>
                        <CheckCircle className="h-4 w-4 mr-2" />
                        Mark as Used
                      </Button>
                    </div>
                  </>
                ) : (
                  <p className="text-gray-400 italic">Answer will appear here...</p>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Right Column: Transcript */}
          <Card className="lg:h-[600px] flex flex-col">
            <CardHeader>
              <CardTitle className="text-base">Live Transcript</CardTitle>
            </CardHeader>
            <CardContent className="flex-1 overflow-y-auto">
              <div className="space-y-3">
                {transcriptSegments.map((segment) => (
                  <div
                    key={segment.id}
                    className={`p-3 rounded-lg ${
                      segment.speaker === 'recruiter'
                        ? 'bg-gray-100 ml-0 mr-8'
                        : 'bg-blue-100 ml-8 mr-0'
                    }`}
                  >
                    <div className="text-xs font-semibold text-gray-600 mb-1">
                      {segment.speaker === 'recruiter' ? '👔 Recruiter' : '👤 You'}
                    </div>
                    <div className={segment.isFinal ? 'text-gray-800' : 'text-gray-500 italic'}>
                      {segment.text}
                    </div>
                  </div>
                ))}
                <div ref={transcriptEndRef} />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Controls */}
        <Card>
          <CardContent className="pt-6">
            <div className="flex justify-center gap-4">
              {!isListening ? (
                <Button size="lg" onClick={handleStartListening} className="w-48">
                  <Mic className="h-5 w-5 mr-2" />
                  Start Listening
                </Button>
              ) : (
                <>
                  <Button
                    size="lg"
                    variant="outline"
                    onClick={handlePause}
                    className="w-40"
                  >
                    {isPaused ? (
                      <>
                        <Mic className="h-5 w-5 mr-2" />
                        Resume
                      </>
                    ) : (
                      <>
                        <MicOff className="h-5 w-5 mr-2" />
                        Pause
                      </>
                    )}
                  </Button>
                  <Button
                    size="lg"
                    variant="destructive"
                    onClick={handleStop}
                    className="w-40"
                  >
                    <Square className="h-4 w-4 mr-2" />
                    Stop Interview
                  </Button>
                </>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

export default withAuth(InterviewPage);
