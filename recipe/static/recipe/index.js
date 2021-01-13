document.addEventListener("scroll", function () {
	const navbar = document.querySelector(".navbar");
	const navbarHeight = 100;
  
	const distanceFromTop = Math.abs(
	  document.body.getBoundingClientRect().top
	);
  
	if (distanceFromTop >= navbarHeight) navbar.classList.add("fixed-top");
	else navbar.classList.remove("fixed-top");
  });

function limitText(limitField,limitCount, limitNum) {
    if (limitField.value.length > limitNum) {
		limitField.value = limitField.value.substring(0, limitNum);
		console.log(limitField.value)
	}
	else {
		limitCount.value = limitNum - limitField.value.length;
	}
}

function RecentRecipes() {
	fetch('/recentrecipes')
	.then(response => response.json())
	.then(recipes => {


		recipes.forEach(recipe => {	
			
			let col = document.createElement('div');
			col.className = 'col-lg col-md col-sm-6';

			let recipediv = document.createElement('div');
			recipediv.className = 'card';
			recipediv.style = "width: 18rem; margin: 0 0 30px 0;"
			col.appendChild(recipediv)

			let imgRes = document.createElement('img');
			imgRes.style = 'width:286px; height:193.81px';
			imgRes.src = `${recipe.img}`
			recipediv.appendChild(imgRes)

			let cardBody = document.createElement('div');
			cardBody.className = 'card-body';
			recipediv.appendChild(cardBody); 

			let recipeTitle = document.createElement('h5');
			recipeTitle.className = 'card-title'
			recipeTitle.textContent = `${recipe.title}`;
			cardBody.appendChild(recipeTitle);

			let description = document.createElement('p');
			description.className = 'card-text';
			description.textContent = `${recipe.description}`;
			cardBody.appendChild(description);

			let whereTo = document.createElement('a');
			whereTo.className = 'btn btn-primary';
			whereTo.href = `/recipe/${recipe.id}`;
			whereTo.textContent = 'View Recipe'
			cardBody.appendChild(whereTo);


			document.body.querySelector('#recent').appendChild(col);
		}
							)
					}	
		)
}


document.addEventListener('DOMContentLoaded', function(){
	RecentRecipes();
})