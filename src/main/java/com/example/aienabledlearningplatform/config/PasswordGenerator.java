package com.example.aienabledlearningplatform.config;

import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

public class PasswordGenerator {

    public static void main(String[] args) {

        BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();

        String password = "123456";

        String hash = encoder.encode(password);

        System.out.println("Generated Hash:");
        System.out.println(hash);

        System.out.println("Password Match:");
        System.out.println(encoder.matches(password, hash));
    }
}