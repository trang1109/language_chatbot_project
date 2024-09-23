import React, { useState } from "react";

function Chatbox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async () => {
    if (input.trim() === "") return; // Ngăn chặn gửi tin nhắn trống

    const userMessage = { text: input, sender: "user" };
    setMessages((prevMessages) => [...prevMessages, userMessage]);

    setIsLoading(true); // Bắt đầu trạng thái loading

    try {
      const response = await fetch("http://localhost:5000/api/chat", {
        method: "POST",
        body: JSON.stringify({ message: input }),
        headers: { "Content-Type": "application/json" },
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();

      setMessages((prevMessages) => [
        ...prevMessages,
        { text: data.reply, sender: "bot" }
      ]);
    } catch (error) {
      console.error("Error during fetch:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: "Error occurred, please try again.", sender: "bot" }
      ]);
    } finally {
      setIsLoading(false); // Kết thúc trạng thái loading
      setInput(""); // Xóa nội dung input sau khi gửi
    }
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
        onKeyPress={(e) => e.key === "Enter" && !isLoading && sendMessage()}
        disabled={isLoading} // Vô hiệu hóa khi đang chờ phản hồi
      />
      <button onClick={sendMessage} disabled={isLoading}>
        {isLoading ? "Sending..." : "Send"}
      </button>
    </div>
  );
}

export default Chatbox;
