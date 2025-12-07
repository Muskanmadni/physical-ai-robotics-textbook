const { spawn } = require('child_process');
const readline = require('readline');

// Create readline interface for user input
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Configuration - Update with your actual backend URL
const RAG_API_URL = 'http://localhost:8000/api/rag/query';

async function queryRAG(question) {
  try {
    const response = await fetch(RAG_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        query: question
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error querying RAG system:', error);
    return null;
  }
}

function startChat() {
  // Check if fetch is available, if not, we'll install node-fetch
  if (typeof fetch === 'undefined') {
    console.log('Installing node-fetch...');
    const { exec } = require('child_process');
    exec('npm install node-fetch@2', (error, stdout, stderr) => {
      if (error) {
        console.error('Error installing node-fetch:', error);
        return;
      }
      console.log('node-fetch installed successfully');
      
      // Now run the chat function after installation
      runChat();
    });
  } else {
    runChat();
  }
}

async function runChat() {
  console.log('🤖 RAG Chatbot for Physical AI & Humanoid Robotics Textbook');
  console.log('Ask me anything about the textbook content!');
  console.log('Type "exit" to quit.\n');

  const askQuestion = () => {
    rl.question('You: ', async (question) => {
      if (question.toLowerCase() === 'exit') {
        console.log('Goodbye!');
        rl.close();
        return;
      }

      if (question.trim() === '') {
        askQuestion();
        return;
      }

      console.log('Thinking...\n');
      
      const result = await queryRAG(question);
      
      if (result) {
        console.log('🤖 Answer:', result.response);
        if (result.sources && result.sources.length > 0) {
          console.log('\n📖 Sources:');
          result.sources.forEach((source, index) => {
            console.log(`  ${index + 1}. ${source.title} (Relevance: ${(source.relevance * 100).toFixed(2)}%)`);
          });
        }
      } else {
        console.log('❌ Sorry, I encountered an error processing your request.');
      }
      
      console.log('');
      askQuestion();
    });
  };

  askQuestion();
}

// For Node.js environments where fetch is not available by default
if (typeof global !== 'undefined' && typeof global.fetch === 'undefined') {
  global.fetch = require('node-fetch');
}

startChat();