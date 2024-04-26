import React, { useState, useEffect } from 'react';
import './App.css'; 
import AnimatedTextDisplay from './AnimatedText.js';

function Chatbot() {
  const [ws, setWs] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  useEffect(() => {
    // Create WebSocket connection
    const websocket = new WebSocket('ws://localhost:8000/api/send-message');

    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);

      // Handle different types of messages here
      if (data.reply) {
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: data.reply, sender: 'bot' }
        ]);
      }

      if (data.data_searched) {
        const data_searched_message = "Searching for " + data.data_searched + "...";
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: data_searched_message, sender: 'bot' }
        ]);
      }
    };

    websocket.onerror = (error) => {
      console.error('WebSocket Error: ', error);
    };

    setWs(websocket);

    return () => {
      websocket.close();
    };
  }, []);

  const sendMessage = () => {
    if (!input.trim()) return;

    setMessages((prevMessages) => [
      ...prevMessages,
      { text: input, sender: 'user' }
    ]);

    if (ws) {
      ws.send(JSON.stringify({ message: input }));
      setInput(''); // Clear the input field
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <img src='logo.png' alt="Next Step Logo" className="header-image" />
      </div>
      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`chat-bubble ${msg.sender === 'user' ? 'user' : 'bot'}`}>
            <AnimatedTextDisplay text={msg.text} sender={msg.sender} />
          </div>
        ))}
      </div>
      <div className="input-container">
        <input
          id='textInput'
          onKeyDown={(event) => { if(event.code === 'Enter'){ sendMessage(); } }}
          value={input} onChange={(e) => setInput(e.target.value)} type="text"/>
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default Chatbot;
