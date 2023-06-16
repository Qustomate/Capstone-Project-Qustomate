package com.qustomate

data class ChatMessage(
    val id: String,
    val text: String,
    val senderId: String,
    val recipientId: String,
    val timeStamp: String
)
