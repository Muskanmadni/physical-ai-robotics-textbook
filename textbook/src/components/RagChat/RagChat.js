import React, { useState, useRef, useEffect } from 'react';
import apiService from '../../services/api';
import './RagChat.css';

const RagChat = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message to the chat
    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const data = await apiService.query(inputValue, 3);

      // Map the backend response format to what the frontend expects
      // Backend returns: { answer: "...", sources: [...] }
      // Frontend expects: { response: "...", sources: [...] }
      const botMessage = {
        id: Date.now() + 1,
        text: data.answer || data.response || "No response text received from server",
        sender: 'bot',
        sources: (data.sources || []).map(source => ({
          // Backend returns: { text, source, title }
          // Frontend expects: { title, relevance }
          title: source.title || source.source || "Unknown Source",
          relevance: source.similarity || source.score || 0.8, // Assigning a default relevance
          text: source.text ? (source.text.length > 100 ? source.text.substring(0, 100) + "..." : source.text) : ""
        })),
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error fetching response:', error);

      const errorMessage = {
        id: Date.now() + 1,
        text: `Sorry, I encountered an error while processing your request: ${error.message}. Please try again.`,
        sender: 'bot',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="rag-chat-container">
      <div className="rag-chat-header">
        <h3>Physical AI & Humanoid Robotics Assistant</h3>
        <p>Ask me anything about the textbook content</p>
      </div>

      <div className="rag-chat-messages">
        {messages.length === 0 ? (
          <div className="rag-chat-welcome">
            <h4>Welcome to the Physical AI & Humanoid Robotics Assistant!</h4>
            <p>Ask questions about the textbook content, such as:</p>
            <ul>
              <li>What is ROS 2 and how does it differ from ROS 1?</li>
              <li>How do NVIDIA Isaac robotics simulators work?</li>
              <li>What are Vision-Language-Action systems?</li>
            </ul>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`rag-chat-message ${message.sender}-message`}
            >
              <div className="message-content">
                <p>{message.text}</p>
                {message.sources && message.sources.length > 0 && (
                  <div className="message-sources">
                    <h5>Sources:</h5>
                    <ul>
                      {message.sources.slice(0, 3).map((source, index) => (
                        <li key={index}>
                          <strong>{source.title}</strong>
                          {source.text && <p><small>{source.text}</small></p>}
                          {source.relevance !== undefined && (
                            <p><small>Relevance: {(source.relevance * 100).toFixed(1)}%</small></p>
                          )}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="rag-chat-message bot-message">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className="rag-chat-input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask a question about the textbook..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  );
};

export default RagChat;