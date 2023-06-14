package com.qustomate

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import androidx.fragment.app.Fragment
import com.google.android.material.bottomnavigation.BottomNavigationView
import com.qustomate.main_fragment.ChatFragment
import com.qustomate.main_fragment.DashboardFragment
import com.qustomate.main_fragment.ManagementFragment
import com.qustomate.main_fragment.SettingFragment

class MainActivity : AppCompatActivity() {
    private lateinit var bottomNavView: BottomNavigationView

    private val dashboardFragment = DashboardFragment()
    private val chatFragment = ChatFragment()
    private val managementFragment = ManagementFragment()
    private val settingFragment = SettingFragment()

    private val mOnNavigationItemSelectedListener =
        BottomNavigationView.OnNavigationItemSelectedListener { item ->
            when (item.itemId) {
                R.id.navigation_dashboard -> {
                    openFragment(dashboardFragment)
                    return@OnNavigationItemSelectedListener true
                }
                R.id.navigation_chat -> {
                    openFragment(chatFragment)
                    return@OnNavigationItemSelectedListener true
                }
                R.id.navigation_management -> {
                    openFragment(managementFragment)
                    return@OnNavigationItemSelectedListener true
                }
                R.id.navigation_setting -> {
                    openFragment(settingFragment)
                    return@OnNavigationItemSelectedListener true
                }
            }
            false
        }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        bottomNavView = findViewById(R.id.navigationView)
        bottomNavView.setOnNavigationItemSelectedListener(mOnNavigationItemSelectedListener)

        openFragment(dashboardFragment)
    }

    private fun openFragment(fragment: Fragment) {
        supportFragmentManager.beginTransaction().replace(R.id.frameLayout, fragment).commit()
    }
}
