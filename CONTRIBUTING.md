# Contributing to Real-Time AI Interview Assistant

Thank you for your interest in contributing! This guide will help you get started with the project and understand our development process.

## 📚 Before You Start

Please read these documents first:

1. **[ROADMAP.md](ROADMAP.md)** - Understand the project phases and current priorities
2. **[RULES.md](RULES.md)** - Development guidelines and best practices
3. **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design and technical architecture
4. **[QUICKSTART.md](QUICKSTART.md)** - Setup guide for Phase 1 development

## 🎯 Current Development Focus

**We are currently in Phase 1: Mobile-First Frontend Development**

Priority areas:
- Next.js 14 setup with TypeScript
- Shadcn UI component library integration
- Mobile-responsive audio recording components
- Real-time WebSocket client implementation
- Audio device detection and management

See [ROADMAP.md Phase 1](ROADMAP.md#phase-1-frontend-development-mobile-first-design) for detailed tasks.

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub first, then:
git clone https://github.com/YOUR_USERNAME/Real-Time-AI-Interview-Assistant.git
cd Real-Time-AI-Interview-Assistant

# Add upstream remote
git remote add upstream https://github.com/saroj-raj/Real-Time-AI-Interview-Assistant.git
```

### 2. Set Up Development Environment

Follow [QUICKSTART.md](QUICKSTART.md) for detailed setup instructions.

#### Frontend (Phase 1)
```bash
cd frontend
pnpm install
pnpm dev
```

#### Backend (Future phases)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3. Create a Branch

```bash
# Update your fork
git fetch upstream
git checkout master
git merge upstream/master

# Create feature branch
git checkout -b feat/your-feature-name
```

#### Branch Naming Convention

- `feat/` - New features (e.g., `feat/record-button`)
- `fix/` - Bug fixes (e.g., `fix/audio-device-detection`)
- `docs/` - Documentation updates (e.g., `docs/api-reference`)
- `refactor/` - Code refactoring (e.g., `refactor/websocket-manager`)
- `test/` - Adding tests (e.g., `test/audio-recorder-hook`)
- `chore/` - Maintenance tasks (e.g., `chore/update-dependencies`)

## 💻 Development Workflow

### 1. Pick an Issue

- Check [GitHub Issues](https://github.com/saroj-raj/Real-Time-AI-Interview-Assistant/issues)
- Look for issues labeled `good first issue` or `help wanted`
- Comment on the issue to let others know you're working on it

### 2. Write Code

Follow guidelines in [RULES.md](RULES.md):

#### Code Quality
- Write clean, self-documenting code
- Add comments for complex logic
- Follow naming conventions (camelCase for TypeScript, snake_case for Python)
- Keep functions small and focused (max 50 lines)

#### Frontend (TypeScript/React)
```typescript
// Good: Descriptive naming, TypeScript types, mobile-first
'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';

interface RecordButtonProps {
  onStart: () => void;
  onStop: () => void;
  disabled?: boolean;
}

export function RecordButton({ onStart, onStop, disabled = false }: RecordButtonProps) {
  const [isRecording, setIsRecording] = useState(false);

  const handleClick = () => {
    if (isRecording) {
      onStop();
      setIsRecording(false);
    } else {
      onStart();
      setIsRecording(true);
    }
  };

  return (
    <Button
      onClick={handleClick}
      disabled={disabled}
      className="h-16 w-16 rounded-full md:h-12 md:w-12"
    >
      {isRecording ? 'Stop' : 'Record'}
    </Button>
  );
}
```

#### Backend (Python/FastAPI)
```python
# Good: Type hints, docstrings, async, error handling
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

router = APIRouter()

class SessionCreate(BaseModel):
    """Request model for creating a new interview session."""
    user_id: str
    profile_id: str
    job_description: str

@router.post("/sessions")
async def create_session(
    session: SessionCreate,
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Create a new interview session.
    
    Args:
        session: Session creation data
        current_user: Authenticated user from JWT
        
    Returns:
        Created session with ID
        
    Raises:
        HTTPException: If validation fails
    """
    try:
        session_id = await session_service.create(session)
        return {"session_id": session_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

### 3. Test Your Changes

#### Frontend Testing
```bash
# Run development server
pnpm dev

# Lint
pnpm lint

# Format
pnpm format

# Type check
pnpm type-check

# Run tests (when available)
pnpm test
```

#### Backend Testing
```bash
# Run tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Lint
flake8 app/
black app/ --check
mypy app/
```

#### Manual Testing Checklist
- [ ] Test on mobile (375px width)
- [ ] Test on tablet (768px)
- [ ] Test on desktop (1024px+)
- [ ] Test keyboard navigation
- [ ] Test screen reader (VoiceOver/NVDA)
- [ ] Test in Chrome, Firefox, Safari
- [ ] Check Lighthouse score (target >90)

### 4. Commit Your Changes

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```bash
git add .
git commit -m "feat: add audio recording component

- Create RecordButton component with start/stop functionality
- Add useAudioRecorder hook for media recording
- Implement mobile-first responsive design
- Add visual feedback for recording state

Closes #42"
```

#### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(audio): add device selection dropdown
fix(websocket): resolve connection timeout issue
docs(api): update endpoint documentation
refactor(llm): extract prompt builder to separate module
test(session): add unit tests for session manager
```

### 5. Push and Create PR

```bash
# Push to your fork
git push origin feat/your-feature-name

# Go to GitHub and create a Pull Request
```

## 📝 Pull Request Guidelines

### PR Title
Follow the same convention as commit messages:
```
feat(audio): Add recording button component
```

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update
- [ ] Refactoring
- [ ] Performance improvement

## Related Issue
Closes #42

## Changes Made
- Added RecordButton component
- Implemented useAudioRecorder hook
- Added mobile-responsive styling
- Wrote unit tests

## Testing
- [x] Tested on mobile (iPhone 12)
- [x] Tested on desktop (Chrome, Firefox)
- [x] All tests pass
- [x] Lighthouse score >90

## Screenshots
[Add screenshots for UI changes]

## Checklist
- [x] Code follows project guidelines (RULES.md)
- [x] Self-review completed
- [x] Comments added for complex logic
- [x] Documentation updated
- [x] No console errors or warnings
- [x] Tests added/updated
- [x] All tests pass
```

### Review Process

1. **Automated Checks**: CI/CD will run linting, tests, and builds
2. **Code Review**: Maintainer will review your code
3. **Feedback**: Address any requested changes
4. **Approval**: Once approved, your PR will be merged

### After Merge

```bash
# Update your local master
git checkout master
git pull upstream master

# Delete feature branch
git branch -d feat/your-feature-name
```

## 🎨 Design Guidelines

### Mobile-First Approach

Always design for mobile first, then scale up:

```css
/* Mobile (default) */
.button {
  @apply h-16 w-16 text-sm;
}

/* Tablet */
@media (min-width: 768px) {
  .button {
    @apply h-14 w-14 text-base;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .button {
    @apply h-12 w-12 text-lg;
  }
}
```

### Component Structure

```
ComponentName/
├── ComponentName.tsx      # Main component
├── ComponentName.test.tsx # Tests
├── ComponentName.stories.tsx # Storybook (future)
├── types.ts              # TypeScript types
└── index.ts              # Exports
```

### Accessibility (WCAG 2.1 AA)

- **Keyboard Navigation**: All interactive elements accessible via Tab
- **Screen Readers**: Use semantic HTML and ARIA labels
- **Color Contrast**: Minimum 4.5:1 for text
- **Touch Targets**: Minimum 44x44px on mobile
- **Focus Indicators**: Visible focus states

Example:
```typescript
<button
  onClick={handleClick}
  aria-label="Start recording"
  className="focus:ring-2 focus:ring-blue-500"
>
  <Mic aria-hidden="true" />
</button>
```

## 🧪 Testing Standards

### Frontend Tests

```typescript
// RecordButton.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { RecordButton } from './RecordButton';

describe('RecordButton', () => {
  it('calls onStart when clicked while not recording', () => {
    const onStart = jest.fn();
    const onStop = jest.fn();
    
    render(<RecordButton onStart={onStart} onStop={onStop} />);
    
    fireEvent.click(screen.getByRole('button'));
    
    expect(onStart).toHaveBeenCalledTimes(1);
    expect(onStop).not.toHaveBeenCalled();
  });

  it('calls onStop when clicked while recording', () => {
    // Test implementation
  });

  it('is disabled when disabled prop is true', () => {
    // Test implementation
  });
});
```

### Backend Tests

```python
# test_sessions.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_session(client: AsyncClient, auth_headers: dict):
    """Test creating a new session."""
    response = await client.post(
        "/api/v1/sessions",
        json={
            "user_id": "test_user",
            "profile_id": "test_profile",
            "job_description": "Software Engineer role"
        },
        headers=auth_headers
    )
    
    assert response.status_code == 201
    assert "session_id" in response.json()
```

## 🐛 Reporting Bugs

### Before Reporting

1. Check [existing issues](https://github.com/saroj-raj/Real-Time-AI-Interview-Assistant/issues)
2. Test on latest version
3. Try to reproduce consistently

### Bug Report Template

```markdown
**Describe the bug**
Clear description of the bug

**To Reproduce**
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What should happen

**Screenshots**
If applicable

**Environment:**
- OS: [e.g., Windows 11, macOS 14]
- Browser: [e.g., Chrome 120, Safari 17]
- Device: [e.g., iPhone 12, Desktop]
- Version: [e.g., 1.2.0]

**Additional context**
Any other relevant information
```

## 💡 Suggesting Features

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
Describe the problem

**Describe the solution you'd like**
Clear description of the feature

**Describe alternatives you've considered**
Other approaches considered

**Additional context**
Screenshots, mockups, etc.

**Implementation notes (optional)**
Technical suggestions
```

## 📞 Communication

- **GitHub Issues**: Bug reports, feature requests
- **Pull Requests**: Code contributions
- **Discussions**: General questions, ideas
- **Email**: For sensitive issues

## 🏆 Recognition

Contributors will be:
- Listed in README.md
- Mentioned in release notes
- Given credit in commits

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 🙏 Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort!

**Questions?** Open an issue or discussion on GitHub.

---

**Ready to contribute?** Pick an issue and start coding! 🚀
