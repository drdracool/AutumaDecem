import React, { useState } from "react";

function CommentForm({ onCommentSubmit }) {
  const [username, setUsername] = useState("");
  const [content, setContent] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (username.trim() && content.trim()) {
      onCommentSubmit({ username, content });
      setUsername("");
      setContent("");
    } else {
      alert("Username and content cannot be empty!");
    }
  };
  return (
    <form onSubmit={handleSubmit}>
      <h3>Leave a Comment</h3>
      <div>
        <input
          type="text"
          placeholder="Your Name"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
      </div>
      <div>
        <textarea
          placeholder="Your Comment"
          value={content}
          onChange={(e) => setContent(e.target.value)}
        />
      </div>
      <button type="submit">Submit</button>
    </form>
  );
}

export default CommentForm;
