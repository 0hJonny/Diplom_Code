package utils

import (
	"fmt"
	"go-gin-postgresql-backend/src/models"
)

func GetArticleSearch(articleWebQuery *models.ArticleWebQuery) (*[]models.ArticleWeb, error) {
	var err error
	var articleWebCollection []models.ArticleWeb

	articleWebQuery.Offset = (articleWebQuery.Page - 1) * articleWebQuery.Limit

	// lang, err := GetLanguageIdByCode(&models.Language{Code: articleWebQuery.LanguageCode})
	// if err != nil {
	// 	return &[]models.ArticleWeb{}, err
	// }

	query := `
		SELECT 
			articles.id, 
			COALESCE(titles.title, '') AS title, 
			articles.created_at, 
			themes.theme_name,
			json_agg(tags.tag_name) AS tags,
			annotations.annotation,
			lang.language_name
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
		AND (
			to_tsvector('simple', COALESCE(titles.title, '')) @@ plainto_tsquery('simple', $2) 
			OR to_tsvector('simple', COALESCE(annotations.annotation, '')) @@ plainto_tsquery('simple', $2)
			OR (
				SELECT array_to_string(array_agg(tags.tag_name), ' ')
				FROM tags
				JOIN article_tags ON article_tags.tag_id = tags.tag_id
				WHERE article_id = articles.id
			) @@ plainto_tsquery('simple', $2)
		)
		GROUP BY articles.id, titles.title, themes.theme_name, annotations.annotation, lang.language_name
		ORDER BY 
			articles.post_date DESC,
			ts_rank(to_tsvector('simple', COALESCE(titles.title, '')), plainto_tsquery('simple', $2)) DESC,
			ts_rank(to_tsvector('simple', COALESCE(annotations.annotation, '')), plainto_tsquery('simple', ?)) DESC
		LIMIT ? OFFSET ?;`

	args = append(args, articleWebQuery.Query, articleWebQuery.Limit, articleWebQuery.Offset)

	// With Lang
	// query += `
	// 	AND (to_tsvector(?, COALESCE(titles.title, '')) @@ plainto_tsquery(?, ?)
	// 	OR to_tsvector(?, COALESCE(annotations.annotation, '')) @@ plainto_tsquery(?, ?))
	// 	GROUP BY articles.id, titles.title, themes.theme_name, annotations.annotation, lang.language_name
	// 	ORDER BY
	// 		ts_rank(to_tsvector(?, COALESCE(titles.title, '')), plainto_tsquery(?, ?)) DESC,
	// 		ts_rank(to_tsvector(?, COALESCE(annotations.annotation, '')), plainto_tsquery(?, ?)) DESC,
	// 		articles.post_date DESC
	// 	LIMIT ? OFFSET ?;`

	// args = append(args, lang.Name, lang.Name, articleWebQuery.Query, lang.Name, lang.Name, articleWebQuery.Query, lang.Name, lang.Name, articleWebQuery.Query, lang.Name, lang.Name, articleWebQuery.Query, articleWebQuery.Limit, articleWebQuery.Offset)

	err = models.DatabaseArticles.Raw(query, args...).Scan(&articleWebCollection).Error

	// log.Printf("articleWebCollection: %+v", articleWebCollection)

	if err != nil {
		return &[]models.ArticleWeb{}, err
	}

	for i := range articleWebCollection {
		articleWebCollection[i].ImageSource = fmt.Sprintf("/images/%s.png", articleWebCollection[i].ID)
		articleWebCollection[i].LanguageCode = articleWebQuery.LanguageCode
	}

	return &articleWebCollection, nil
}
