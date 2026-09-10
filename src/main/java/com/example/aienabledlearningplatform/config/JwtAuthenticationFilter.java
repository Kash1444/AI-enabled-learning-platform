package com.example.aienabledlearningplatform.config;

import com.example.aienabledlearningplatform.service.JwtService;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.List;

@Component
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    private final JwtService jwtService;

    public JwtAuthenticationFilter(JwtService jwtService) {
        this.jwtService = jwtService;
    }

    @Override
    protected void doFilterInternal(
            HttpServletRequest request,
            HttpServletResponse response,
            FilterChain filterChain)
            throws ServletException, IOException {

        System.out.println("========== JWT FILTER ==========");

        String authHeader = request.getHeader("Authorization");

        System.out.println("Authorization Header: " + authHeader);

        if (authHeader == null || !authHeader.startsWith("Bearer ")) {

            System.out.println("NO JWT TOKEN");
            filterChain.doFilter(request, response);
            return;
        }

        String token = authHeader.substring(7);

        System.out.println("JWT TOKEN FOUND");

        if (!jwtService.isTokenValid(token)) {

            System.out.println("JWT TOKEN INVALID");

            filterChain.doFilter(request, response);
            return;
        }

        System.out.println("JWT TOKEN VALID");

        String email = jwtService.extractEmail(token);
        String role = jwtService.extractRole(token);

        System.out.println("EMAIL: " + email);
        System.out.println("ROLE: " + role);

        SimpleGrantedAuthority authority =
                new SimpleGrantedAuthority("ROLE_" + role);

        UsernamePasswordAuthenticationToken authentication =
                new UsernamePasswordAuthenticationToken(
                        email,
                        null,
                        List.of(authority)
                );

        SecurityContextHolder
                .getContext()
                .setAuthentication(authentication);

        System.out.println("AUTHENTICATION SET");
        System.out.println("AUTH: "
                + SecurityContextHolder.getContext().getAuthentication());
        System.out.println("AUTHORITY: "
                + authentication.getAuthorities());

        System.out.println("IS AUTHENTICATED: "
                + authentication.isAuthenticated());

        filterChain.doFilter(request, response);
    }
}