import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

function Post() {
  const { slug } = useParams();
  const [postData, setPostData] = useState(null);

  useEffect(() => {
    fetch(`/post/${slug}`)
      .then((res) => res.json())
      .then((data) => {
        console.log("Fetched data:", data);
        setPostData(data);
      });
  }, [slug]);

  if (!postData) {
    return <p>Loading...</p>;
  }

  if (postData.error) {
    return <p>{postData.error}</p>;
  }

  const { post, comments } = postData;

  return (
    <div>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
      <h2>Comments</h2>
      {comments.length > 0 ? (
        <ul>
          {comments.map((comment, index) => (
            <li key={index}>{comment.content}</li>
          ))}
        </ul>
      ) : (
        <p>No comments yet.</p>
      )}
    </div>
  );
}

export default Post;
