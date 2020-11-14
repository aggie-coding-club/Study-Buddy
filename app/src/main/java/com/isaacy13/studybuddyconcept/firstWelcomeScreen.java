package com.isaacy13.studybuddyconcept;

import androidx.appcompat.app.AppCompatActivity;

import java.lang.System;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.io.FileWriter;
import java.io.IOException;

public class firstWelcomeScreen extends AppCompatActivity {
    Button submit;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_first_welcome_screen);

        submit = (Button) findViewById(R.id.bGetStarted);

        submit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                System.out.println("Button pressed");
                nameSubmit(v);
            }
        });
    }

    public void nameSubmit (View v) {
        EditText tv = findViewById(R.id.ptEnterName);
        String username = tv.getText().toString();
        if (validUsername(username)) {
            saveUserName(username);
            startActivity(new Intent(firstWelcomeScreen.this, MainActivity.class));
        }
    }

    private void saveUserName(String username) {
        SharedPreferences sharedPreferences = getSharedPreferences("username", Context.MODE_PRIVATE);
        SharedPreferences.Editor editor = sharedPreferences.edit();
        editor.putString("username", username);
        editor.apply();
    }

    public boolean validUsername(String s) {
        try {
            // username can't be longer than 20 characters or have any invalid symbols
            if (s.length() > 20)
                throw new RuntimeException("The username can't be longer than 20 characters");
            else if (s.length() == 0)
                throw new RuntimeException("The username can't be blank");

            // check for invalid symbols
            s = s.toLowerCase();
            char[] s_charArray = s.toCharArray();
            int numLetters = 0;

            // username can only have letters, dashes, spaces, and numbers
            for (int i = 0; i < s_charArray.length; i++) {
                if (!Character.isDigit(s_charArray[i]) && !Character.isLetter(s_charArray[i]) && s_charArray[i] != ' ' && s_charArray[i] != '-')
                    throw new RuntimeException("The username can only have letters, dashes, spaces, and numbers");
                if (Character.isLetter(s_charArray[i]))
                    numLetters++;
            }
            if (numLetters == 0)
                throw new RuntimeException("You have to have at least one letter in your username");
            return true;
        } catch (Exception e) {
            // when exception is thrown, pop up alert
            Toast.makeText(getApplicationContext(), e.getMessage(), Toast.LENGTH_LONG).show();
            return false;
        }
    }
}