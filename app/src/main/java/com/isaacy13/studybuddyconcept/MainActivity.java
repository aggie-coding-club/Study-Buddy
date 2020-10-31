package com.isaacy13.studybuddyconcept;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.view.WindowManager;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.TextView;

//https://devpost.com/software/studybuddy-jkvyc7

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // making everything fullscreen
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
        // grab sharedpreferences values
        SharedPreferences sharedPreferences = getSharedPreferences("username", Context.MODE_PRIVATE);
        String current_username = sharedPreferences.getString("username", "defaultValue");

        // if is user's first time, display welcome screen
        if (current_username != "defaultValue") {
            setContentView(R.layout.activity_main);
            welcomeUser(current_username);
        } else {
            startActivity(new Intent(MainActivity.this, firstWelcomeScreen.class));
        }

        // populate class drop-down menu
        populateClasses();

        // temporary reset buttons
        Button resetSharedPrefs = findViewById(R.id.resetSharedPref);
        resetSharedPrefs.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick (View v) {resetPrefs(v);}});
    }

    // changes welcome text
    public void welcomeUser(String username) {
        TextView welcomeBack = findViewById(R.id.tWelcomeBack);
        welcomeBack.setText(String.format("Welcome back, %s", username));
    }

    // resets sharedpreferences
    public void resetPrefs (View v) {
        SharedPreferences sharedPreferences = getSharedPreferences("username", Context.MODE_PRIVATE);
        SharedPreferences.Editor editor = sharedPreferences.edit();
        editor.remove("username");
        editor.commit();
        startActivity(new Intent(MainActivity.this, firstWelcomeScreen.class));
    }

    public void populateClasses () {
        Spinner spinner = (Spinner) findViewById(R.id.spinner);
        ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(this, R.array.classes_array, android.R.layout.simple_spinner_item);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinner.setAdapter(adapter);
    }
}