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

      // Debug: Log the actual response from the backend
      console.log("Backend response:", data);

      // Check if the response contains an error or detail field indicating timeout
      if (data.detail) {
        const errorMessage = {
          id: Date.now() + 1,
          text: `Server response: ${data.detail}`,
          sender: 'bot',
          timestamp: new Date()
        };

        setMessages(prev => [...prev, errorMessage]);
      } else {
        // Check if the response data has any keys at all
        console.log("Response data keys:", Object.keys(data));
        console.log("Response data type:", typeof data);

        // Map the backend response format to what the frontend expects
        // Check for various possible field names the backend might return
        let responseText = "No response text received from server";

        if (data && typeof data === 'object') {
          responseText = data.answer ||
                        data.response ||
                        data.text ||
                        data.result ||
                        data.output ||
                        (data.detail && !data.detail.includes('Query failed') ? data.detail : null) ||
                        "No response text received from server";
        } else if (data && typeof data === 'string') {
          responseText = data;
        }

        console.log("Selected response text:", responseText);

        const botMessage = {
          id: Date.now() + 1,
          text: responseText,
          sender: 'bot',
          sources: (data.sources || data.context || []).map(source => ({
            title: source.title || source.source || source.document || "Unknown Source",
            relevance: source.similarity || source.score || source.relevance || 0.8, // Assigning a default relevance
            text: source.text || source.content ? (source.text || source.content).length > 100 ?
              (source.text || source.content).substring(0, 100) + "..." :
              (source.text || source.content) : ""
          })),
          timestamp: new Date()
        };

        setMessages(prev => [...prev, botMessage]);
      }
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