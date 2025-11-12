import Link from 'next/link';
import { Mic, Brain, Clock, TrendingUp } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <main className="container mx-auto px-4 py-12 md:py-20">
        {/* Hero Section */}
        <div className="text-center space-y-6 mb-16">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 tracking-tight">
            AI Interview Assistant
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 max-w-2xl mx-auto">
            Practice interviews with real-time AI feedback and improve your chances of landing your dream job
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-4">
            <Link href="/login">
              <Button size="lg" className="w-full sm:w-auto text-lg px-8 py-6">
                Get Started
              </Button>
            </Link>
            <Link href="#features">
              <Button variant="outline" size="lg" className="w-full sm:w-auto text-lg px-8 py-6">
                Learn More
              </Button>
            </Link>
          </div>
        </div>

        {/* Features Section */}
        <div id="features" className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
          <Card>
            <CardHeader>
              <Mic className="h-10 w-10 text-blue-600 mb-2" />
              <CardTitle>Voice Recording</CardTitle>
              <CardDescription className="text-gray-700">
                Record your answers with high-quality audio capture
              </CardDescription>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader>
              <Brain className="h-10 w-10 text-blue-600 mb-2" />
              <CardTitle>AI Feedback</CardTitle>
              <CardDescription className="text-gray-700">
                Get instant, personalized feedback powered by advanced LLMs
              </CardDescription>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader>
              <Clock className="h-10 w-10 text-blue-600 mb-2" />
              <CardTitle>Real-Time Analysis</CardTitle>
              <CardDescription className="text-gray-700">
                See transcriptions and feedback as you speak
              </CardDescription>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader>
              <TrendingUp className="h-10 w-10 text-blue-600 mb-2" />
              <CardTitle>Track Progress</CardTitle>
              <CardDescription className="text-gray-700">
                Review past sessions and monitor your improvement
              </CardDescription>
            </CardHeader>
          </Card>
        </div>

        {/* How It Works */}
        <div className="bg-white rounded-2xl shadow-lg p-8 md:p-12">
          <h2 className="text-3xl font-bold text-center mb-8">How It Works</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-blue-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-blue-600">1</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Record Your Answer</h3>
              <p className="text-gray-700">
                Click the microphone button and answer the interview question naturally
              </p>
            </div>

            <div className="text-center">
              <div className="bg-blue-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-blue-600">2</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Real-Time Transcription</h3>
              <p className="text-gray-700">
                Watch as your speech is transcribed in real-time using Whisper AI
              </p>
            </div>

            <div className="text-center">
              <div className="bg-blue-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-blue-600">3</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Get AI Feedback</h3>
              <p className="text-gray-700">
                Receive instant, personalized feedback to improve your responses
              </p>
            </div>
          </div>

          <div className="text-center mt-12">
            <Link href="/login">
              <Button size="lg" className="text-lg px-8 py-6">
                Try It Now - It&apos;s Free!
              </Button>
            </Link>
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-16 text-center text-gray-700">
          <p>Built with Next.js, TypeScript, and AI</p>
        </footer>
      </main>
    </div>
  );
}
