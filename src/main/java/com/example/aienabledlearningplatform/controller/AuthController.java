package com.example.aienabledlearningplatform.controller;

import com.example.aienabledlearningplatform.dto.LoginRequest;
import com.example.aienabledlearningplatform.dto.LoginResponse;
import com.example.aienabledlearningplatform.service.AuthService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @PostMapping("/login")
    public LoginResponse login(@RequestBody LoginRequest request) {
        return authService.login(request);
    }
}