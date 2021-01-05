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

function showAllRecipes() {
	fetch('/recentrecipes')
	.then(response => response.json())
	.then(recipes => {
		for (var i=0; i < recipes.length; i++){
			console.log(recipes[i].title);
			document.querySelector('#main').innerHTML = recipes[i].title;
		}
	})
}

showAllRecipes();