function createArticleElement(content) {
  const article = document.createElement("p");
  article.textContent = content;
  return article;
}

const articleContainer = document.getElementById("article-container");
function myOnClick(i) {
  if (articleContainer.children.length == 0) {
    fetch(`http://127.0.0.1:8000/api/articles/${i}`)
      .then(res => res.json())
      .then(res => {
        console.log("hi server!");
        const article = createArticleElement(res.article);
        articleContainer.appendChild(article);
      }).catch(err => console.log(err));
  } else {
    articleContainer.removeChild(articleContainer.firstChild);
    myOnClick(i);
  }
}

const buttonContainer = document.getElementById("button-container");
for (let i = 0; i < 5; i++) {
  const button = document.createElement("button");
  button.textContent = i;
  button.onclick = () => { myOnClick(i) };

  buttonContainer.appendChild(button);
}