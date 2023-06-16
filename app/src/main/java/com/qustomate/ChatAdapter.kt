package com.qustomate

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

class ChatAdapter(private val messageList: List<CustomChatMessage>) :
    RecyclerView.Adapter<ChatAdapter.ViewHolder>() {

    private val retrofit = Retrofit.Builder()
        .baseUrl("https://qustomate.et.r.appspot.com/") // Replace with the appropriate base URL
        .addConverterFactory(GsonConverterFactory.create())
        .build()

    private val apiService = retrofit.create(ApiService::class.java)

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_chat, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val message = messageList[position]
        holder.bind(message)

        holder.itemView.setOnClickListener {
            // Perform the appropriate action when a conversation item is clicked
        }
    }

    override fun getItemCount(): Int {
        return messageList.size
    }

    inner class ViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val messageTextView: TextView = itemView.findViewById(R.id.messageTextView)

        fun bind(message: CustomChatMessage) {
            messageTextView.text = message.message_text
        }
    }

    suspend fun sendMessage(message: CustomChatMessage) {
        try {
            val response = apiService.addMessage(message)
            if (response) {
                // Message sent successfully
            } else {
                // Message sending failed
            }
        } catch (t: Throwable) {
            // Error sending message, display error message
        }
    }
}
