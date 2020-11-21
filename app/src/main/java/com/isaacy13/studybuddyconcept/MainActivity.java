package com.isaacy13.studybuddyconcept;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.viewpager.widget.ViewPager;

import android.app.Dialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.MotionEvent;
import android.view.View;
import android.view.WindowManager;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.TextView;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.concurrent.TimeUnit;

import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.tabs.TabItem;
import com.google.android.material.tabs.TabLayout;

//https://devpost.com/software/studybuddy-jkvyc7

public class MainActivity extends AppCompatActivity {
    // TODO - Make different classes matter
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // making everything fullscreen
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);

        // grab shared preferences username values
        SharedPreferences sharedPreferences = getSharedPreferences("username", Context.MODE_PRIVATE);
        String current_username = sharedPreferences.getString("username", "defaultValue");
        setContentView(R.layout.activity_main);

        // if is user's first time, display welcome screen
        if (current_username != "defaultValue")
            welcomeUser(current_username);
        else
            startActivity(new Intent(MainActivity.this, firstWelcomeScreen.class));

        // create instance of FAB
        FloatingActionButton fabMainActivityBase = findViewById(R.id.fabActivityMainBase);

        // on click, either make button menu show or disappear
        fabMainActivityBase.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {showButtonMenu(v);}
        });

        // populate spinner on wake
        populateSpinner(this.getCurrentFocus());
        // look for touches on spinner
        Spinner spinner = findViewById(R.id.spinner);
        spinner.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                populateSpinner(v);
                return false;
            }
        });

        //// create instances of FABS in sub-menu && perform respective actions
        // add class fab
        FloatingActionButton fabMainActivityAddClass = findViewById(R.id.fabActivityMainAddClass);
        // new view to let user add class
        fabMainActivityAddClass.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                addClass(v);
                SharedPreferences tmp = getSharedPreferences("classesSet", Context.MODE_PRIVATE);
                if (tmp.getStringSet("classesSet", null) != null)
                    populateSpinner(v);
            }
        });

        // reset shared preferences fab
        FloatingActionButton fabMainActivityResetPrefs = findViewById(R.id.fabActivityMainResetSharedPrefs);
        // reset all shared preferences -- TODO -- move to under PFP
        fabMainActivityResetPrefs.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                resetPrefs(v);
            }
        });

        // initialize tab bar, tabs, and viewpager
        TabLayout tabLayout = findViewById(R.id.tabBar);
        TabItem tabUploadNotes = findViewById(R.id.TabUploadNotes);
        TabItem tabReviewFlashcards = findViewById(R.id.TabReviewFlashcards);
        TabItem tabGoalProgress = findViewById(R.id.TabGoalProgress);
        final ViewPager viewPager = findViewById(R.id.viewPager);

        // connect viewpager with pager adapter
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

    // resets shared preferences
    public void resetPrefs (View v) {
        final SharedPreferences usernamePreferences = getSharedPreferences("username", Context.MODE_PRIVATE);
        final SharedPreferences.Editor usernameEditor = usernamePreferences.edit();

        final SharedPreferences classPreferences = getSharedPreferences("classesSet", Context.MODE_PRIVATE);
        final SharedPreferences.Editor classesEditor = classPreferences.edit();

        System.out.println(String.format("Classes before clear: %s", classPreferences.getStringSet("classesSet", null)));

        // ask user what they'd like to reset and perform accordingly
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Reset");
        builder.setMessage("Would you like to reset the username or the class list?");
        builder.setPositiveButton("Username", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                usernameEditor.remove("username");
                usernameEditor.apply();
                startActivity(new Intent(MainActivity.this, firstWelcomeScreen.class));
            }
        });
        builder.setNegativeButton("Class list", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                classesEditor.remove("classesSet").apply();
                System.out.println(String.format("Classes after clear: %s", classPreferences.getString("classesSet", null)));
            }
        });
        builder.show();
    }

    public void addClass(View v) {
        System.out.println("Called addClass");
        // FIGURE OUT A WAY TO ADD CLASSES TODO
        // CHECK IF ALREADY EXISTS
        // maybe sharedpreferences?

        // get class name and store in shared preferences
        startActivity(new Intent(MainActivity.this, AddClass.class));
        SharedPreferences classPreferences = getSharedPreferences("classesSet", Context.MODE_PRIVATE);
    }

    public void showButtonMenu(View v) {
        FloatingActionButton fabAddClass = findViewById(R.id.fabActivityMainAddClass);
        FloatingActionButton fabResetPrefs = findViewById(R.id.fabActivityMainResetSharedPrefs);

        if (fabAddClass.getVisibility() == View.INVISIBLE) {
            fabAddClass.setVisibility(View.VISIBLE);
            fabResetPrefs.setVisibility(View.VISIBLE);
        }
        else if (fabAddClass.getVisibility() == View.VISIBLE){
            fabAddClass.setVisibility(View.INVISIBLE);
            fabResetPrefs.setVisibility(View.INVISIBLE);
        }
    }

    public void populateSpinner (View v) {
        System.out.println("Called populateSpinner");
        Spinner spinner = findViewById(R.id.spinner);

        // get what's inside of shared preferences
        SharedPreferences classPreferences = getSharedPreferences("classesSet", Context.MODE_PRIVATE);
        Set<String> classes_set = classPreferences.getStringSet("classesSet", null);

        if (classPreferences.getStringSet("classesSet", null) == null) {
            Set<String> tmp = new HashSet<String>();
            tmp.add("SELECT COURSE");
            SharedPreferences.Editor classPreferencesEditor = classPreferences.edit();
            classPreferencesEditor.putStringSet("classesSet", tmp);

            List<String> tmp_list = new ArrayList<String>();
            for (String x : tmp)
                tmp_list.add(x);

            ArrayAdapter<String> adapter = new ArrayAdapter<String>(this, android.R.layout.simple_spinner_dropdown_item, tmp_list);
            adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
            spinner.setAdapter(adapter);
            return;
        }

        // put into a list
        List<String> classes_list = new ArrayList<String>();
        for (String x : classes_set)
            classes_list.add(x);

        for (String x : classes_list)
            System.out.println(String.format("Populating spinner with: %s", x));

        // put into adapter
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(this, android.R.layout.simple_spinner_dropdown_item, classes_list);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinner.setAdapter(adapter);
    }
}