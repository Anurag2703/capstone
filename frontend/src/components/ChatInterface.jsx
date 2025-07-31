import React, { useState } from "react";
import BackgroundScene from "./BackgroundScene";
import ChatSidebar from "./ChatSidebar";
import axios from "axios";
import "../styles/components/ChatInterface.css";

export default function ChatInterface() {
  const [sessions, setSessions] = useState([[]]);
  const [sessionIndex, setSessionIndex] = useState(0);
  const [currentMessage, setCurrentMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [collapsed, setCollapsed] = useState(false);

  const chats = sessions[sessionIndex];

  const handleSend = async () => {
    if (currentMessage.trim() === "") return;

    const userMessage = { id: Date.now(), text: currentMessage, sender: "user" };
    const updatedSession = [...chats, userMessage];
    const updatedSessions = [...sessions];
    updatedSessions[sessionIndex] = updatedSession;
    setSessions(updatedSessions);
    setLoading(true);

    try {
      const res = await axios.post(
        `${import.meta.env.VITE_BACKEND_URL}/chatbot/`,
        {
          student_id: "test-student",
          message: currentMessage,
        }
      );

      const botReply = res.data.reply;
      const botMessage = { id: Date.now() + 1, text: botReply, sender: "bot" };
      updatedSessions[sessionIndex] = [...updatedSession, botMessage];
      setSessions([...updatedSessions]);
    } catch (err) {
      console.error("Chatbot error:", err);
      const errorMessage = {
        id: Date.now() + 2,
        text: "Error: Could not get response from server.",
        sender: "bot",
      };
      updatedSessions[sessionIndex] = [...updatedSession, errorMessage];
      setSessions([...updatedSessions]);
    } finally {
      setCurrentMessage("");
      setLoading(false);
    }
  };

  const startNewChat = () => {
    setSessions((prev) => [...prev, []]);
    setSessionIndex(sessions.length);
  };

  return (
    <div className="chat-interface">
      <BackgroundScene />

      <ChatSidebar
        sessions={sessions}
        setSessions={setSessions} // ✅ required for delete/rename
        sessionIndex={sessionIndex}
        setSessionIndex={setSessionIndex}
        startNewChat={startNewChat}
        collapsed={collapsed}
        setCollapsed={setCollapsed}
      />

      <div className={`chat-main ${collapsed ? "collapsed" : ""}`}>
        <div className="chat-history">
          {chats.map((chat) => (
            <div
              key={chat.id}
              className={`chat-bubble-wrapper ${chat.sender === "user" ? "right" : "left"}`}
            >
              {chat.sender === "bot" && (
                <img src="/bot.png" alt="bot" className="chat-icon" />
              )}
              <div className={`chat-bubble ${chat.sender}`}>
                {chat.text}
              </div>
              {chat.sender === "user" && (
                <img src="/user.png" alt="user" className="chat-icon" />
              )}
            </div>
          ))}
          {loading && <div className="chat-bubble bot">Thinking...</div>}
        </div>
        <div className="chat-input-container">
          <input
            type="text"
            value={currentMessage}
            onChange={(e) => setCurrentMessage(e.target.value)}
            placeholder="Type a message..."
          />
          <button onClick={handleSend}>➤</button>
        </div>
      </div>
    </div>
  );
}






// import React, { useState } from "react";
// import BackgroundScene from "./BackgroundScene";
// import ChatSidebar from "./ChatSidebar";
// import axios from "axios";
// import "../styles/components/ChatInterface.css";

// export default function ChatInterface() {
//   const [chats, setChats] = useState([]);
//   const [currentMessage, setCurrentMessage] = useState("");
//   const [loading, setLoading] = useState(false);

//   // 🔥 collapse state managed here
//   const [collapsed, setCollapsed] = useState(false);

//   const handleSend = async () => {
//     if (currentMessage.trim() === "") return;

//     const userMessage = { id: Date.now(), text: currentMessage, sender: "user" };
//     setChats((prev) => [...prev, userMessage]);
//     setLoading(true);

//     try {
//       const res = await axios.post(
//         `${import.meta.env.VITE_BACKEND_URL}/chatbot/`,
//         {
//           student_id: "test-student",
//           message: currentMessage,
//         }
//       );

//       const botReply = res.data.reply;
//       const botMessage = { id: Date.now() + 1, text: botReply, sender: "bot" };
//       setChats((prev) => [...prev, botMessage]);
//     } catch (err) {
//       console.error("Chatbot error:", err);
//       const errorMessage = {
//         id: Date.now() + 2,
//         text: "Error: Could not get response from server.",
//         sender: "bot",
//       };
//       setChats((prev) => [...prev, errorMessage]);
//     } finally {
//       setCurrentMessage("");
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="chat-interface">
//       <BackgroundScene />

//       {/* Sidebar with collapsed control */}
//       <ChatSidebar
//         chats={chats}
//         collapsed={collapsed}
//         setCollapsed={setCollapsed}
//       />

//       {/* Main Chat Area */}
//       <div className={`chat-main ${collapsed ? "collapsed" : ""}`}>
//         <div className="chat-history">
//           {chats.map((chat) => (
//             <div
//               key={chat.id}
//               className={`chat-bubble-wrapper ${chat.sender === "user" ? "right" : "left"}`}
//             >
//               {chat.sender === "bot" && (
//                 <img src="/bot.png" alt="bot" className="chat-icon" />
//               )}
//               <div className={`chat-bubble ${chat.sender}`}>
//                 {chat.text}
//               </div>
//               {chat.sender === "user" && (
//                 <img src="/user.png" alt="user" className="chat-icon" />
//               )}
//             </div>
//           ))}
//           {loading && <div className="chat-bubble bot">Thinking...</div>}
//         </div>
//         <div className="chat-input-container">
//           <input
//             type="text"
//             value={currentMessage}
//             onChange={(e) => setCurrentMessage(e.target.value)}
//             placeholder="Type a message..."
//           />
//           <button onClick={handleSend}>➤</button>
//         </div>
//       </div>
//     </div>
//   );
// }





// import React, { useState } from "react";
// import BackgroundScene from "./BackgroundScene";
// import ChatSidebar from "./ChatSidebar";
// import axios from "axios";
// import "../styles/components/ChatInterface.css";

// export default function ChatInterface() {
//   const [chats, setChats] = useState([]);
//   const [currentMessage, setCurrentMessage] = useState("");
//   const [loading, setLoading] = useState(false);

//   // 🔥 collapse state managed here
//   const [collapsed, setCollapsed] = useState(false);

//   const handleSend = async () => {
//     if (currentMessage.trim() === "") return;

//     const userMessage = { id: Date.now(), text: currentMessage, sender: "user" };
//     setChats((prev) => [...prev, userMessage]);
//     setLoading(true);

//     try {
//       const res = await axios.post(
//         `${import.meta.env.VITE_BACKEND_URL}/chatbot/`,
//         {
//           student_id: "test-student",
//           message: currentMessage,
//         }
//       );

//       const botReply = res.data.reply;
//       const botMessage = { id: Date.now() + 1, text: botReply, sender: "bot" };
//       setChats((prev) => [...prev, botMessage]);
//     } catch (err) {
//       console.error("Chatbot error:", err);
//       const errorMessage = {
//         id: Date.now() + 2,
//         text: "Error: Could not get response from server.",
//         sender: "bot",
//       };
//       setChats((prev) => [...prev, errorMessage]);
//     } finally {
//       setCurrentMessage("");
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="chat-interface">
//       <BackgroundScene />

//       {/* pass collapsed state + toggle to sidebar */}
//       <ChatSidebar chats={chats} collapsed={collapsed} setCollapsed={setCollapsed} />

//       {/* Main Chat Area */}
//       <div className={`chat-main ${collapsed ? "collapsed" : ""}`}>
//         <div className="chat-history">
//           {chats.map((chat) => (
//             <div
//               key={chat.id}
//               className={`chat-bubble ${chat.sender === "user" ? "user" : "bot"}`}
//             >
//               {chat.text}
//             </div>
//           ))}
//           {loading && <div className="chat-bubble bot">Thinking...</div>}
//         </div>
//         <div className="chat-input-container">
//           <input
//             type="text"
//             value={currentMessage}
//             onChange={(e) => setCurrentMessage(e.target.value)}
//             placeholder="Type a message..."
//           />
//           <button onClick={handleSend}>Send</button>
//         </div>
//       </div>
//     </div>
//   );
// }
