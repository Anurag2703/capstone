import React, { useState } from 'react';
import '../styles/components/ChatSidebar.css';

const ChatSidebar = ({
  sessions,
  sessionIndex,
  setSessionIndex,
  startNewChat,
  setSessions, // ✅ For delete/rename
}) => {
  const [renamingIndex, setRenamingIndex] = useState(null);
  const [renameValue, setRenameValue] = useState('');

  const handleDelete = (index) => {
    const updated = [...sessions];
    updated.splice(index, 1);
    setSessions(updated);
    if (sessionIndex === index) {
      setSessionIndex(0);
    } else if (index < sessionIndex) {
      setSessionIndex(sessionIndex - 1);
    }
  };

  const handleRename = (index) => {
    const updated = [...sessions];
    updated[index].name = renameValue || `Session ${index + 1}`;
    setSessions(updated);
    setRenamingIndex(null);
  };

  return (
    <div className="chat-sidebar">
      <div className="sidebar-header">
        <h3 className="sidebar-title" style={{ marginTop: '70px' }}>Conversations</h3>
      </div>

      <button
        style={{
          marginBottom: '15px',
          width: '100%',
          padding: '10px',
          background: '#05c8f4',
          color: '#000',
          fontWeight: 'bold',
          border: 'none',
          borderRadius: '8px',
          cursor: 'pointer',
        }}
        onClick={startNewChat} // ✅ Fix New Chat
      >
        + New Chat
      </button>

      <div className="chat-list">
        {sessions.length === 0 ? (
          <div className="empty">No sessions yet</div>
        ) : (
          sessions.map((session, index) => {
            const title =
              session.name || session[0]?.content?.slice(0, 30) || `Session ${index + 1}`;
            return (
              <div
                key={index}
                className="chat-item"
                style={{
                  background: index === sessionIndex ? 'rgba(255, 255, 255, 0.3)' : undefined,
                  position: 'relative',
                }}
              >
                {renamingIndex === index ? (
                  <input
                    type="text"
                    value={renameValue}
                    autoFocus
                    onChange={(e) => setRenameValue(e.target.value)}
                    onBlur={() => handleRename(index)}
                    onKeyDown={(e) => e.key === 'Enter' && handleRename(index)}
                    style={{
                      width: '90%',
                      padding: '4px',
                      marginRight: '5px',
                    }}
                  />
                ) : (
                  <div
                    onClick={() => setSessionIndex(index)}
                    style={{ cursor: 'pointer', flex: 1 }}
                  >
                    {title}
                  </div>
                )}
                <div style={{ position: 'absolute', right: 6, top: 4 }}>
                  <button
                    onClick={() => {
                      setRenameValue(title);
                      setRenamingIndex(index);
                    }}
                    style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 0, marginTop: '7.5px' }}
                    title="Rename"
                  >
                    ✏️
                  </button>
                  <button
                    onClick={() => handleDelete(index)}
                    style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 0, marginTop: '7.5px' }}
                    title="Delete"
                  >
                    🗑️
                  </button>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};

export default ChatSidebar;




// import React, { useState } from 'react';
// import '../styles/components/ChatSidebar.css';

// const ChatSidebar = ({
//   sessions,
//   sessionIndex,
//   setSessionIndex,
//   onNewChat,
//   isCollapsed,
//   setIsCollapsed,
//   setSessions, // ✅ Add this prop to support delete/rename
// }) => {
//   const [renamingIndex, setRenamingIndex] = useState(null);
//   const [renameValue, setRenameValue] = useState('');

//   const handleDelete = (index) => {
//     const updated = [...sessions];
//     updated.splice(index, 1);
//     setSessions(updated);
//     if (sessionIndex === index) {
//       setSessionIndex(0);
//     } else if (index < sessionIndex) {
//       setSessionIndex(sessionIndex - 1);
//     }
//   };

//   const handleRename = (index) => {
//     const updated = [...sessions];
//     updated[index].name = renameValue || `Session ${index + 1}`;
//     setSessions(updated);
//     setRenamingIndex(null);
//   };

//   return (
//     <div className={`chat-sidebar ${isCollapsed ? 'collapsed' : ''}`}>
//       <div className="sidebar-header">
//         {!isCollapsed && <h3 className="sidebar-title">Conversations</h3>}
//         <button className="collapse-btn" onClick={() => setIsCollapsed(!isCollapsed)}>
//           {isCollapsed ? '⮞' : '⮜'}
//         </button>
//       </div>

//       {!isCollapsed && (
//         <button
//           style={{
//             marginBottom: '15px',
//             width: '100%',
//             padding: '10px',
//             background: '#05c8f4',
//             color: '#000',
//             fontWeight: 'bold',
//             border: 'none',
//             borderRadius: '8px',
//             cursor: 'pointer',
//           }}
//           onClick={onNewChat}
//         >
//           + New Chat
//         </button>
//       )}

//       <div className="chat-list">
//         {sessions.length === 0 ? (
//           <div className="empty">No sessions yet</div>
//         ) : (
//           sessions.map((session, index) => {
//             const title =
//               session.name || session[0]?.content?.slice(0, 30) || `Session ${index + 1}`;
//             return (
//               <div
//                 key={index}
//                 className="chat-item"
//                 style={{
//                   background: index === sessionIndex ? 'rgba(255, 255, 255, 0.3)' : undefined,
//                   position: 'relative',
//                 }}
//               >
//                 {renamingIndex === index ? (
//                   <input
//                     type="text"
//                     value={renameValue}
//                     autoFocus
//                     onChange={(e) => setRenameValue(e.target.value)}
//                     onBlur={() => handleRename(index)}
//                     onKeyDown={(e) => e.key === 'Enter' && handleRename(index)}
//                     style={{
//                       width: '90%',
//                       padding: '4px',
//                       marginRight: '5px',
//                     }}
//                   />
//                 ) : (
//                   <div
//                     onClick={() => setSessionIndex(index)}
//                     style={{ cursor: 'pointer', flex: 1 }}
//                   >
//                     {title}
//                   </div>
//                 )}
//                 {!isCollapsed && (
//                   <div style={{ position: 'absolute', right: 6, top: 4 }}>
//                     <button
//                       onClick={() => {
//                         setRenameValue(title);
//                         setRenamingIndex(index);
//                       }}
//                       style={{ marginRight: '6px', background: 'none', border: 'none', cursor: 'pointer' }}
//                       title="Rename"
//                     >
//                       ✏️
//                     </button>
//                     <button
//                       onClick={() => handleDelete(index)}
//                       style={{ background: 'none', border: 'none', cursor: 'pointer' }}
//                       title="Delete"
//                     >
//                       🗑️
//                     </button>
//                   </div>
//                 )}
//               </div>
//             );
//           })
//         )}
//       </div>
//     </div>
//   );
// };

// export default ChatSidebar;






// import React from "react";
// import "../styles/components/ChatSidebar.css";

// export default function ChatSidebar({ chats, collapsed, setCollapsed }) {
//   return (
//     <div className={`chat-sidebar ${collapsed ? "collapsed" : ""}`}>
//       <div className="sidebar-header">
//         {!collapsed && <h2 className="sidebar-title">Chats</h2>}
//         <button
//           className="collapse-btn"
//           onClick={() => setCollapsed(!collapsed)}
//           aria-label="Collapse sidebar"
//         >
//           {collapsed ? "➤" : "◀"}
//         </button>
//       </div>

//       {!collapsed && (
//         <div className="chat-list">
//           {chats.length === 0 ? (
//             <p className="empty">No chats yet</p>
//           ) : (
//             chats.map((chat) => (
//               <div key={chat.id} className="chat-item">
//                 {chat.text.slice(0, 20)}…
//               </div>
//             ))
//           )}
//         </div>
//       )}
//     </div>
//   );
// }
