'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { collection, query, where, getDocs, addDoc } from 'firebase/firestore';
import { ref, uploadBytes, getDownloadURL } from 'firebase/storage';
import { signOut } from 'firebase/auth';
import { db, storage, auth } from '@/lib/firebase';
import { useStore } from '@/lib/store';
import { withAuth } from '@/components/auth/AuthProvider';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Plus, FileText, Briefcase, LogOut, Play } from 'lucide-react';
import type { Resume, JobDescription } from '@/types';

function DashboardPage() {
  const { user, setSelectedResume, setSelectedJobDescription } = useStore();
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [jobDescriptions, setJobDescriptions] = useState<JobDescription[]>([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    console.log('Dashboard mounted, user from store:', user);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const loadUserData = async () => {
    if (!user) {
      console.log('No user found, skipping data load');
      setLoading(false);
      return;
    }

    console.log('Loading data for user:', user.uid);

    try {
      // Load resumes
      console.log('Querying resumes...');
      const resumesQuery = query(
        collection(db, 'resumes'),
        where('userId', '==', user.uid)
      );
      const resumesSnapshot = await getDocs(resumesQuery);
      console.log('Resumes found:', resumesSnapshot.docs.length);
      const resumesData = resumesSnapshot.docs.map((doc) => ({
        id: doc.id,
        ...doc.data(),
        createdAt: doc.data().createdAt?.toDate() || new Date(),
        updatedAt: doc.data().updatedAt?.toDate() || new Date(),
      })) as Resume[];
      setResumes(resumesData);

      // Load job descriptions
      console.log('Querying job descriptions...');
      const jdsQuery = query(
        collection(db, 'jobDescriptions'),
        where('userId', '==', user.uid)
      );
      const jdsSnapshot = await getDocs(jdsQuery);
      console.log('Job descriptions found:', jdsSnapshot.docs.length);
      const jdsData = jdsSnapshot.docs.map((doc) => ({
        id: doc.id,
        ...doc.data(),
        createdAt: doc.data().createdAt?.toDate() || new Date(),
        updatedAt: doc.data().updatedAt?.toDate() || new Date(),
      })) as JobDescription[];
      setJobDescriptions(jdsData);
      
      console.log('Data loaded successfully');
    } catch (error) {
      console.error('Error loading user data:', error);
      // Show error in UI instead of just logging
      alert(`Error loading data: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      console.log('Setting loading to false');
      setLoading(false);
    }
  };

  useEffect(() => {
    if (user) {
      loadUserData();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user]);

  const handleResumeUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || !user) {
      console.log('No file selected or no user');
      return;
    }

    console.log('Starting resume upload:', file.name, file.size, 'bytes');
    setLoading(true);

    try {
      // Upload file to Firebase Storage
      console.log('Uploading to Firebase Storage...');
      const storageRef = ref(storage, `resumes/${user.uid}/${Date.now()}_${file.name}`);
      await uploadBytes(storageRef, file);
      const fileUrl = await getDownloadURL(storageRef);
      console.log('File uploaded successfully:', fileUrl);

      // Create resume document in Firestore
      console.log('Creating Firestore document...');
      const resumeData = {
        userId: user.uid,
        name: file.name,
        fileUrl,
        parsedData: {
          skills: [],
          experience: [],
          education: [],
          projects: [],
        },
        createdAt: new Date(),
        updatedAt: new Date(),
      };

      await addDoc(collection(db, 'resumes'), resumeData);
      console.log('Resume saved to Firestore');
      
      // Reload data
      await loadUserData();
      alert(`Resume "${file.name}" uploaded successfully!`);
    } catch (error) {
      console.error('Error uploading resume:', error);
      alert(`Failed to upload resume: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setLoading(false);
      // Reset the input so the same file can be uploaded again if needed
      e.target.value = '';
    }
  };

  const handleStartInterview = (resume: Resume, jd: JobDescription) => {
    setSelectedResume(resume);
    setSelectedJobDescription(jd);
    router.push('/setup');
  };

  const handleSignOut = async () => {
    await signOut(auth);
    router.push('/login');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading your data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <header className="bg-white border-b border-gray-200">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <div className="flex items-center gap-4">
            <span className="text-gray-600">{user?.email}</span>
            <Button variant="outline" size="sm" onClick={handleSignOut}>
              <LogOut className="h-4 w-4 mr-2" />
              Sign Out
            </Button>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="grid md:grid-cols-2 gap-8">
          {/* Resumes Section */}
          <div>
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold text-gray-900 flex items-center gap-2">
                <FileText className="h-5 w-5" />
                My Resumes
              </h2>
              <label>
                <input
                  type="file"
                  accept=".pdf,.doc,.docx,.txt"
                  onChange={handleResumeUpload}
                  className="hidden"
                />
                <Button size="sm" asChild>
                  <span className="cursor-pointer">
                    <Plus className="h-4 w-4 mr-2" />
                    Upload Resume
                  </span>
                </Button>
              </label>
            </div>

            <div className="space-y-3">
              {resumes.length === 0 ? (
                <Card>
                  <CardContent className="pt-6 text-center text-gray-500">
                    No resumes uploaded yet. Upload your first resume to get started!
                  </CardContent>
                </Card>
              ) : (
                resumes.map((resume) => (
                  <Card key={resume.id} className="hover:shadow-md transition-shadow">
                    <CardHeader>
                      <CardTitle className="text-base">{resume.name}</CardTitle>
                      <CardDescription>
                        Uploaded {resume.createdAt.toLocaleDateString()}
                      </CardDescription>
                    </CardHeader>
                  </Card>
                ))
              )}
            </div>
          </div>

          {/* Job Descriptions Section */}
          <div>
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold text-gray-900 flex items-center gap-2">
                <Briefcase className="h-5 w-5" />
                Job Descriptions
              </h2>
              <Button size="sm" onClick={() => router.push('/jd/new')}>
                <Plus className="h-4 w-4 mr-2" />
                Add JD
              </Button>
            </div>

            <div className="space-y-3">
              {jobDescriptions.length === 0 ? (
                <Card>
                  <CardContent className="pt-6 text-center text-gray-500">
                    No job descriptions added yet. Add one to start preparing!
                  </CardContent>
                </Card>
              ) : (
                jobDescriptions.map((jd) => (
                  <Card key={jd.id} className="hover:shadow-md transition-shadow">
                    <CardHeader>
                      <CardTitle className="text-base">
                        {jd.roleName} at {jd.companyName}
                      </CardTitle>
                      <CardDescription>
                        Added {jd.createdAt.toLocaleDateString()}
                      </CardDescription>
                    </CardHeader>
                  </Card>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Quick Start Section */}
        {resumes.length > 0 && jobDescriptions.length > 0 && (
          <div className="mt-12">
            <Card className="bg-gradient-to-r from-blue-50 to-indigo-50 border-blue-200">
              <CardHeader>
                <CardTitle>Ready to start an interview?</CardTitle>
                <CardDescription>
                  Select a resume and job description combination to begin
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid md:grid-cols-2 gap-4">
                  {resumes.slice(0, 2).map((resume) =>
                    jobDescriptions.slice(0, 2).map((jd) => (
                      <Button
                        key={`${resume.id}-${jd.id}`}
                        variant="outline"
                        className="h-auto py-4 justify-start"
                        onClick={() => handleStartInterview(resume, jd)}
                      >
                        <Play className="h-4 w-4 mr-2 flex-shrink-0" />
                        <div className="text-left">
                          <div className="font-semibold text-sm">
                            {resume.name.substring(0, 30)}...
                          </div>
                          <div className="text-xs text-gray-600">
                            {jd.roleName} at {jd.companyName}
                          </div>
                        </div>
                      </Button>
                    ))
                  )}
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </main>
    </div>
  );
}

export default withAuth(DashboardPage);
