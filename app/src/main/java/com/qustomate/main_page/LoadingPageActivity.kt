package com.qustomate.main_page

import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import androidx.appcompat.app.AppCompatActivity
import com.qustomate.R


class LoadingPageActivity : AppCompatActivity() {

    private val splashTimeout: Long = 3000 // 3 seconds

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_loading_page)

        Handler(Looper.getMainLooper()).postDelayed({
            val intent = Intent(this, WelcomePageActivity::class.java)
            startActivity(intent)
            finish()
        }, splashTimeout)
    }
}
