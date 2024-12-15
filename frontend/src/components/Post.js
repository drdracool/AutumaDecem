import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

function Post() {
  const { slug } = useParams;
  const [post, setPost] = useState(null);

  useEffect(() => {
    fetch(`/post/${slug}`)
      .then((res) => res.json())
      .then((data) => {
        console.log(slug);
        setPost(data);
      });
  }, [slug]);

  if (!post) {
    return <p>Loading...</p>;
  }

  if (post.error) {
    return <p>{post.error}</p>;
  }

  return (
    <div>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </div>
  );
}

export default Post;
