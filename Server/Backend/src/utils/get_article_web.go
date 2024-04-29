package utils

import (
	"fmt"
	"go-gin-postgresql-backend/src/models"
)

func GetArticleWeb(articleWebQuery *models.ArticleWebQuery) (*[]models.ArticleWeb, error) {
	var err error
	var articleWebCollection []models.ArticleWeb

	articleWebQuery.Offset = (articleWebQuery.Page - 1) * articleWebQuery.Limit

	query := `
		SELECT 
			articles.id, 
			COALESCE(titles.title, '') AS title, 
			articles.created_at, 
			themes.theme_name,
			json_agg(tags.tag_name) AS tags,
			annotations.annotation
		FROM 
			articles
		LEFT JOIN 
			themes ON articles.theme_id = themes.theme_id
		LEFT JOIN 
			article_tags ON articles.id = article_tags.article_id
		LEFT JOIN 
			tags ON article_tags.tag_id = tags.tag_id
		LEFT JOIN 
			languages lang ON lang.language_code = ?
		LEFT JOIN 
			annotations ON articles.id = annotations.article_id AND annotations.language_id = lang.language_id
		LEFT JOIN
			titles ON articles.id = titles.article_id AND titles.language_id = lang.language_id
	`

	args := []interface{}{articleWebQuery.LanguageCode}

	if articleWebQuery.Category != "" {
		query += ` WHERE themes.theme_name = ? AND annotations.article_id IS NOT NULL`
		args = append(args, articleWebQuery.Category)
	} else {
		query += ` WHERE annotations.article_id IS NOT NULL`
	}

	query += `
		GROUP BY articles.id, titles.title, themes.theme_name, annotations.annotation
		ORDER BY articles.created_at DESC
		LIMIT ? OFFSET ?;`

	args = append(args, articleWebQuery.Limit, articleWebQuery.Offset)

	err = models.DatabaseArticles.Raw(query, args...).Scan(&articleWebCollection).Error

	if err != nil {
		return &[]models.ArticleWeb{}, err
	}

	for i := range articleWebCollection {
		articleWebCollection[i].ImageSource = fmt.Sprintf("/images/%s.png", articleWebCollection[i].ID)
		articleWebCollection[i].LanguageCode = articleWebQuery.LanguageCode
	}

	return &articleWebCollection, nil
}
