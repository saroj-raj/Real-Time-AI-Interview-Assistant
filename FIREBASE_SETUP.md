# Firebase Setup Instructions

Your app needs Firebase Storage and Firestore configured properly. Follow these steps:

## 1. Firebase Storage Rules

Go to Firebase Console → Storage → Rules and set:

```
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /resumes/{userId}/{fileName} {
      // Allow users to upload their own resumes
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

## 2. Firestore Rules

Go to Firebase Console → Firestore Database → Rules and set:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can only read/write their own data
    match /resumes/{resumeId} {
      allow read, write: if request.auth != null && 
                         resource.data.userId == request.auth.uid;
      allow create: if request.auth != null && 
                    request.resource.data.userId == request.auth.uid;
    }
    
    match /jobDescriptions/{jdId} {
      allow read, write: if request.auth != null && 
                         resource.data.userId == request.auth.uid;
      allow create: if request.auth != null && 
                    request.resource.data.userId == request.auth.uid;
    }
    
    match /interviewSessions/{sessionId} {
      allow read, write: if request.auth != null && 
                         resource.data.userId == request.auth.uid;
      allow create: if request.auth != null && 
                    request.resource.data.userId == request.auth.uid;
    }
  }
}
```

## 3. Enable Firebase Storage

1. Go to Firebase Console → Storage
2. Click "Get Started"
3. Choose "Start in production mode"
4. Then update rules as shown above

## 4. Test the Upload

After setting up the rules:
1. Go to your dashboard
2. Click "Upload Resume"
3. Select a PDF, DOC, or TXT file
4. Check the browser console for upload progress logs
5. You should see a success message

If you see permission errors, double-check the Storage and Firestore rules match exactly.
