// User & Authentication
export interface User {
  uid: string;
  email: string;
  displayName?: string;
  photoURL?: string;
  createdAt: Date;
}

// Resume
export interface Resume {
  id: string;
  userId: string;
  name: string; // e.g., "Senior Engineer Resume - 2024"
  fileUrl: string; // Firebase Storage URL
  parsedData: {
    skills: string[];
    experience: Array<{
      company: string;
      role: string;
      duration: string;
      description: string;
      projects?: string[];
    }>;
    education: Array<{
      institution: string;
      degree: string;
      year: string;
    }>;
    projects: Array<{
      name: string;
      description: string;
      technologies: string[];
    }>;
  };
  createdAt: Date;
  updatedAt: Date;
}

// Job Description
export interface JobDescription {
  id: string;
  userId: string;
  companyName: string;
  roleName: string;
  description: string;
  requiredSkills: string[];
  responsibilities: string[];
  url?: string;
  createdAt: Date;
  updatedAt: Date;
}

// Interview Session
export interface InterviewSession {
  id: string;
  userId: string;
  resumeId: string;
  jobDescriptionId: string;
  companyName: string;
  roleName: string;
  status: 'scheduled' | 'live' | 'completed' | 'cancelled';
  startedAt?: Date;
  endedAt?: Date;
  duration?: number; // in seconds
  outcome?: 'success' | 'rejected' | 'pending' | 'follow-up';
  notes?: string;
  isFollowUp?: boolean;
  parentSessionId?: string; // For follow-up interviews
  createdAt: Date;
  updatedAt: Date;
}

// Transcript Segment (for real-time display)
export interface TranscriptSegment {
  id: string;
  sessionId: string;
  speaker: 'recruiter' | 'user';
  text: string;
  timestamp: number;
  isFinal: boolean;
  isQuestion?: boolean; // AI-detected question
  confidence?: number;
}

// Interview Question & Answer
export interface QuestionAnswer {
  id: string;
  sessionId: string;
  question: string;
  questionTimestamp: number;
  suggestedAnswer: string;
  actualAnswer?: string; // What user actually said
  wasUsed: boolean; // Did user use the suggested answer?
  confidence: number; // AI confidence in answer quality (0-1)
  contextUsed: {
    resumeSection?: string;
    jdSection?: string;
    previousSession?: string; // Reference to follow-up context
  };
  createdAt: Date;
}

// Audio Recording
export interface AudioRecording {
  id: string;
  sessionId: string;
  fileUrl: string; // Firebase Storage URL
  duration: number;
  format: string; // 'webm', 'mp3', etc.
  hasDiarization: boolean;
  createdAt: Date;
}

// Audio Recorder State
export interface AudioRecorderState {
  isRecording: boolean;
  audioBlob: Blob | null;
  duration: number;
  error: string | null;
}

// WebSocket Message Types
export interface WSMessage {
  type: 'transcript' | 'question_detected' | 'answer_generated' | 'error';
  data: unknown;
  timestamp?: number;
}

export interface WSTranscriptMessage extends WSMessage {
  type: 'transcript';
  data: {
    text: string;
    speaker: 'recruiter' | 'user';
    isFinal: boolean;
  };
}

export interface WSQuestionDetectedMessage extends WSMessage {
  type: 'question_detected';
  data: {
    question: string;
    timestamp: number;
  };
}

export interface WSAnswerGeneratedMessage extends WSMessage {
  type: 'answer_generated';
  data: {
    questionId: string;
    answer: string;
    confidence: number;
    contextUsed: {
      resumeSection?: string;
      jdSection?: string;
    };
  };
}

// Store State (Zustand)
export interface AppState {
  // User
  user: User | null;
  setUser: (user: User | null) => void;

  // Current Session
  currentSession: InterviewSession | null;
  setCurrentSession: (session: InterviewSession | null) => void;

  // Selected Resume & JD
  selectedResume: Resume | null;
  selectedJobDescription: JobDescription | null;
  setSelectedResume: (resume: Resume | null) => void;
  setSelectedJobDescription: (jd: JobDescription | null) => void;

  // Real-time Transcript
  transcriptSegments: TranscriptSegment[];
  addTranscriptSegment: (segment: TranscriptSegment) => void;
  clearTranscript: () => void;

  // Questions & Answers
  questionsAnswers: QuestionAnswer[];
  addQuestionAnswer: (qa: QuestionAnswer) => void;
  updateQuestionAnswer: (id: string, updates: Partial<QuestionAnswer>) => void;
}

// Legacy interfaces (for backward compatibility)
export interface InterviewQuestion {
  id: string;
  number: number;
  question: string;
  answer: string;
  timestamp: Date;
  responseTime: number;
}

export interface Session {
  id: string;
  userId: string;
  profileId: string;
  jobDescription: string;
  status: 'active' | 'completed' | 'abandoned';
  createdAt: Date;
  completedAt: Date | null;
  duration: number;
  questions: InterviewQuestion[];
}
