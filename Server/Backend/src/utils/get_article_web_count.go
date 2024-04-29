package utils

import "go-gin-postgresql-backend/src/models"

func GetArticleWebCount(articleWebQuery *models.ArticleWebQuery) (*models.ArticleWebCount, error) {
	var err error
	var count models.ArticleWebCount

	query := `
		SELECT 
			COUNT(articles.id)
		FROM 
			articles
		LEFT JOIN 
			themes ON articles.theme_id = themes.theme_id
		LEFT JOIN 
			annotations ON articles.id = annotations.article_id`

	if articleWebQuery.Category != "" {
		query += ` WHERE themes.theme_name = ? AND annotations.article_id IS NOT NULL`
	} else {
		query += ` WHERE annotations.article_id IS NOT NULL`
	}

	query += ` AND annotations.language_id = (SELECT language_id FROM languages WHERE language_code = ?);`

	err = models.DatabaseArticles.Raw(query, articleWebQuery.LanguageCode).Count(&count.Count).Error
	if err != nil {
		return &models.ArticleWebCount{}, err
	}

	return &count, nil
}
