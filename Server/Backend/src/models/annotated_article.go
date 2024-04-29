// go-gin-postgresql-backend/src/models/annotated_article.go

package models

import (
	"time"
)

type ArticleAnnotation struct {
	ID                   string            `gorm:"column:id;primaryKey" json:"id"`
	Title                string            `json:"title"`
	Body                 string            `json:"body"`
	LanguageID           int               `gorm:"column:language_id" json:"-"`
	LanguageCode         string            `gorm:"column:language_native_code" json:"language_code"`
	LanguageToAnswerCode string            `json:"language_to_answer_code"`
	LanguageToAnswerName string            `json:"language_to_answer_name"`
	ThemeID              int               `gorm:"column:theme_id"`
	ThemeName            string            `json:"theme_name"`
	Tags                 []string          `gorm:"-" json:"tags"`
	Annotation           string            `json:"annotation"`
	NeuralNetworks       map[string]string `gorm:"-" json:"neural_networks"`
	CreatedAt            time.Time         `json:"created_at" gorm:"autoCreateTime"`
}

type ArticleQueryID struct {
	ID string `gorm:"column:id;primaryKey" json:"id"`
}
