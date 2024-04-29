// go-gin-postgresql-backend/src/models/db.go
package models

import (
	"fmt"
	"log"
	"os"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var DatabaseArticles, DatabaseUsers *gorm.DB

func OpenDtabaseConnection() {

	var err error

	host := os.Getenv("POSTGRES_DATABASE_URL")
	username := os.Getenv("POSTGRES_USERNAME")
	password := os.Getenv("POSTGRES_PASSWORD")
	port := os.Getenv("POSTGRES_PORT")

	articles_name, users_name := os.Getenv("POSTGRES_ARTICLES"), os.Getenv("POSTGRES_USERS")

	connStrArticles := fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%s sslmode=disable application_name=go-server:articles", host, username, password, articles_name, port)
	connStrUsers := fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%s sslmode=disable application_name=go-server:users", host, username, password, users_name, port)

	DatabaseArticles, err = gorm.Open(postgres.Open(connStrArticles), &gorm.Config{})
	if err != nil {
		log.Fatal(err)
	}
	DatabaseUsers, err = gorm.Open(postgres.Open(connStrUsers), &gorm.Config{})
	if err != nil {
		log.Fatal(err)
	}

	log.Println("✨✨✨ Database connection established! ✨✨✨")
}

func CloseDatabaseConnection() {
	sqlDBArticles, err := DatabaseArticles.DB()
	if err != nil {
		log.Fatal(err)
	}
	sqlDBUsers, err := DatabaseUsers.DB()
	if err != nil {
		log.Fatal(err)
	}
	sqlDBArticles.Close()
	sqlDBUsers.Close()
}
