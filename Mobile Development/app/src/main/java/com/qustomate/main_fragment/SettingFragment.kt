package com.qustomate.main_fragment

import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import androidx.fragment.app.Fragment
import com.qustomate.R
import com.qustomate.main_page.LoadingPageActivity

class SettingFragment : Fragment() {
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_setting, container, false)

        val logoutButton = view.findViewById<Button>(R.id.logout_button)
        logoutButton.setOnClickListener {
            performLogout()
        }

        return view
    }

    private fun performLogout() {
        // Clear user session or perform any necessary cleanup here

        // Start LoadingPageActivity
        val intent = Intent(requireContext(), LoadingPageActivity::class.java)
        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP or Intent.FLAG_ACTIVITY_NEW_TASK)
        startActivity(intent)
        requireActivity().finish() // Finish the current activity
    }
}
