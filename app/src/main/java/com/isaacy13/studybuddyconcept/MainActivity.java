package com.isaacy13.studybuddyconcept;

import androidx.appcompat.app.AppCompatActivity;
import androidx.viewpager.widget.ViewPager;

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

import java.util.ArrayList;

import com.google.android.material.tabs.TabItem;
import com.google.android.material.tabs.TabLayout;

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
        setContentView(R.layout.activity_main);
        // if is user's first time, display welcome screen
        if (current_username != "defaultValue")
            welcomeUser(current_username);
        else
            startActivity(new Intent(MainActivity.this, firstWelcomeScreen.class));

        // populate class drop-down menu
        populateClasses();

        // add a class button
        Button addAClass = findViewById(R.id.bAddClass);
        addAClass.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick (View v) {addClass(v);} });

        // temporary reset button
        Button resetSharedPrefs = findViewById(R.id.resetSharedPref);
        resetSharedPrefs.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick (View v) {resetPrefs(v);} });


        // initialize tab bar, tabs, and viewpager
        TabLayout tabLayout = findViewById(R.id.tabBar);
        TabItem tabUploadNotes = findViewById(R.id.TabUploadNotes);
        TabItem tabReviewFlashcards = findViewById(R.id.TabReviewFlashcards);
        TabItem tabGoalProgress = findViewById(R.id.TabGoalProgress);
        final ViewPager viewPager = findViewById(R.id.viewPager);

        // connect viewpager with pageradapter
        PagerAdapter pagerAdapter = new PagerAdapter(getSupportFragmentManager(), tabLayout.getTabCount());
        viewPager.setAdapter(pagerAdapter);

        // change on tab selection
        tabLayout.addOnTabSelectedListener(new TabLayout.OnTabSelectedListener() {
            @Override
            public void onTabSelected(TabLayout.Tab tab) {
                viewPager.setCurrentItem(tab.getPosition());
            }

            @Override
            public void onTabUnselected(TabLayout.Tab tab) { }

            @Override
            public void onTabReselected(TabLayout.Tab tab) { }
        });

    }

    // changes welcome text
    public void welcomeUser(String username) {
        TextView welcomeBack = findViewById(R.id.tNameHolder);
        welcomeBack.setText(String.format("%s", username));
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

    public void addClass(View v) {
        // FIGURE OUT A WAY TO ADD CLASSES TODO
        // maybe sharedpreferences?
    }
}