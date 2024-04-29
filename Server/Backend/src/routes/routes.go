// go-gin-postgresql-backend/src/routes/startup.go

package routes

import (
	"github.com/gin-gonic/gin"
)

func GroupRouter(baseRouter *gin.RouterGroup) {
	GroupRouterAuth(baseRouter)
	GroupRouterPrivate(baseRouter)
	GroupRouterPublic(baseRouter)
}

func SetupRoutes() *gin.Engine {

	router := gin.Default()

	routerVersion := router.Group("/api/v1")
	GroupRouter(routerVersion)

	return router
}
