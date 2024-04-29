package routes

import (
	"go-gin-postgresql-backend/src/controllers"

	"github.com/gin-gonic/gin"
)

func GroupRouterAuth(baseRouter *gin.RouterGroup) {
	auth := baseRouter.Group("/auth")
	auth.POST("/login", controllers.Login)
	auth.POST("/registration", controllers.Registration)
}
