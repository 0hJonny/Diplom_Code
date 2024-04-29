// app.go
package main

import (
	"go-gin-postgresql-backend/src/models"
	"go-gin-postgresql-backend/src/routes"
)

func main() {
	models.OpenDtabaseConnection()
	router := routes.SetupRoutes()
	router.Run(":5000")

}
