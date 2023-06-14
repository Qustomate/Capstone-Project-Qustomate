package com.qustomate.main_fragment

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import com.qustomate.dashboard_sencond_fragment.HandleClientFragment
import com.qustomate.R
import com.qustomate.dashboard_sencond_fragment.SentimentAnalysisFragment
import com.qustomate.dashboard_sencond_fragment.TotalPendapatanFragment

class DashboardFragment : Fragment() {

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        val view = inflater.inflate(R.layout.fragment_dashboard, container, false)
        return view
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // Menambahkan HandleClientFragment ke dalam handleClientContainer
        val handleClientFragment = HandleClientFragment()
        childFragmentManager.beginTransaction()
            .replace(R.id.handleClientContainer, handleClientFragment)
            .commit()

        // Menambahkan TotalPendapatanFragment ke dalam totalPendapatanContainer
        val totalPendapatanFragment = TotalPendapatanFragment()
        childFragmentManager.beginTransaction()
            .replace(R.id.totalPendapatanContainer, totalPendapatanFragment)
            .commit()

        // Menambahkan SentimentAnalysisFragment ke dalam sentimentAnalysisContainer
        val sentimentAnalysisFragment = SentimentAnalysisFragment()
        childFragmentManager.beginTransaction()
            .replace(R.id.sentimentAnalysisContainer, sentimentAnalysisFragment)
            .commit()
    }
}
