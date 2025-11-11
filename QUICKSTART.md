# Quick Start Guide - Phase 1: Frontend Development

## 🎯 Current Phase: Mobile-First Frontend

We're building a Next.js mobile-first web application to replace the CLI interface. This guide will help you get started with Phase 1 development.

---

## 📋 Prerequisites

Before starting, ensure you have:

### Required
- **Node.js**: v18.17 or higher ([Download](https://nodejs.org/))
- **pnpm**: v8.0 or higher (recommended) or npm/yarn
  ```bash
  npm install -g pnpm
  ```
- **Git**: For version control
- **VS Code**: Recommended editor with extensions:
  - ESLint
  - Prettier
  - Tailwind CSS IntelliSense
  - TypeScript and JavaScript Language Features

### Optional (for full stack)
- **Python**: 3.11+ (for backend development)
- **Docker**: For containerization
- **Firebase CLI**: For Firebase integration

---

## 🚀 Phase 1.1: Project Setup

### Step 1: Create Next.js Project

```bash
# Navigate to project root
cd Real-Time-AI-Interview-Assistant

# Create frontend directory
npx create-next-app@latest frontend

# Follow prompts:
# ✔ Would you like to use TypeScript? … Yes
# ✔ Would you like to use ESLint? … Yes
# ✔ Would you like to use Tailwind CSS? … Yes
# ✔ Would you like to use `src/` directory? … No
# ✔ Would you like to use App Router? … Yes
# ✔ Would you like to customize the default import alias (@/*)? … No

cd frontend
```

### Step 2: Install Dependencies

```bash
# UI Components (Shadcn)
pnpm add -D @shadcn/ui
npx shadcn-ui@latest init

# State Management
pnpm add zustand

# Forms
pnpm add react-hook-form zod @hookform/resolvers

# API Client
pnpm add axios

# Audio
pnpm add recordrtc

# Utilities
pnpm add clsx tailwind-merge class-variance-authority
pnpm add lucide-react # Icons
pnpm add date-fns # Date utilities

# Development
pnpm add -D @types/node @types/react @types/react-dom
pnpm add -D prettier prettier-plugin-tailwindcss
pnpm add -D eslint-config-prettier
```

### Step 3: Project Structure

```bash
# Create directories
mkdir -p app/\(auth\)/login
mkdir -p app/\(auth\)/signup
mkdir -p app/\(dashboard\)/interview
mkdir -p app/\(dashboard\)/history
mkdir -p app/\(dashboard\)/settings
mkdir -p components/ui
mkdir -p components/audio
mkdir -p components/interview
mkdir -p components/session
mkdir -p components/layout
mkdir -p hooks
mkdir -p lib
mkdir -p types
```

### Step 4: Configure Tailwind (Mobile-First)

Edit `tailwind.config.ts`:

```typescript
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      screens: {
        'xs': '375px',
        'sm': '640px',
        'md': '768px',
        'lg': '1024px',
        'xl': '1280px',
        '2xl': '1536px',
      },
      colors: {
        primary: {
          50: '#f0f9ff',
          // ... add your color palette
        },
      },
    },
  },
  plugins: [],
}
export default config
```

### Step 5: ESLint & Prettier Setup

Create `.prettierrc.json`:

```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "tabWidth": 2,
  "useTabs": false,
  "printWidth": 80,
  "plugins": ["prettier-plugin-tailwindcss"]
}
```

Update `.eslintrc.json`:

```json
{
  "extends": [
    "next/core-web-vitals",
    "prettier"
  ],
  "rules": {
    "react/no-unescaped-entities": "off",
    "@next/next/no-html-link-for-pages": "off"
  }
}
```

---

## 🎨 Phase 1.2: Core UI Components

### Component 1: RecordButton

Create `components/audio/RecordButton.tsx`:

```typescript
'use client';

import { useState } from 'react';
import { Mic, Square } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface RecordButtonProps {
  onRecordStart: () => void;
  onRecordStop: () => void;
  disabled?: boolean;
}

export function RecordButton({
  onRecordStart,
  onRecordStop,
  disabled = false,
}: RecordButtonProps) {
  const [isRecording, setIsRecording] = useState(false);

  const handleClick = () => {
    if (isRecording) {
      onRecordStop();
      setIsRecording(false);
    } else {
      onRecordStart();
      setIsRecording(true);
    }
  };

  return (
    <Button
      onClick={handleClick}
      disabled={disabled}
      className={`
        h-16 w-16 rounded-full transition-all
        ${isRecording
          ? 'bg-red-500 hover:bg-red-600 animate-pulse'
          : 'bg-blue-500 hover:bg-blue-600'
        }
      `}
      size="lg"
    >
      {isRecording ? (
        <Square className="h-6 w-6 text-white" />
      ) : (
        <Mic className="h-6 w-6 text-white" />
      )}
    </Button>
  );
}
```

### Component 2: TranscriptDisplay

Create `components/interview/TranscriptDisplay.tsx`:

```typescript
'use client';

import { useEffect, useRef } from 'react';
import { Card } from '@/components/ui/card';

interface TranscriptDisplayProps {
  transcript: string;
  isInterim?: boolean;
}

export function TranscriptDisplay({
  transcript,
  isInterim = false,
}: TranscriptDisplayProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [transcript]);

  return (
    <Card className="p-4 h-64 overflow-y-auto" ref={scrollRef}>
      <p className={`text-sm ${isInterim ? 'text-gray-500 italic' : 'text-gray-900'}`}>
        {transcript || 'Press the mic button to start recording...'}
      </p>
    </Card>
  );
}
```

### Component 3: useAudioRecorder Hook

Create `hooks/useAudioRecorder.ts`:

```typescript
'use client';

import { useState, useRef, useCallback } from 'react';

export function useAudioRecorder() {
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  const startRecording = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
        setAudioBlob(blob);
        chunksRef.current = [];
      };

      mediaRecorderRef.current = mediaRecorder;
      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Error starting recording:', error);
    }
  }, []);

  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
      setIsRecording(false);
    }
  }, [isRecording]);

  return {
    isRecording,
    audioBlob,
    startRecording,
    stopRecording,
  };
}
```

---

## 🧪 Testing Your Setup

### Run Development Server

```bash
cd frontend
pnpm dev
```

Visit `http://localhost:3000` to see your app.

### Test Responsive Design

1. Open Chrome DevTools (F12)
2. Click Device Toolbar (Ctrl+Shift+M)
3. Test on:
   - iPhone SE (375px)
   - iPhone 12 Pro (390px)
   - iPad (768px)
   - Desktop (1024px+)

### Lighthouse Audit

1. Open Chrome DevTools
2. Go to Lighthouse tab
3. Select "Mobile"
4. Click "Generate report"
5. Target: >90 performance score

---

## 📝 Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feat/record-button
```

### 2. Develop Component

Follow component structure:
- Create component in `components/[category]/`
- Write TypeScript types
- Style with Tailwind (mobile-first)
- Export from index.ts

### 3. Test Locally

```bash
pnpm dev
```

### 4. Lint & Format

```bash
pnpm lint
pnpm format
```

### 5. Commit Changes

```bash
git add .
git commit -m "feat: Add record button component"
```

### 6. Push & Create PR

```bash
git push origin feat/record-button
```

---

## 🎯 Phase 1 Checklist

### Week 1: Setup ✅
- [ ] Create Next.js project
- [ ] Install dependencies
- [ ] Configure Tailwind
- [ ] Set up project structure
- [ ] Configure ESLint/Prettier

### Week 2: Core Components
- [ ] RecordButton component
- [ ] TranscriptDisplay component
- [ ] Timer component
- [ ] useAudioRecorder hook
- [ ] Test on mobile devices

### Week 3: Interview UI
- [ ] QuestionCard component
- [ ] ResponseStreaming component
- [ ] SessionSummary component
- [ ] Mobile layout optimization

### Week 4: Polish & Integration
- [ ] WebSocket client
- [ ] API client setup
- [ ] Error boundaries
- [ ] Loading states
- [ ] Responsive testing

---

## 🐛 Common Issues

### Issue: "Module not found"
**Solution**: Ensure all imports use `@/` alias:
```typescript
import { Button } from '@/components/ui/button';
```

### Issue: Tailwind classes not working
**Solution**: Check `tailwind.config.ts` content paths include your files.

### Issue: Audio recording fails
**Solution**: Ensure HTTPS (localhost is ok) and microphone permissions granted.

### Issue: Next.js hydration errors
**Solution**: Use `'use client'` directive for components with browser APIs.

---

## 📚 Resources

### Next.js
- [Next.js Documentation](https://nextjs.org/docs)
- [App Router Guide](https://nextjs.org/docs/app)
- [TypeScript Guide](https://nextjs.org/docs/basic-features/typescript)

### Tailwind CSS
- [Tailwind Documentation](https://tailwindcss.com/docs)
- [Mobile-First Design](https://tailwindcss.com/docs/responsive-design)
- [Utility-First CSS](https://tailwindcss.com/docs/utility-first)

### Shadcn UI
- [Component Library](https://ui.shadcn.com/)
- [Installation Guide](https://ui.shadcn.com/docs/installation/next)
- [Theming](https://ui.shadcn.com/docs/theming)

### Web Audio
- [MediaRecorder API](https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder)
- [Web Audio API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)
- [getUserMedia](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia)

---

## 🤝 Getting Help

- **Documentation Issues**: Open issue on GitHub
- **Development Questions**: Check [RULES.md](../RULES.md)
- **Architecture Questions**: See [ARCHITECTURE.md](../ARCHITECTURE.md)
- **Roadmap Clarification**: Review [ROADMAP.md](../ROADMAP.md)

---

## 🎉 Next Steps

Once Phase 1.1-1.2 is complete:

1. **Phase 1.3**: Real-time transcription interface
2. **Phase 1.4**: Audio device detection
3. **Phase 1.5**: Backend API integration

See [ROADMAP.md](../ROADMAP.md) for full plan.

---

**Ready to start?** Jump to Step 1 and create your Next.js project! 🚀
