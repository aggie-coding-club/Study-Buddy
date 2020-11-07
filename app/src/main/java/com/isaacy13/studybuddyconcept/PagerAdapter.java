package com.isaacy13.studybuddyconcept;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentPagerAdapter;

public class PagerAdapter extends FragmentPagerAdapter {
    private int numOfTabs;

    public PagerAdapter (FragmentManager fm, int numOfTabs) {
        super(fm);
        this.numOfTabs = numOfTabs;
    }

    @NonNull
    @Override
    public Fragment getItem(int position) {
        switch(position) {
            case 0:
                return new UploadNotesFragment();
            case 1:
                return new ReviewFlashcardsFragment();
            case 2:
                return new GoalProgressFragment();
            default:
                return null;
        }
    }

    @Override
    public int getCount() { return numOfTabs; }
}
