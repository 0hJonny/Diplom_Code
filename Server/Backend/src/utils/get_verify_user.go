package utils

import (
	"go-gin-postgresql-backend/src/middlewares"
	"go-gin-postgresql-backend/src/models"

	"golang.org/x/crypto/bcrypt"
)

func VerifyUser(userData *models.AuthUserData) (*models.User, error) {

	var err error
	var user models.User
	err = models.DatabaseUsers.Raw("SELECT u.*, r.role_name FROM users u JOIN roles r ON u.role_id = r.role_id WHERE u.username = ? AND u.confirmed = true;", userData.Username).Scan(&user).Error

	if err != nil {
		return &models.User{}, err
	}

	err = bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(userData.Password))

	if err != nil {
		return &models.User{}, err
	}

	user.JWT_Token, err = middlewares.GenerateToken(user.User_ID)
	user.Password = ""

	if err != nil {
		return &models.User{}, err
	}

	return &user, nil
}
