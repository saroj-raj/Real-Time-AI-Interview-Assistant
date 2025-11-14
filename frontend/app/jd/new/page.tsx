'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { collection, addDoc } from 'firebase/firestore';
import { db } from '@/lib/firebase';
import { useStore } from '@/lib/store';
import { withAuth } from '@/components/auth/AuthProvider';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowLeft } from 'lucide-react';
import Link from 'next/link';

function NewJobDescriptionPage() {
  const { user } = useStore();
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    companyName: '',
    roleName: '',
    description: '',
    requirements: '',
    responsibilities: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user) return;

    setLoading(true);

    try {
      const jdData = {
        userId: user.uid,
        companyName: formData.companyName,
        roleName: formData.roleName,
        description: formData.description,
        requirements: formData.requirements.split('\n').filter(r => r.trim()),
        responsibilities: formData.responsibilities.split('\n').filter(r => r.trim()),
        createdAt: new Date(),
        updatedAt: new Date(),
      };

      await addDoc(collection(db, 'jobDescriptions'), jdData);
      router.push('/dashboard');
    } catch (error) {
      console.error('Error creating job description:', error);
      alert('Failed to create job description. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <header className="bg-white border-b border-gray-200">
        <div className="container mx-auto px-4 py-4">
          <Link href="/dashboard" className="inline-flex items-center text-blue-600 hover:text-blue-700">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Dashboard
          </Link>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <Card className="max-w-2xl mx-auto">
          <CardHeader>
            <CardTitle>Add Job Description</CardTitle>
            <CardDescription>
              Enter the details of the role you&apos;re preparing for
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="companyName" className="block text-sm font-medium text-black mb-1">
                  Company Name *
                </label>
                <input
                  id="companyName"
                  type="text"
                  value={formData.companyName}
                  onChange={(e) => setFormData({ ...formData, companyName: e.target.value })}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="e.g., Google, Microsoft, Startup Inc."
                />
              </div>

              <div>
                <label htmlFor="roleName" className="block text-sm font-medium text-black mb-1">
                  Role Name *
                </label>
                <input
                  id="roleName"
                  type="text"
                  value={formData.roleName}
                  onChange={(e) => setFormData({ ...formData, roleName: e.target.value })}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="e.g., Senior Software Engineer, Product Manager"
                />
              </div>

              <div>
                <label htmlFor="description" className="block text-sm font-medium text-black mb-1">
                  Job Description
                </label>
                <textarea
                  id="description"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  rows={4}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Brief overview of the role..."
                />
              </div>

              <div>
                <label htmlFor="requirements" className="block text-sm font-medium text-black mb-1">
                  Requirements
                </label>
                <textarea
                  id="requirements"
                  value={formData.requirements}
                  onChange={(e) => setFormData({ ...formData, requirements: e.target.value })}
                  rows={6}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="One requirement per line:&#10;5+ years of experience with Python&#10;Strong knowledge of React&#10;Experience with cloud platforms"
                />
                <p className="text-sm text-gray-600 mt-1">Enter one requirement per line</p>
              </div>

              <div>
                <label htmlFor="responsibilities" className="block text-sm font-medium text-black mb-1">
                  Responsibilities
                </label>
                <textarea
                  id="responsibilities"
                  value={formData.responsibilities}
                  onChange={(e) => setFormData({ ...formData, responsibilities: e.target.value })}
                  rows={6}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="One responsibility per line:&#10;Design and implement scalable systems&#10;Lead technical discussions&#10;Mentor junior engineers"
                />
                <p className="text-sm text-gray-600 mt-1">Enter one responsibility per line</p>
              </div>

              <div className="flex gap-4">
                <Button type="submit" disabled={loading} className="flex-1">
                  {loading ? 'Saving...' : 'Save Job Description'}
                </Button>
                <Button type="button" variant="outline" onClick={() => router.push('/dashboard')}>
                  Cancel
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </main>
    </div>
  );
}

export default withAuth(NewJobDescriptionPage);
