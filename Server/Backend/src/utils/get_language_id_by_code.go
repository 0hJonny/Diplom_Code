package utils

import "go-gin-postgresql-backend/src/models"

func GetLanguageIdByCode(language *models.Language) (models.Language, error) {

	if err := models.DatabaseArticles.Raw("SELECT * FROM languages WHERE language_code = ?", language.Code).Scan(&language).Error; err != nil {
		return models.Language{}, err
	}

	return *language, nil
}
