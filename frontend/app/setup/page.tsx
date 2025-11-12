'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { addDoc, collection } from 'firebase/firestore';
import { db } from '@/lib/firebase';
import { useStore } from '@/lib/store';
import { withAuth } from '@/components/auth/AuthProvider';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowLeft } from 'lucide-react';
import type { InterviewSession } from '@/types';

function SetupPage() {
  const { user, selectedResume, selectedJobDescription, setCurrentSession } = useStore();
  const [companyName, setCompanyName] = useState(selectedJobDescription?.companyName || '');
  const [roleName, setRoleName] = useState(selectedJobDescription?.roleName || '');
  const [isFollowUp, setIsFollowUp] = useState(false);
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleStartInterview = async () => {
    if (!user || !selectedResume || !selectedJobDescription) {
      alert('Please select a resume and job description first');
      router.push('/dashboard');
      return;
    }

    setLoading(true);
    try {
      const sessionData: Omit<InterviewSession, 'id'> = {
        userId: user.uid,
        resumeId: selectedResume.id,
        jobDescriptionId: selectedJobDescription.id,
        companyName,
        roleName,
        status: 'live',
        startedAt: new Date(),
        isFollowUp,
        notes,
        createdAt: new Date(),
        updatedAt: new Date(),
      };

      const docRef = await addDoc(collection(db, 'interviewSessions'), sessionData);
      const session: InterviewSession = { id: docRef.id, ...sessionData };
      
      setCurrentSession(session);
      router.push('/interview');
    } catch (error) {
      console.error('Error creating session:', error);
      alert('Failed to start interview. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <div className="container mx-auto px-4 py-8">
        <Button variant="ghost" onClick={() => router.push('/dashboard')} className="mb-6">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Dashboard
        </Button>

        <Card className="max-w-2xl mx-auto">
          <CardHeader>
            <CardTitle>Interview Setup</CardTitle>
            <CardDescription>
              Configure your interview session before starting
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Selected Resume & JD */}
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Selected Resume
                </label>
                <div className="p-3 bg-gray-50 rounded-md text-sm">
                  {selectedResume?.name || 'None selected'}
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Selected Job Description
                </label>
                <div className="p-3 bg-gray-50 rounded-md text-sm">
                  {selectedJobDescription
                    ? `${selectedJobDescription.roleName} at ${selectedJobDescription.companyName}`
                    : 'None selected'}
                </div>
              </div>
            </div>

            {/* Company Name */}
            <div>
              <label htmlFor="company" className="block text-sm font-medium text-gray-700 mb-2">
                Company Name
              </label>
              <input
                id="company"
                type="text"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="e.g., Google"
                required
              />
            </div>

            {/* Role Name */}
            <div>
              <label htmlFor="role" className="block text-sm font-medium text-gray-700 mb-2">
                Role / Position
              </label>
              <input
                id="role"
                type="text"
                value={roleName}
                onChange={(e) => setRoleName(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="e.g., Senior AI Engineer"
                required
              />
            </div>

            {/* Follow-up Interview */}
            <div className="flex items-center">
              <input
                id="followup"
                type="checkbox"
                checked={isFollowUp}
                onChange={(e) => setIsFollowUp(e.target.checked)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label htmlFor="followup" className="ml-2 block text-sm text-gray-700">
                This is a follow-up interview (AI will reference previous session context)
              </label>
            </div>

            {/* Notes */}
            <div>
              <label htmlFor="notes" className="block text-sm font-medium text-gray-700 mb-2">
                Notes (Optional)
              </label>
              <textarea
                id="notes"
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Any specific points you want to mention during the interview..."
              />
            </div>

            {/* Start Button */}
            <Button
              onClick={handleStartInterview}
              disabled={loading || !companyName || !roleName}
              className="w-full"
              size="lg"
            >
              {loading ? 'Starting Interview...' : 'Start Live Interview'}
            </Button>

            <p className="text-sm text-gray-500 text-center">
              Make sure your microphone is connected and working before starting
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

export default withAuth(SetupPage);
