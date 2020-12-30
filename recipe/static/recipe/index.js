function getCatitemLikes(){
    fetch('/api/allrecipes').then(response => response.json())
    .then(data => {
        const recipeItems = data.map(item => {
            document.getElementById('CatItemLikes').innerHTML = item.likes;
        })
    })
}