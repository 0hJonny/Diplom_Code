// src/contollers/articles_controller.go

package controllers

import (
	"go-gin-postgresql-backend/src/models"
	"net/http"

	"go-gin-postgresql-backend/src/utils"

	"github.com/gin-gonic/gin"
)

func Login(c *gin.Context) {

	var err error
	var userData models.AuthUserData
	err = c.ShouldBindJSON(&userData)

	if err != nil {
		c.JSON(400, gin.H{"error": err.Error()})
		return
	}

	user, err := utils.VerifyUser(&userData)

	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"status": "failed", "message": "Invalid email or password!", "data": nil})
		return
	}

	c.JSON(http.StatusOK, gin.H{"status": "success", "message": "User authenticated successfully!", "data": user})

}

func Registration(c *gin.Context) {
	var err error
	var userData models.User

	err = c.ShouldBindJSON(&userData)

	if err != nil {
		c.JSON(400, gin.H{"error": err.Error()})
		return
	}

	_, err = utils.CreateUser(&userData)

	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"status": "failed", "message": "Unable to create user", "data": nil})
		return
	}

	c.JSON(http.StatusCreated, gin.H{"status": "success", "message": "User created successfully", "data": userData})
}
