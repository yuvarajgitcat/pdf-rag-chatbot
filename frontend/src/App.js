import React from 'react';
import Upload from './Upload';
import Chat from './Chat';

function App() {
  return (
    <div style={{ padding: 20 }}>
      <h1>PDF RAG Chatbot</h1>
      <Upload />
      <Chat />
    </div>
  );
}

export default App;
