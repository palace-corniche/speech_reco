import React, { useState, useRef } from 'react';
import { Mic, Square, Pause, Play, Trash2, Save, Copy } from 'lucide-react';

export default function SpeechRecognitionApp() {
  const [transcribedText, setTranscribedText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('en-US');
  const [selectedAPI, setSelectedAPI] = useState('web');
  const [status, setStatus] = useState('');
  const recognitionRef = useRef(null);

  const languages = {
    'English': 'en-US',
    'Spanish': 'es-ES',
    'French': 'fr-FR',
    'German': 'de-DE',
    'Chinese': 'zh-CN',
    'Japanese': 'ja-JP',
    'Portuguese': 'pt-PT',
  };

  const startRecording = () => {
    try {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRecognition) {
        setStatus('❌ Speech Recognition not supported in your browser');
        return;
      }

      const recognition = new SpeechRecognition();
      recognition.language = selectedLanguage;
      recognition.continuous = true;
      recognition.interimResults = true;

      recognition.onstart = () => {
        setIsRecording(true);
        setStatus('🎤 Listening...');
      };

      recognition.onresult = (event) => {
        let interimTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            setTranscribedText(prev => prev + ' ' + transcript);
          } else {
            interimTranscript += transcript;
          }
        }
        if (interimTranscript) {
          setStatus(`🎤 Listening... "${interimTranscript}"`);
        }
      };

      recognition.onerror = (event) => {
        setStatus(`❌ Error: ${event.error}`);
      };

      recognition.onend = () => {
        setIsRecording(false);
        setStatus('✅ Recording stopped');
      };

      recognitionRef.current = recognition;
      recognition.start();
    } catch (error) {
      setStatus(`❌ Error: ${error.message}`);
    }
  };

  const stopRecording = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      setIsRecording(false);
      setIsPaused(false);
    }
  };

  const pauseRecording = () => {
    if (recognitionRef.current) {
      if (isPaused) {
        recognitionRef.current.abort();
        startRecording();
        setIsPaused(false);
      } else {
        recognitionRef.current.abort();
        setIsPaused(true);
        setStatus('⏸️ Paused');
      }
    }
  };

  const clearText = () => {
    setTranscribedText('');
    setStatus('');
  };

  const saveToFile = () => {
    if (!transcribedText.trim()) {
      setStatus('⚠️ No text to save');
      return;
    }

    const element = document.createElement('a');
    const file = new Blob([transcribedText], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
    element.download = `transcription_${timestamp}.txt`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
    setStatus('✅ File saved!');
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(transcribedText);
    setStatus('📋 Copied to clipboard!');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">🎤 Speech Recognition App</h1>
          <p className="text-gray-600">Convert your speech to text using browser's built-in Web Speech API</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Sidebar Settings */}
          <div className="lg:col-span-1 bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-6">⚙️ Settings</h2>

            <div className="mb-6">
              <label className="block text-sm font-semibold text-gray-700 mb-2">API Type</label>
              <select
                value={selectedAPI}
                onChange={(e) => setSelectedAPI(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="web">Web Speech API</option>
              </select>
              <p className="text-xs text-gray-500 mt-2">✅ Works offline (no installation needed)</p>
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Language</label>
              <select
                value={selectedLanguage}
                onChange={(e) => setSelectedLanguage(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {Object.entries(languages).map(([name, code]) => (
                  <option key={code} value={code}>{name}</option>
                ))}
              </select>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3 space-y-6">
            {/* Recording Section */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Recording Controls</h2>
              
              <div className="flex flex-wrap gap-3 mb-4">
                <button
                  onClick={startRecording}
                  disabled={isRecording}
                  className="flex items-center gap-2 px-6 py-3 bg-red-500 text-white rounded-lg font-semibold hover:bg-red-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
                >
                  <Mic size={20} /> Start Recording
                </button>

                <button
                  onClick={pauseRecording}
                  disabled={!isRecording}
                  className="flex items-center gap-2 px-6 py-3 bg-yellow-500 text-white rounded-lg font-semibold hover:bg-yellow-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
                >
                  {isPaused ? <Play size={20} /> : <Pause size={20} />}
                  {isPaused ? 'Resume' : 'Pause'}
                </button>

                <button
                  onClick={stopRecording}
                  disabled={!isRecording}
                  className="flex items-center gap-2 px-6 py-3 bg-gray-700 text-white rounded-lg font-semibold hover:bg-gray-800 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
                >
                  <Square size={20} /> Stop
                </button>
              </div>

              {/* Status Display */}
              {status && (
                <div className={`p-3 rounded-lg font-semibold ${
                  status.includes('❌') ? 'bg-red-100 text-red-800' :
                  status.includes('✅') ? 'bg-green-100 text-green-800' :
                  'bg-blue-100 text-blue-800'
                }`}>
                  {status}
                </div>
              )}

              {isRecording && (
                <div className="mt-3 p-3 bg-blue-100 text-blue-800 rounded-lg font-semibold">
                  🔴 Recording is ACTIVE - Please speak now...
                </div>
              )}

              {isPaused && (
                <div className="mt-3 p-3 bg-yellow-100 text-yellow-800 rounded-lg font-semibold">
                  ⏸️ Recording is PAUSED
                </div>
              )}
            </div>

            {/* Text Display */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Transcribed Text</h2>
              <textarea
                value={transcribedText}
                onChange={(e) => setTranscribedText(e.target.value)}
                placeholder="Your transcribed text will appear here..."
                className="w-full h-48 p-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              />
            </div>

            {/* Actions */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Actions</h2>
              <div className="flex flex-wrap gap-3">
                <button
                  onClick={copyToClipboard}
                  className="flex items-center gap-2 px-6 py-3 bg-blue-500 text-white rounded-lg font-semibold hover:bg-blue-600 transition"
                >
                  <Copy size={20} /> Copy
                </button>

                <button
                  onClick={saveToFile}
                  className="flex items-center gap-2 px-6 py-3 bg-green-500 text-white rounded-lg font-semibold hover:bg-green-600 transition"
                >
                  <Save size={20} /> Save File
                </button>

                <button
                  onClick={clearText}
                  className="flex items-center gap-2 px-6 py-3 bg-red-500 text-white rounded-lg font-semibold hover:bg-red-600 transition"
                >
                  <Trash2 size={20} /> Clear
                </button>
              </div>
            </div>

            {/* Instructions */}
            <div className="bg-indigo-50 rounded-lg shadow-lg p-6 border-l-4 border-indigo-500">
              <h3 className="text-lg font-bold text-indigo-900 mb-3">📋 How to use:</h3>
              <ul className="space-y-2 text-indigo-800">
                <li>✅ Choose your language from settings</li>
                <li>✅ Click "Start Recording" and speak clearly</li>
                <li>✅ Use Pause/Resume if needed</li>
                <li>✅ Click "Stop" when done</li>
                <li>✅ Copy text or save to a file</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
