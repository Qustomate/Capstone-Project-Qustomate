package com.qustomate.main_page

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import com.qustomate.R
import com.qustomate.MainActivity

class LoginPageActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login_page)

        val loginButton = findViewById<Button>(R.id.login_button)
        loginButton.setOnClickListener {
            // TODO: Perform login verification with API cloud
            val email = "sales2@gmail.com"
            val password = "sales002"

            val loginManager = LoginManager()
            loginManager.performLogin(email, password)

            val intent = Intent(this, MainActivity::class.java)
            startActivity(intent)
        }

        val googleLoginButton = findViewById<Button>(R.id.google_login_button)
        googleLoginButton.setOnClickListener {
            // TODO: Implement login with Google

            val intent = Intent(this, MainActivity::class.java)
            startActivity(intent)
        }
    }
}
