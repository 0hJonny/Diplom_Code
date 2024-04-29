// go-gin-postgresql-backend/src/models/user.go

package models

import (
	"time"
)

type User struct {
	User_ID   int       `json:"-" gorm:"column:user_id;primary_key"`
	Username  string    `json:"username" binding:"required" gorm:"column:username;unique;not null"`
	Email     string    `json:"email" binding:"required" gorm:"column:email;unique;not null"`
	Password  string    `json:"password,omitempty" binding:"required"`
	FirstName string    `json:"first_name" gorm:"column:first_name"`
	LastName  string    `json:"last_name" gorm:"column:last_name"`
	Birthdate time.Time `json:"birthdate"`
	Avatar    string    `json:"avatar,omitempty"`
	Confirmed bool      `json:"-" gorm:"-"`
	CreatedAt time.Time `json:"created_at" gorm:"column:created_at;autoCreateTime"`
	Role_name string    `json:"role"`
	JWT_Token string    `json:"jwt_token,omitempty" gorm:"-"`
}

type AuthUserData struct {
	Username string `json:"username" binding:"required"`
	Password string `json:"password" binding:"required"`
}
