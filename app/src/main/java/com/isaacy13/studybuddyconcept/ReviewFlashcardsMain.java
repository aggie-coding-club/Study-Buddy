package com.isaacy13.studybuddyconcept;
import androidx.fragment.app.Fragment;

public class ReviewFlashcardsMain extends ReviewFlashcardsFragmentManager {
    @Override
    protected Fragment createFragment() {
        return new ReviewFlashcardsFragment().newInstance();
    }
}
