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
        System.out.println(username);
        saveUserName(username);
        //setContentView(R.layout.activity_main);
        startActivity(new Intent(firstWelcomeScreen.this, MainActivity.class));
    }

    private void saveUserName(String username) {
        SharedPreferences sharedPreferences = getSharedPreferences("username", Context.MODE_PRIVATE);
        SharedPreferences.Editor editor = sharedPreferences.edit();
        editor.putString("username", username);
        editor.apply();
    }
}