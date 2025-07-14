import React, { useState } from 'react';
import { askQuestion } from './api';

export default function Chat() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');

  const handleAsk = async () => {
    const res = await askQuestion(question);
    setAnswer(res.data.answer);
  };

  return (
    <div>
      <h2>Ask a Question</h2>
      <input
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Type your question"
      />
      <button onClick={handleAsk}>Ask</button>
      <p>{answer}</p>
    </div>
  );
}
