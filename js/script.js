document.addEventListener('DOMContentLoaded', () => {
    const blogPosts = [
        { title: "First Blog Post", content: "This is a placeholder for your first blog post." },
        { title: "Why I Love Coding", content: "Thoughts on problem-solving and creativity." }
    ];

    const blogContainer = document.getElementById('blog-posts');

    if (blogContainer) {
        blogPosts.forEach(post => {
            const postDiv = document.createElement('div');
            postDiv.innerHTML = `<h3>${post.title}</h3><p>${post.content}</p>`;
            blogContainer.appendChild(postDiv);
        });
    }
});
