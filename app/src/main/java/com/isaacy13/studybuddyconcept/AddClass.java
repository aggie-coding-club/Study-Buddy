package com.isaacy13.studybuddyconcept;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import com.isaacy13.studybuddyconcept.MainActivity;
public class AddClass extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_class);

        Button addClass = findViewById(R.id.bAddClassSubmit);
        addClass.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // get string user entered
                EditText newClassName = findViewById(R.id.tAddNewClass);
                String addClassName = newClassName.getText().toString();

                SharedPreferences classPreferences = getSharedPreferences("classesSet", Context.MODE_PRIVATE);
                SharedPreferences.Editor classPreferencesEditor = classPreferences.edit();

                ArrayAdapter<String> adapter;

                Set<String> replace;
                System.out.println(String.format("Before define: %s", classPreferences.getStringSet("classesSet", null)));
                if (classPreferences.getStringSet("classesSet", null) != null) {
                    Set<String> tmp = classPreferences.getStringSet("classesSet", null);
                    replace = new HashSet<String>(tmp);

                }
                else {
                    replace = new HashSet<String>();
                }
                replace.add(addClassName);
                classPreferencesEditor.clear();
                classPreferencesEditor.putStringSet("classesSet",  new HashSet<String>(replace)).apply();

                System.out.println(String.format("After define: %s", classPreferences.getStringSet("classesSet", null)));
                finish();
            }
        });
    }
}