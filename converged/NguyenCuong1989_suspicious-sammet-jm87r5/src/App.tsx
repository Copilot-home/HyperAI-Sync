import React, { useState } from 'react';
import { input } from './components/ui/input';
import { textarea } from './components/ui/textarea';
import { button } from './components/ui/button';

export default function AIHacking() {
  const [systemName, setSystemName] = useState('');
  const [systemDescription, setSystemDescription] = useState('');
  const [systemGoals, setSystemGoals] = useState('');
  const [systemArchitecture, setSystemArchitecture] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log('System Name:', systemName);
    console.log('System Description:', systemDescription);
    console.log('System Goals:', systemGoals);
    console.log('System Architecture:', systemArchitecture);
  };

  return (
    <div className="max-w-7xl mx-auto p-4 sm:p-6 md:p-8">
      <h1 className="text-3xl font-bold mb-4">AIHacking System</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={systemName}
          onChange={(event) => setSystemName(event.target.value)}
          placeholder="System Name"
          className="block w-full p-2 mb-4 border border-gray-300 rounded-md"
        />
        <textarea
          value={systemDescription}
          onChange={(event) => setSystemDescription(event.target.value)}
          placeholder="System Description"
          className="block w-full p-2 mb-4 border border-gray-300 rounded-md"
        />
        <textarea
          value={systemGoals}
          onChange={(event) => setSystemGoals(event.target.value)}
          placeholder="System Goals"
          className="block w-full p-2 mb-4 border border-gray-300 rounded-md"
        />
        <textarea
          value={systemArchitecture}
          onChange={(event) => setSystemArchitecture(event.target.value)}
          placeholder="System Architecture"
          className="block w-full p-2 mb-4 border border-gray-300 rounded-md"
        />
        <button
          type="submit"
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Submit
        </button>
      </form>
    </div>
  );
}