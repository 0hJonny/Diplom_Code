package utils

import (
	"errors"
	"go-gin-postgresql-backend/src/models"
)

func CreateUser(user *models.User) (*models.User, error) {

	models.DatabaseUsers.Raw("SELECT u.* FROM users u WHERE u.username = ? OR u.email = ? LIMIT 1;", user.Username, user.Email).Scan(&user)

	if user.User_ID != 0 {
		return &models.User{}, errors.New("username or email already exists")
	}

	err := models.DatabaseUsers.Exec("INSERT INTO users (username, password, email) VALUES (?, ?, ?) RETURNING user_id;", user.Username, user.Password, user.Email).Error
	if err != nil {
		return &models.User{}, err
	}
	return user, nil
}
