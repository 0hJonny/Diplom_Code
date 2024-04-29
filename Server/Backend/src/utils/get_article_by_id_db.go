package utils

import "go-gin-postgresql-backend/src/models"

func GetArticleByID(article *models.ArticleAnnotation) (models.ArticleAnnotation, error) {
	query := `
	SELECT 
		a.id AS article_id,
		t.title,
		a.body,
		ln.language_code AS language_native_code,
		la.language_code AS language_to_answer_code,
		la.language_name as language_to_answer_name
	FROM 
		articles a
	LEFT JOIN 
		titles t ON a.id = t.article_id AND t.language_id = a.language_id
	LEFT JOIN 
		languages ln ON a.language_id = ln.language_id
	CROSS JOIN 
		languages la
	WHERE 
		a.id = ?
		AND NOT EXISTS (
			SELECT 
				1 
			FROM 
				annotations an 
			WHERE 
				an.article_id = a.id 
				AND an.language_id = la.language_id
		)
	ORDER BY 
		ln.language_id
	LIMIT 1;`

	if err := models.DatabaseArticles.Raw(query, article.ID).Scan(&article).Error; err != nil {
		return models.ArticleAnnotation{}, err
	}
	return *article, nil
}
