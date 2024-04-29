package utils

import (
	"go-gin-postgresql-backend/src/models"
)

func GetAnnotationQueue() (*[]models.ArticleQueryID, error) {
	var articleQueue []models.ArticleQueryID

	query := `SELECT articles.id
	FROM articles
	LEFT JOIN (
		SELECT DISTINCT article_id
		FROM annotations
	) AS annotated_articles ON articles.id = annotated_articles.article_id
	WHERE articles.language_id IS NOT NULL
	AND articles.id NOT IN (
		SELECT article_id
		FROM annotations
		GROUP BY article_id
		HAVING COUNT(DISTINCT language_id) = (
			SELECT COUNT(*) FROM languages
		)
	);`

	err := models.DatabaseArticles.Raw(query).Scan(&articleQueue).Error

	if err != nil {
		return &[]models.ArticleQueryID{}, err
	}

	return &articleQueue, nil
}
