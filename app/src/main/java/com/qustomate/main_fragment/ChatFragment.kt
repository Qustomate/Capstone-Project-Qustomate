package com.qustomate.main_fragment

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.qustomate.ApiClient
import com.qustomate.ChatAdapter
import com.qustomate.CustomChatMessage
import com.qustomate.R
import kotlinx.coroutines.launch

class ChatFragment : Fragment() {
    private lateinit var chatRecyclerView: RecyclerView
    private lateinit var messageEditText: EditText
    private lateinit var sendButton: Button
    private val messageList = mutableListOf<CustomChatMessage>()
    private val apiService = ApiClient.create()

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_chat, container, false)

        // Initialize RecyclerView
        chatRecyclerView = view.findViewById(R.id.chatRecyclerView)
        chatRecyclerView.layoutManager = LinearLayoutManager(requireContext())

        // Initialize input message components
        messageEditText = view.findViewById(R.id.messageEditText)
        sendButton = view.findViewById(R.id.sendButton)

        // Set click listener for send button
        sendButton.setOnClickListener {
            // Get the text message from user input
            val messageText = messageEditText.text.toString()

            // Create a new CustomChatMessage instance
            val message = CustomChatMessage(
                id_message = "", // Provide the message ID
                message_text = messageText,
                recipientID = "", // Provide the recipient ID
                sender_id = "", // Provide the sender ID
                time_stamp = "" // Provide the timestamp
            )

            // Call sendMessage from a coroutine
            viewLifecycleOwner.lifecycleScope.launch {
                sendMessage(message)
            }
        }

        // Create instance of ChatAdapter and apply it to RecyclerView
        val adapter = ChatAdapter(messageList)
        chatRecyclerView.adapter = adapter

        // Fetch message data from API
        viewLifecycleOwner.lifecycleScope.launch {
            getMessages()
        }

        return view
    }

    private suspend fun sendMessage(message: CustomChatMessage) {
        try {
            val response = apiService.addMessage(message)
            if (response) {
                // Message sent successfully
                getMessages() // Refresh message list after sending the message
            } else {
                // Message sending failed
                Toast.makeText(requireContext(), "Failed to send message", Toast.LENGTH_SHORT).show()
            }
        } catch (e: Exception) {
            // Error sending message, display error message
            Toast.makeText(requireContext(), "Error: ${e.message}", Toast.LENGTH_SHORT).show()
        }
    }

    private suspend fun getMessages() {
        try {
            val messages = apiService.getMessages("https://qustomate.et.r.appspot.com/message/chat/chat-3cbc92d2-c7ec-4")

            // Update message data in adapter
            messageList.clear()
            messageList.addAll(messages)

            // Refresh RecyclerView
            chatRecyclerView.adapter?.notifyDataSetChanged()
        } catch (e: Exception) {
            // Display error message
            Toast.makeText(requireContext(), "Error: ${e.message}", Toast.LENGTH_SHORT).show()
        }
    }
}
