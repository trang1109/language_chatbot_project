import React, { useState } from "react";

function Chatbox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    const userMessage = { text: input, sender: "user" };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
  
    const response = await fetch("http://localhost:5000/api/chat", {
      method: "POST",
      body: JSON.stringify({ message: input }),
      headers: { "Content-Type": "application/json" },
    });
  
    const data = await response.json();
    setMessages((prevMessages) => [
      ...prevMessages,
      { text: data.reply, sender: "bot" }
    ]);
    setInput("");
  };
  

  return (
    <div>
      <div className="chat-window">
        {messages.map((msg, index) => (
          <p key={index}><strong>{msg.sender}</strong>: {msg.text}</p>
        ))}
      </div>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={(e) => e.key === "Enter" && sendMessage()}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default Chatbox;
