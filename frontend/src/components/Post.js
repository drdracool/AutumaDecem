import React, { useState, useEffect, useRef } from "react";
import { useParams } from "react-router-dom";
import CommentList from "./CommentList";
import CommentForm from "./CommentForm";

function Post() {
  const [postData, setPostData] = useState(null);
  const contentRef = useRef(null);
  const { slug } = useParams();

  useEffect(() => {
    fetch(`/post/${slug}`)
      .then((res) => res.json())
      .then((data) => {
        setPostData(data);
      })
      .catch((error) => console.error("Error fetching post:", error));
  }, [slug]);

  const handleCommentSubmit = (comment) => {
    fetch(`/post/${slug}/comment`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(comment),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.error) {
          alert(data.error);
        } else {
          alert("Comment submitted successfully!");
          fetch(`/post/${slug}`)
            .then((res) => res.json())
            .then((data) => {
              setPostData(data);
            });
        }
      })
      .catch((error) => console.error("Error submitting comment:", error));
  };

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
      <div
        ref={contentRef}
        dangerouslySetInnerHTML={{ __html: post.content }} //convert html json data to actual html using dangerouslySetInnerHTML
        style={{ textAlign: "justify" }}
      />
      <CommentList comments={comments} />
      <CommentForm onCommentSubmit={handleCommentSubmit} />
    </div>
  );
}

export default Post;
