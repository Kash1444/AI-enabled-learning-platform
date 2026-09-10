package com.example.aienabledlearningplatform.dto;

import com.example.aienabledlearningplatform.entity.User;

public class LoginResponse {

    private String message;
    private Long userId;
    private String username;
    private String email;
    private User.Role role;
    private String token;

    public LoginResponse(
            String message,
            Long userId,
            String username,
            String email,
            User.Role role,
            String token) {

        this.message = message;
        this.userId = userId;
        this.username = username;
        this.email = email;
        this.role = role;
        this.token = token;
    }

    public String getMessage() {
        return message;
    }

    public Long getUserId() {
        return userId;
    }

    public String getUsername() {
        return username;
    }

    public String getEmail() {
        return email;
    }

    public User.Role getRole() {
        return role;
    }
    public String getToken() {
        return token;
    }
}