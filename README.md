Fivesquare API: Service that allows users to write reviews of businesses

Requirements:

User posts review for business
Store{
	rating: 1 - 5 stars,
	review: text,
	tags: [freeform]
}

Business{
	reviews: [chron order],
	rating: overall,
	tags: [summary from reviews],
	location: geotag
}